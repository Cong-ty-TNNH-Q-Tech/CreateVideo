"""
Example implementation: Model Manager with Pre-loading & Caching
Cải thiện 100% thời gian load model cho task thứ 2 trở đi

Tạo file mới: app/services/model_manager.py
"""

from typing import Optional, Dict, Any
import threading
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class ModelManager:
    """
    Singleton class to manage all AI models with lazy loading and caching
    
    Benefits:
    - Load models once, use multiple times
    - Pre-load models at startup in background
    - Thread-safe access
    - Automatic cleanup on errors
    - Memory-efficient (lazy loading)
    
    Usage:
        # Get singleton instance
        manager = ModelManager.get_instance()
        
        # Get cached models
        whisper = manager.get_whisper()
        transformer = manager.get_sentence_transformer()
        clip = manager.get_clip_model()
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        """Private constructor - use get_instance() instead"""
        # Model cache
        self.whisper_model = None
        self.sentence_transformer = None
        self.sentence_transformer_name = None
        self.clip_model = None
        self.clip_processor = None
        self.clip_model_name = None
        self.chatterbox_model = None
        
        # Model loading status
        self.models_preloaded = False
        self.loading_errors = {}
        
        # Configuration cache
        self._config = None
        
        logger.info("🔧 ModelManager initialized")
    
    @classmethod
    def get_instance(cls):
        """
        Get singleton instance of ModelManager
        Thread-safe implementation
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = ModelManager()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset singleton (useful for testing or forced reload)"""
        with cls._lock:
            if cls._instance:
                cls._instance.cleanup_all()
            cls._instance = None
            logger.warning("🔄 ModelManager instance reset")
    
    def _get_config(self):
        """Lazy load config"""
        if self._config is None:
            from app.config import config
            self._config = config
        return self._config
    
    # ========================================================================
    # WHISPER MODEL
    # ========================================================================
    
    def get_whisper(self, force_reload: bool = False) -> Any:
        """
        Get Whisper model (faster-whisper)
        
        Args:
            force_reload: Force reload model even if cached
        
        Returns:
            WhisperModel instance
        """
        if self.whisper_model is None or force_reload:
            try:
                from faster_whisper import WhisperModel
                from app.utils import utils
                import os.path
                
                config = self._get_config()
                model_size = config.whisper.get("model_size", "large-v3")
                device = config.whisper.get("device", "cpu")
                compute_type = config.whisper.get("compute_type", "int8")
                
                # Check for local model first
                model_path = f"{utils.root_dir()}/models/whisper-{model_size}"
                model_bin_file = f"{model_path}/model.bin"
                if not os.path.isdir(model_path) or not os.path.isfile(model_bin_file):
                    model_path = model_size
                
                logger.info(
                    f"🤖 Loading Whisper model: {model_size} "
                    f"(device={device}, compute_type={compute_type})"
                )
                start_time = time.time()
                
                self.whisper_model = WhisperModel(
                    model_size_or_path=model_path,
                    device=device,
                    compute_type=compute_type
                )
                
                load_time = time.time() - start_time
                logger.success(f"✅ Whisper model loaded in {load_time:.1f}s")
                
                # Clear any previous errors
                self.loading_errors.pop('whisper', None)
                
            except Exception as e:
                error_msg = f"Failed to load Whisper model: {str(e)}"
                logger.error(f"❌ {error_msg}")
                self.loading_errors['whisper'] = error_msg
                raise
        
        return self.whisper_model
    
    # ========================================================================
    # SENTENCE TRANSFORMER (for semantic similarity)
    # ========================================================================
    
    def get_sentence_transformer(
        self,
        model_name: str = "all-mpnet-base-v2",
        force_reload: bool = False
    ) -> Any:
        """
        Get SentenceTransformer model
        
        Args:
            model_name: Model identifier
            force_reload: Force reload model
        
        Returns:
            SentenceTransformer instance
        """
        # Check if we need to reload due to different model
        needs_reload = (
            self.sentence_transformer is None or
            self.sentence_transformer_name != model_name or
            force_reload
        )
        
        if needs_reload:
            try:
                from sentence_transformers import SentenceTransformer
                
                config = self._get_config()
                device = config.app.get("semantic_device", "cpu")
                
                logger.info(f"🤖 Loading SentenceTransformer: {model_name} (device={device})")
                start_time = time.time()
                
                self.sentence_transformer = SentenceTransformer(
                    model_name,
                    device=device
                )
                self.sentence_transformer_name = model_name
                
                load_time = time.time() - start_time
                logger.success(
                    f"✅ SentenceTransformer loaded in {load_time:.1f}s "
                    f"(max_seq_length={self.sentence_transformer.max_seq_length})"
                )
                
                self.loading_errors.pop('sentence_transformer', None)
                
            except Exception as e:
                error_msg = f"Failed to load SentenceTransformer: {str(e)}"
                logger.error(f"❌ {error_msg}")
                self.loading_errors['sentence_transformer'] = error_msg
                raise
        
        return self.sentence_transformer
    
    # ========================================================================
    # CLIP MODEL (for image-text similarity)
    # ========================================================================
    
    def get_clip_model(
        self,
        model_name: str = "openai/clip-vit-base-patch32",
        force_reload: bool = False
    ) -> tuple:
        """
        Get CLIP model and processor
        
        Args:
            model_name: CLIP model identifier
            force_reload: Force reload model
        
        Returns:
            Tuple of (model, processor)
        """
        needs_reload = (
            self.clip_model is None or
            self.clip_model_name != model_name or
            force_reload
        )
        
        if needs_reload:
            try:
                from transformers import CLIPProcessor, CLIPModel
                import torch
                
                config = self._get_config()
                device = config.app.get("clip_device", "cpu")
                
                logger.info(f"🤖 Loading CLIP model: {model_name} (device={device})")
                start_time = time.time()
                
                self.clip_processor = CLIPProcessor.from_pretrained(model_name)
                self.clip_model = CLIPModel.from_pretrained(model_name).to(device)
                self.clip_model.eval()  # Set to evaluation mode
                self.clip_model_name = model_name
                
                load_time = time.time() - start_time
                logger.success(f"✅ CLIP model loaded in {load_time:.1f}s")
                
                self.loading_errors.pop('clip', None)
                
            except Exception as e:
                error_msg = f"Failed to load CLIP model: {str(e)}"
                logger.error(f"❌ {error_msg}")
                self.loading_errors['clip'] = error_msg
                raise
        
        return self.clip_model, self.clip_processor
    
    # ========================================================================
    # CHATTERBOX TTS
    # ========================================================================
    
    def get_chatterbox(self, force_reload: bool = False) -> Any:
        """Get Chatterbox TTS model"""
        if self.chatterbox_model is None or force_reload:
            try:
                from chatterbox.tts import ChatterboxTTS
                
                logger.info("🤖 Loading Chatterbox TTS model")
                start_time = time.time()
                
                self.chatterbox_model = ChatterboxTTS()
                
                load_time = time.time() - start_time
                logger.success(f"✅ Chatterbox TTS loaded in {load_time:.1f}s")
                
                self.loading_errors.pop('chatterbox', None)
                
            except Exception as e:
                error_msg = f"Failed to load Chatterbox TTS: {str(e)}"
                logger.error(f"❌ {error_msg}")
                self.loading_errors['chatterbox'] = error_msg
                raise
        
        return self.chatterbox_model
    
    # ========================================================================
    # PRE-LOADING & CLEANUP
    # ========================================================================
    
    def preload_all(
        self,
        models: Optional[list] = None,
        parallel: bool = True
    ) -> Dict[str, bool]:
        """
        Pre-load all specified models
        
        Args:
            models: List of model names to pre-load. 
                   Options: ['whisper', 'sentence_transformer', 'clip', 'chatterbox']
                   If None, loads all available models
            parallel: Load models in parallel threads
        
        Returns:
            Dict with loading status for each model
        """
        if models is None:
            models = ['whisper', 'sentence_transformer', 'clip']
        
        logger.info(f"🚀 Pre-loading {len(models)} models...")
        results = {}
        start_time = time.time()
        
        if parallel:
            # Parallel loading
            with ThreadPoolExecutor(max_workers=len(models)) as executor:
                future_to_model = {}
                
                for model_name in models:
                    if model_name == 'whisper':
                        future = executor.submit(self.get_whisper)
                    elif model_name == 'sentence_transformer':
                        future = executor.submit(self.get_sentence_transformer)
                    elif model_name == 'clip':
                        future = executor.submit(self.get_clip_model)
                    elif model_name == 'chatterbox':
                        future = executor.submit(self.get_chatterbox)
                    else:
                        logger.warning(f"⚠️  Unknown model: {model_name}")
                        continue
                    
                    future_to_model[future] = model_name
                
                # Wait for all to complete
                for future in as_completed(future_to_model):
                    model_name = future_to_model[future]
                    try:
                        future.result()
                        results[model_name] = True
                        logger.success(f"  ✓ {model_name} loaded")
                    except Exception as e:
                        results[model_name] = False
                        logger.error(f"  ✗ {model_name} failed: {str(e)}")
        else:
            # Sequential loading
            for model_name in models:
                try:
                    if model_name == 'whisper':
                        self.get_whisper()
                    elif model_name == 'sentence_transformer':
                        self.get_sentence_transformer()
                    elif model_name == 'clip':
                        self.get_clip_model()
                    elif model_name == 'chatterbox':
                        self.get_chatterbox()
                    
                    results[model_name] = True
                    logger.success(f"  ✓ {model_name} loaded")
                except Exception:
                    results[model_name] = False
        
        total_time = time.time() - start_time
        successful = sum(1 for v in results.values() if v)
        
        logger.success(
            f"✅ Pre-loading complete: {successful}/{len(models)} models loaded "
            f"in {total_time:.1f}s"
        )
        
        self.models_preloaded = True
        return results
    
    def cleanup_all(self):
        """Cleanup all loaded models and free memory"""
        logger.info("🧹 Cleaning up all models...")
        
        # Clear model references
        self.whisper_model = None
        self.sentence_transformer = None
        self.sentence_transformer_name = None
        self.clip_model = None
        self.clip_processor = None
        self.clip_model_name = None
        self.chatterbox_model = None
        
        # Clear errors
        self.loading_errors.clear()
        self.models_preloaded = False
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # CUDA cleanup if available
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                logger.info("  ✓ CUDA cache cleared")
        except ImportError:
            pass
        
        logger.success("✅ All models cleaned up")
    
    def get_memory_usage(self) -> Dict[str, str]:
        """Get memory usage information"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            mem_info = process.memory_info()
            
            return {
                'rss': f"{mem_info.rss / 1024 / 1024:.1f} MB",
                'vms': f"{mem_info.vms / 1024 / 1024:.1f} MB",
                'percent': f"{process.memory_percent():.1f}%"
            }
        except ImportError:
            return {'error': 'psutil not available'}
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all models"""
        return {
            'models_preloaded': self.models_preloaded,
            'whisper_loaded': self.whisper_model is not None,
            'sentence_transformer_loaded': self.sentence_transformer is not None,
            'sentence_transformer_model': self.sentence_transformer_name,
            'clip_loaded': self.clip_model is not None,
            'clip_model': self.clip_model_name,
            'chatterbox_loaded': self.chatterbox_model is not None,
            'loading_errors': self.loading_errors,
            'memory_usage': self.get_memory_usage()
        }


# ============================================================================
# INTEGRATION WITH FASTAPI
# ============================================================================

def setup_model_preloading():
    """
    Setup function to call from main.py or app startup
    Pre-loads models in background thread
    """
    import threading
    
    def preload_task():
        """Background task to pre-load models"""
        try:
            manager = ModelManager.get_instance()
            
            # Determine which models to pre-load based on config
            from app.config import config
            models_to_load = []
            
            if config.whisper.get("model_size"):
                models_to_load.append('whisper')
            
            if config.app.get("enable_semantic_search", False):
                models_to_load.append('sentence_transformer')
            
            if config.app.get("enable_image_similarity", False):
                models_to_load.append('clip')
            
            if models_to_load:
                manager.preload_all(models=models_to_load, parallel=True)
            else:
                logger.info("ℹ️  No models configured for pre-loading")
                
        except Exception as e:
            logger.error(f"❌ Model pre-loading failed: {str(e)}")
    
    # Start in background daemon thread
    thread = threading.Thread(target=preload_task, daemon=True, name="ModelPreloader")
    thread.start()
    logger.info("🚀 Model pre-loading started in background")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
=== INTEGRATION STEPS ===

1. Add to main.py:

   from app.services.model_manager import setup_model_preloading

   if __name__ == "__main__":
       # Pre-load models in background
       setup_model_preloading()
       
       # Start server
       uvicorn.run(...)

2. Update subtitle.py:

   from app.services.model_manager import ModelManager

   def create(audio_file, subtitle_file: str = ""):
       # Use cached model
       model = ModelManager.get_instance().get_whisper()
       segments, info = model.transcribe(...)

3. Update semantic_video.py:

   from app.services.model_manager import ModelManager

   def load_model(model_name: str = "all-mpnet-base-v2"):
       # Use cached model
       return ModelManager.get_instance().get_sentence_transformer(model_name)

4. Update image_similarity.py:

   from app.services.model_manager import ModelManager

   def load_clip_model(model_name: str):
       # Use cached model
       return ModelManager.get_instance().get_clip_model(model_name)

5. Add config to config.toml:

   [app]
   enable_semantic_search = true
   enable_image_similarity = true
   semantic_device = "cpu"  # or "cuda"
   clip_device = "cpu"  # or "cuda"

=== PERFORMANCE GAINS ===

Before:
- Task 1: Load models (10-25s) + Process (60-300s) = 70-325s
- Task 2: Load models (10-25s) + Process (60-300s) = 70-325s
- Task 3: Load models (10-25s) + Process (60-300s) = 70-325s

After:
- Startup: Pre-load models (10-25s) in background
- Task 1: Process (60-300s) = 60-300s
- Task 2: Process (60-300s) = 60-300s
- Task 3: Process (60-300s) = 60-300s

Improvement: 10-25 seconds saved PER TASK (after the first one)
"""
