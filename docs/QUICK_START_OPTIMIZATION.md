# 🚀 Quick Start: Tối Ưu Hiệu Suất Ngay Lập Tức

## 🎯 Top 3 Cải Thiện Quan Trọng Nhất

### 1️⃣ Parallel Video Downloads (60-80% faster) ⚡

**Thời gian triển khai:** 10 phút  
**Cải thiện:** 20-120 giây → 5-30 giây

**Bước 1:** Mở file [app/services/material.py](../app/services/material.py)

**Bước 2:** Thêm import ở đầu file:
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
```

**Bước 3:** Thay thế code trong function `download_videos()`, tìm đoạn:
```python
# ❌ OLD CODE (sequential)
for item in valid_video_items:
    try:
        logger.info(f"downloading video: {item.url}")
        item_search_term = getattr(item, 'search_term', 'unknown')
        saved_video_path = save_video(
            video_url=item.url, save_dir=material_directory, 
            search_term=item_search_term, thumbnail_url=item.thumbnail_url, 
            preview_images=item.preview_images
        )
        # ... rest of code
```

**Bước 4:** Thay bằng code mới (parallel):
```python
# ✅ NEW CODE (parallel)
def download_single_video(item):
    """Helper function for parallel downloads"""
    try:
        item_search_term = getattr(item, 'search_term', 'unknown')
        saved_video_path = save_video(
            video_url=item.url, save_dir=material_directory,
            search_term=item_search_term, thumbnail_url=item.thumbnail_url,
            preview_images=item.preview_images
        )
        if saved_video_path:
            return {
                'path': saved_video_path,
                'url': item.url,
                'duration': min(max_clip_duration, item.duration),
                'search_term': item_search_term
            }
    except Exception as e:
        logger.error(f"failed to download video: {item.url} => {str(e)}")
    return None

# Parallel download với ThreadPoolExecutor
max_workers = 5  # Download 5 videos cùng lúc
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_item = {
        executor.submit(download_single_video, item): item 
        for item in valid_video_items
    }
    
    for future in as_completed(future_to_item):
        if total_duration > audio_duration:
            logger.info("✓ Đã đủ video, stopping downloads...")
            break
            
        result = future.result()
        if result and result['url'] not in downloaded_urls:
            video_paths.append(result['path'])
            downloaded_urls.add(result['url'])
            total_duration += result['duration']
            logger.info(f"✓ {len(video_paths)} videos ({total_duration:.1f}s/{audio_duration:.1f}s)")
```

**Xem code đầy đủ:** [docs/examples/parallel_downloads.py](examples/parallel_downloads.py)

---

### 2️⃣ Model Pre-loading & Caching (100% faster cho task 2+) 🧠

**Thời gian triển khai:** 20 phút  
**Cải thiện:** Task 2+ không cần load model lại (tiết kiệm 10-25 giây)

**Bước 1:** Tạo file mới `app/services/model_manager.py`

Copy toàn bộ code từ: [docs/examples/model_manager.py](examples/model_manager.py)

**Bước 2:** Cập nhật [main.py](../main.py):
```python
from app.services.model_manager import setup_model_preloading

if __name__ == "__main__":
    # 🚀 Pre-load models trong background
    setup_model_preloading()
    
    logger.info("start server...")
    uvicorn.run(...)
```

**Bước 3:** Cập nhật [app/services/subtitle.py](../app/services/subtitle.py):

Tìm:
```python
def create(audio_file, subtitle_file: str = ""):
    global model
    if not model:
        # Old: Load model mỗi lần
        model = WhisperModel(...)
```

Thay bằng:
```python
def create(audio_file, subtitle_file: str = ""):
    # ✅ New: Use cached model
    from app.services.model_manager import ModelManager
    model = ModelManager.get_instance().get_whisper()
```

**Bước 4:** Cập nhật [app/services/semantic_video.py](../app/services/semantic_video.py):

Tìm:
```python
def load_model(model_name: str = "all-mpnet-base-v2"):
    global _model, _model_name
    if _model is None or _model_name != model_name:
        _model = SentenceTransformer(model_name, device='cpu')
```

Thay bằng:
```python
def load_model(model_name: str = "all-mpnet-base-v2"):
    # ✅ New: Use cached model
    from app.services.model_manager import ModelManager
    return ModelManager.get_instance().get_sentence_transformer(model_name)
```

---

### 3️⃣ Tối Ưu Semantic Similarity (50-70% faster) 🔍

**Thời gian triển khai:** 5 phút  
**Cải thiện:** 30 giây → 5-10 giây

**Bước 1:** Mở [app/services/image_similarity.py](../app/services/image_similarity.py)

**Bước 2:** Tìm và thay đổi các constants:
```python
# ❌ OLD (slow)
INFERENCE_DELAY = 0.15
MAX_BATCH_SIZE = 10

# ✅ NEW (fast)
INFERENCE_DELAY = 0.05  # Giảm delay từ 150ms → 50ms
MAX_BATCH_SIZE = 50     # Tăng batch size từ 10 → 50
```

**Bước 3:** Tìm dòng:
```python
_force_cpu_only = True  # Force CPU-only mode
```

Nếu bạn có **NVIDIA GPU**, thay bằng:
```python
_force_cpu_only = False  # Allow GPU usage
```

---

## 📊 Kết Quả Mong Đợi

### Trước khi tối ưu:
```
🔹 Generate Script:     10 giây
🔹 Generate Terms:      5 giây
🔹 Generate Audio:      15 giây
🔹 Download Videos:     90 giây ⚠️  (SLOW)
🔹 Semantic Match:      30 giây ⚠️  (SLOW)
🔹 Generate Subtitle:   20 giây (+ 10s load model)
🔹 Combine Videos:      40 giây
━━━━━━━━━━━━━━━━━━━━━━━━━━━
   TỔNG:               220 giây (3.7 phút)
```

### Sau khi tối ưu (3 cải thiện trên):
```
🔹 Generate Script:     10 giây
🔹 Generate Terms:      5 giây
🔹 Generate Audio:      15 giây
🔹 Download Videos:     20 giây ✅ (60-80% faster)
🔹 Semantic Match:      8 giây  ✅ (70% faster)
🔹 Generate Subtitle:   20 giây (no load time!) ✅
🔹 Combine Videos:      40 giây
━━━━━━━━━━━━━━━━━━━━━━━━━━━
   TỔNG:               118 giây (2.0 phút)

🚀 CẢI THIỆN: 46% NHANH HƠN!
```

---

## 🧪 Test & Verify

### 1. Test parallel downloads:
```bash
# Chạy WebUI hoặc API
python main.py

# Tạo 1 video và xem logs
# Tìm dòng:
# "🚀 Speedup: X.X× faster than sequential"
```

### 2. Test model caching:
```bash
# Task 1: Sẽ thấy "Loading Whisper model..."
# Task 2: KHÔNG thấy "Loading..." nữa - model đã cached!
```

### 3. Kiểm tra memory:
```python
from app.services.model_manager import ModelManager
status = ModelManager.get_instance().get_status()
print(status)
```

---

## 🎛️ Cấu Hình Nâng Cao (Optional)

### Config file: [config.toml](../config.example.toml)

```toml
[app]
# Parallel downloads
max_download_workers = 5  # 5-10 recommended (càng cao càng nhanh nhưng tốn RAM)

# Semantic search
enable_semantic_search = true
semantic_device = "cuda"  # or "cpu" (CUDA = 4-5× faster)

# Image similarity
enable_image_similarity = true
image_similarity_model = "clip-vit-base-patch32"
clip_device = "cuda"  # or "cpu"

[whisper]
model_size = "base"  # "tiny/base/small/medium/large-v3"
device = "cuda"      # or "cpu" (CUDA = 5-10× faster)
compute_type = "float16"  # or "int8" cho CPU
```

### Lựa chọn Whisper model size:
- **tiny** - Nhanh nhất, độ chính xác thấp (1-2 giây)
- **base** - Balance tốt (3-5 giây) ✅ Recommended
- **small** - Chính xác hơn (5-8 giây)
- **medium** - Rất chính xác (10-15 giây)
- **large-v3** - Tốt nhất, chậm nhất (20-60 giây)

---

## 🐛 Troubleshooting

### Lỗi: "CUDA out of memory"
**Giải pháp:**
```toml
# config.toml
[whisper]
device = "cpu"  # Fallback về CPU

[app]
semantic_device = "cpu"
clip_device = "cpu"
```

### Lỗi: "Too many open files"
**Giải pháp:** Giảm số workers:
```python
max_workers = 3  # Thay vì 5-10
```

### Downloads vẫn chậm
**Nguyên nhân:** Network slow hoặc proxy issues  
**Giải pháp:**
```toml
[proxy]
http = ""   # Thử disable proxy
https = ""
```

### Model loading failed
**Giải pháp:** Download model manually:
```bash
# Whisper
mkdir -p models
cd models
# Download từ: https://huggingface.co/Systran/faster-whisper-base

# SentenceTransformer
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-mpnet-base-v2')"
```

---

## 📖 Tài Liệu Đầy Đủ

- 📄 [Performance Optimization Guide](PERFORMANCE_OPTIMIZATION.md) - Chi tiết đầy đủ
- 💻 [Parallel Downloads Example](examples/parallel_downloads.py) - Code mẫu
- 🧠 [Model Manager Example](examples/model_manager.py) - Code mẫu

---

## ✅ Checklist

- [ ] Implement parallel downloads → Test → Verify speedup
- [ ] Add model_manager.py → Update services → Test caching
- [ ] Optimize semantic similarity settings
- [ ] (Optional) Enable GPU acceleration
- [ ] (Optional) Add smart caching layer
- [ ] Measure & compare before/after performance
- [ ] Update config.toml với settings phù hợp
- [ ] Document changes trong README

---

**Chúc bạn tối ưu thành công! 🚀**

Nếu có vấn đề, check logs hoặc mở issue trên GitHub.
