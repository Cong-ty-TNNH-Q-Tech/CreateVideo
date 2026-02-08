"""
ModelManager - Singleton for managing all AI models with lazy loading and caching.

Benefits:
- Load models once, reuse across multiple tasks
- Pre-load models at startup in background threads
- Thread-safe access
- Automatic cleanup on errors
- Eliminates 10-25s model loading overhead for every task after the first
"""

import os
import time
import threading
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from loguru import logger


def _detect_device(preferred: str = "auto") -> str:
    """
    Detect the best available device.
    Priority: CUDA GPU > CPU.
    
    Args:
        preferred: 'auto' (detect), 'cuda', or 'cpu'
    Returns:
        'cuda' or 'cpu'
    """
    if preferred == "cpu":
        return "cpu"
    
    try:
        import torch
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            vram_mb = torch.cuda.get_device_properties(0).total_mem / 1024 / 1024
            logger.info(
                f"🎮 GPU detected: {device_name} ({vram_mb:.0f} MB VRAM)"
            )
            return "cuda"
        else:
            logger.info("🖥️  No CUDA GPU detected, using CPU")
            return "cpu"
    except ImportError:
        logger.info("🖥️  PyTorch not available, using CPU")
        return "cpu"
    except Exception as e:
        logger.warning(f"⚠️  GPU detection failed ({e}), falling back to CPU")
        return "cpu"


class ModelManager:
    """
    Singleton class to manage all AI models with lazy loading and caching.

    Usage:
        manager = ModelManager.get_instance()
        whisper = manager.get_whisper()
        transformer = manager.get_sentence_transformer()
        clip_model, clip_processor = manager.get_clip_model()
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        # Model cache
        self._whisper_model = None
        self._sentence_transformer = None
        self._sentence_transformer_name = None
        self._clip_model = None
        self._clip_processor = None
        self._clip_model_name = None

        # Device detection (GPU priority, CPU fallback)
        self._device = _detect_device("auto")

        # Status tracking
        self._models_preloaded = False
        self._loading_errors: Dict[str, str] = {}
        self._load_times: Dict[str, float] = {}

        # Config cache
        self._config = None

        logger.info(f"🔧 ModelManager initialized (device={self._device})")

    @classmethod
    def get_instance(cls) -> "ModelManager":
        """Get singleton instance (thread-safe)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = ModelManager()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset singleton (for testing or forced reload)."""
        with cls._lock:
            if cls._instance:
                cls._instance.cleanup_all()
            cls._instance = None
            logger.warning("🔄 ModelManager instance reset")

    def _get_config(self):
        """Lazy load config."""
        if self._config is None:
            from app.config import config
            self._config = config
        return self._config

    # ========================================================================
    # WHISPER MODEL (faster-whisper)
    # ========================================================================

    def get_whisper(self, force_reload: bool = False) -> Any:
        """
        Get Whisper model for speech-to-text.
        Returns a faster_whisper.WhisperModel instance.
        """
        if self._whisper_model is not None and not force_reload:
            return self._whisper_model

        try:
            from faster_whisper import WhisperModel
            from app.utils import utils

            config = self._get_config()
            model_size = config.whisper.get("model_size", "large-v3")
            # Use config device if explicitly set, otherwise auto-detect
            cfg_device = config.whisper.get("device", "auto")
            device = cfg_device if cfg_device != "auto" else self._device
            # Use float16 on GPU for speed, int8 on CPU for memory
            default_compute = "float16" if device == "cuda" else "int8"
            compute_type = config.whisper.get("compute_type", default_compute)

            # Check for local model first
            model_path = f"{utils.root_dir()}/models/whisper-{model_size}"
            model_bin_file = f"{model_path}/model.bin"
            if not os.path.isdir(model_path) or not os.path.isfile(model_bin_file):
                model_path = model_size

            logger.info(
                f"🤖 [ModelManager] Loading Whisper: {model_size} "
                f"(device={device}, compute_type={compute_type})"
            )
            start_time = time.time()

            self._whisper_model = WhisperModel(
                model_size_or_path=model_path,
                device=device,
                compute_type=compute_type,
            )

            load_time = time.time() - start_time
            self._load_times["whisper"] = load_time
            self._loading_errors.pop("whisper", None)
            logger.success(f"✅ [ModelManager] Whisper loaded in {load_time:.1f}s")

        except Exception as e:
            error_msg = f"Failed to load Whisper model: {e}"
            logger.error(f"❌ [ModelManager] {error_msg}")
            self._loading_errors["whisper"] = error_msg
            raise

        return self._whisper_model

    # ========================================================================
    # SENTENCE TRANSFORMER (semantic search / video matching)
    # ========================================================================

    def get_sentence_transformer(
        self,
        model_name: str = "all-mpnet-base-v2",
        force_reload: bool = False,
    ) -> Any:
        """
        Get SentenceTransformer model for semantic similarity.
        Returns a sentence_transformers.SentenceTransformer instance.
        """
        needs_reload = (
            self._sentence_transformer is None
            or self._sentence_transformer_name != model_name
            or force_reload
        )

        if not needs_reload:
            return self._sentence_transformer

        try:
            from sentence_transformers import SentenceTransformer

            # Prefer GPU, fallback to CPU
            device = self._device

            logger.info(
                f"🤖 [ModelManager] Loading SentenceTransformer: {model_name} "
                f"(device={device})"
            )
            start_time = time.time()

            try:
                self._sentence_transformer = SentenceTransformer(model_name, device=device)
            except Exception as gpu_err:
                if device == "cuda":
                    logger.warning(
                        f"⚠️  GPU loading failed ({gpu_err}), falling back to CPU"
                    )
                    device = "cpu"
                    self._sentence_transformer = SentenceTransformer(model_name, device=device)
                else:
                    raise
            self._sentence_transformer_name = model_name

            load_time = time.time() - start_time
            self._load_times["sentence_transformer"] = load_time
            self._loading_errors.pop("sentence_transformer", None)
            logger.success(
                f"✅ [ModelManager] SentenceTransformer loaded in {load_time:.1f}s "
                f"(max_seq_length={self._sentence_transformer.max_seq_length})"
            )

        except Exception as e:
            error_msg = f"Failed to load SentenceTransformer: {e}"
            logger.error(f"❌ [ModelManager] {error_msg}")
            self._loading_errors["sentence_transformer"] = error_msg
            raise

        return self._sentence_transformer

    # ========================================================================
    # CLIP MODEL (image-text similarity)
    # ========================================================================

    def get_clip_model(
        self,
        model_name: str = "clip-vit-base-patch32",
        force_reload: bool = False,
    ) -> tuple:
        """
        Get CLIP model and processor for image-text similarity.
        Returns tuple of (CLIPModel, CLIPProcessor).
        """
        # Map short names to HuggingFace model IDs
        model_mapping = {
            "clip-vit-base-patch32": "openai/clip-vit-base-patch32",
            "clip-vit-base-patch16": "openai/clip-vit-base-patch16",
            "clip-vit-large-patch14": "openai/clip-vit-large-patch14",
        }
        hf_model_name = model_mapping.get(model_name, model_name)

        needs_reload = (
            self._clip_model is None
            or self._clip_model_name != model_name
            or force_reload
        )

        if not needs_reload:
            return self._clip_model, self._clip_processor

        try:
            from transformers import CLIPProcessor, CLIPModel

            cache_dir = os.path.expanduser("~/.cache/huggingface/transformers")
            os.makedirs(cache_dir, exist_ok=True)

            # Prefer GPU, fallback to CPU
            device = self._device

            logger.info(f"🤖 [ModelManager] Loading CLIP: {model_name} (device={device})")
            start_time = time.time()

            # Load processor (slow tokenizer for compatibility)
            self._clip_processor = CLIPProcessor.from_pretrained(
                hf_model_name,
                cache_dir=cache_dir,
                use_fast=False,
            )

            # Load model - try safetensors first
            try:
                self._clip_model = CLIPModel.from_pretrained(
                    hf_model_name,
                    cache_dir=cache_dir,
                    use_safetensors=True,
                )
            except Exception:
                self._clip_model = CLIPModel.from_pretrained(
                    hf_model_name,
                    cache_dir=cache_dir,
                )

            # Move to detected device (GPU if available, else CPU)
            try:
                self._clip_model = self._clip_model.to(device)
            except Exception as gpu_err:
                if device == "cuda":
                    logger.warning(
                        f"⚠️  CLIP GPU move failed ({gpu_err}), falling back to CPU"
                    )
                    self._clip_model = self._clip_model.to("cpu")
                    device = "cpu"
                else:
                    raise

            self._clip_model.eval()
            self._clip_model_name = model_name

            load_time = time.time() - start_time
            self._load_times["clip"] = load_time
            self._loading_errors.pop("clip", None)
            logger.success(f"✅ [ModelManager] CLIP loaded in {load_time:.1f}s (device={device})")

        except Exception as e:
            error_msg = f"Failed to load CLIP model: {e}"
            logger.error(f"❌ [ModelManager] {error_msg}")
            self._loading_errors["clip"] = error_msg
            raise

        return self._clip_model, self._clip_processor

    # ========================================================================
    # PRE-LOADING
    # ========================================================================

    def preload_all(
        self,
        models: Optional[List[str]] = None,
        parallel: bool = True,
    ) -> Dict[str, bool]:
        """
        Pre-load models at startup.

        Args:
            models: List of model names to load.
                    Options: ['whisper', 'sentence_transformer', 'clip']
                    If None, loads whisper + sentence_transformer + clip
            parallel: Load models in parallel threads
        """
        if models is None:
            models = ["whisper", "sentence_transformer", "clip"]

        logger.info(f"🚀 [ModelManager] Pre-loading {len(models)} models...")
        results: Dict[str, bool] = {}
        start_time = time.time()

        loader_map = {
            "whisper": self.get_whisper,
            "sentence_transformer": self.get_sentence_transformer,
            "clip": self.get_clip_model,
        }

        if parallel and len(models) > 1:
            with ThreadPoolExecutor(max_workers=len(models)) as executor:
                future_to_model = {
                    executor.submit(loader_map[m]): m
                    for m in models
                    if m in loader_map
                }
                for future in as_completed(future_to_model):
                    name = future_to_model[future]
                    try:
                        future.result()
                        results[name] = True
                        logger.success(f"  ✓ {name} loaded")
                    except Exception as e:
                        results[name] = False
                        logger.error(f"  ✗ {name} failed: {e}")
        else:
            for name in models:
                if name not in loader_map:
                    continue
                try:
                    loader_map[name]()
                    results[name] = True
                    logger.success(f"  ✓ {name} loaded")
                except Exception as e:
                    results[name] = False
                    logger.error(f"  ✗ {name} failed: {e}")

        total_time = time.time() - start_time
        successful = sum(1 for v in results.values() if v)
        logger.success(
            f"✅ [ModelManager] Pre-loading complete: {successful}/{len(models)} models "
            f"in {total_time:.1f}s"
        )

        self._models_preloaded = True
        return results

    # ========================================================================
    # CLEANUP & STATUS
    # ========================================================================

    def cleanup_all(self):
        """Release all loaded models and free memory."""
        logger.info("🧹 [ModelManager] Cleaning up all models...")

        self._whisper_model = None
        self._sentence_transformer = None
        self._sentence_transformer_name = None
        self._clip_model = None
        self._clip_processor = None
        self._clip_model_name = None
        self._loading_errors.clear()
        self._load_times.clear()
        self._models_preloaded = False

        import gc
        gc.collect()

        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        except ImportError:
            pass

        logger.success("✅ [ModelManager] All models cleaned up")

    def get_status(self) -> Dict[str, Any]:
        """Get status of all managed models."""
        return {
            "device": self._device,
            "models_preloaded": self._models_preloaded,
            "whisper_loaded": self._whisper_model is not None,
            "sentence_transformer_loaded": self._sentence_transformer is not None,
            "sentence_transformer_model": self._sentence_transformer_name,
            "clip_loaded": self._clip_model is not None,
            "clip_model": self._clip_model_name,
            "loading_errors": self._loading_errors,
            "load_times": self._load_times,
        }


# ============================================================================
# STARTUP HELPER
# ============================================================================

def setup_model_preloading(models: Optional[List[str]] = None):
    """
    Pre-load models in a background thread at startup.
    Call this from main.py or asgi.py startup event.
    """
    def _preload_task():
        try:
            manager = ModelManager.get_instance()
            models_to_load = models or ["sentence_transformer", "clip"]
            manager.preload_all(models=models_to_load, parallel=True)
        except Exception as e:
            logger.error(f"❌ [ModelManager] Background pre-loading failed: {e}")

    thread = threading.Thread(target=_preload_task, daemon=True, name="ModelPreloader")
    thread.start()
    logger.info("🚀 [ModelManager] Background pre-loading started")
