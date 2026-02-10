# Video Quality Optimization Guide

Hướng dẫn tối ưu chất lượng video: giảm video lặp và tăng độ liên quan giữa video và nội dung.

## 🎯 Vấn Đề Thường Gặp

### 1. Video không liên quan với nội dung
**Triệu chứng:**
- Video về "mèo" xuất hiện khi đang nói về "chó"
- Video cảnh biển khi đang nói về núi
- Video không khớp với context của câu nói

**Nguyên nhân:**
- Search terms không tốt
- Similarity threshold quá thấp
- Search pool quá nhỏ
- Không dùng semantic matching

### 2. Video bị lặp nhiều lần
**Triệu chứng:**
- Cùng 1 video xuất hiện 2-3 lần trong video
- Số lượng video unique quá ít
- Thiếu diversity

**Nguyên nhân:**
- `max_video_reuse` quá cao
- Pool video quá nhỏ
- `diversity_threshold` chưa đủ
- Video source không đủ video

---

## 🔧 Giải Pháp Chi Tiết

### A. Cấu Hình Tối Ưu Cho Semantic Mode

#### 1. **Tăng Similarity Threshold** ⭐⭐⭐⭐⭐

```
Similarity Threshold: 0.65 - 0.75
```

**Giải thích:**
- `0.5` (mặc định) → Chấp nhận video "hơi liên quan"
- `0.65` → Yêu cầu video "khá liên quan" ✅ **KHUYẾN NGHỊ**
- `0.75` → Chỉ chấp nhận video "rất liên quan" (có thể không đủ video)

**Trade-off:**
- ⬆️ Tăng = Video liên quan hơn, nhưng cần nhiều video hơn
- ⬇️ Giảm = Dễ tìm video, nhưng có thể không liên quan

#### 2. **Tăng Search Pool Size** ⭐⭐⭐⭐⭐

```
Search Pool Size: 100 - 150
```

**Giải thích:**
- `50` (mặc định) → Chỉ có 50 video để chọn
- `100` → Có 100 video để chọn ✅ **KHUYẾN NGHỊ**
- `150` → Có 150 video (tốt cho video dài)

**Lưu ý:**
- Càng nhiều càng tốt, nhưng tải chậm hơn
- Tối thiểu: `audio_duration / max_clip_duration * 1.5`

#### 3. **Giảm Max Video Reuse** ⭐⭐⭐⭐⭐

```
Max Video Reuse: 1
```

**Giải thích:**
- `1` → **Không bao giờ lặp video** ✅ **KHUYẾN NGHỊ CHO VIDEO NGẮN**
- `2` → Cho phép lặp 1 lần (cho video dài)

**Khi nào dùng `2`:**
- Video dài (> 2 phút)
- Search pool nhỏ (< 50 video)
- Ít search terms (< 3 terms)

#### 4. **Tăng Diversity Threshold** ⭐⭐⭐⭐

```
Video Diversity Threshold: 8 - 10
```

**Giải thích:**
- `5` (mặc định) → Phải cách 5 clips mới dùng lại
- `8-10` → Phải cách 8-10 clips ✅ **KHUYẾN NGHỊ**

**Công thức:**
```
diversity_threshold ≥ total_clips / max_video_reuse / 2
```

#### 5. **Chọn Segmentation Method** ⭐⭐⭐

```
Split by Paragraphs (cho script có đoạn văn rõ ràng)
```

**So sánh:**
| Method | Phù hợp | Ưu điểm | Nhược điểm |
|--------|---------|---------|-----------|
| **Sentences** | Script ngắn | Segments nhiều | Khó match (quá ngắn) |
| **Paragraphs** | Script dài | Segments có ngữ cảnh | Ít segments hơn |

**Khuyến nghị:**
- Script < 500 words → Sentences
- Script > 500 words → Paragraphs ✅

#### 6. **Tăng Minimum Segment Length** ⭐⭐⭐

```
Minimum Segment Length: 35 - 50 characters
```

**Giải thích:**
- `25` → Segments rất ngắn → khó match
- `35-50` → Segments có đủ context ✅
- `> 60` → Quá dài → ít segments

#### 7. **Enable Image Similarity** ⭐⭐⭐⭐

```
✅ Enable Image Similarity
Image Similarity Threshold: 0.65 - 0.75
```

**Giải thích:**
- So sánh thêm **hình ảnh** video với text
- Tăng accuracy lên 20-30%
- **Lưu ý:** Cần cài `transformers`, `torch`, `pillow`

**Model options:**
- `CLIP ViT-B/32` → Nhanh, accuracy tốt ✅ **KHUYẾN NGHỊ**
- `CLIP ViT-B/16` → Chậm hơn, accuracy cao hơn
- `CLIP ViT-L/14` → Rất chậm, accuracy cao nhất

---

### B. Optimize Search Terms ⭐⭐⭐⭐⭐

**Video quality 80% phụ thuộc vào search terms!**

#### Bad Search Terms ❌
```
"success, motivation, money, business, entrepreneur"
```
→ Quá chung chung, không specific

#### Good Search Terms ✅
```
"person climbing mountain, startup team meeting, dollar bills flying, 
handshake business deal, man typing laptop coffee shop"
```
→ Cụ thể, visual, mô tả hành động

#### Tips cho LLM Generate Better Terms:

**Cập nhật prompt:**
```markdown
Generate 8-10 VISUAL and SPECIFIC search terms for video footage.

Good terms describe:
- Specific actions (e.g., "person running on beach" not "exercise")
- Visual scenes (e.g., "sunset over ocean" not "beautiful nature")
- Concrete objects (e.g., "red sports car driving" not "luxury")

Bad: success, motivation, money
Good: businessman shaking hands, entrepreneur presenting to investors, money falling from sky
```

---

### C. Cấu Hình Cho Từng Loại Video

#### 📱 **Short Video (< 60s)**

```yaml
Video Concat Mode: Semantic Text Alignment
Search Pool Size: 80-100
Similarity Threshold: 0.70
Max Video Reuse: 1 ⭐
Diversity Threshold: 8
Segmentation: Sentences
Min Segment Length: 30

Enable Image Similarity: Yes
Image Threshold: 0.70
```

**Kết quả:**
- ✅ Không bao giờ lặp video
- ✅ Video rất liên quan
- ✅ Diversity cao

#### 🎬 **Long Video (1-3 mins)**

```yaml
Video Concat Mode: Semantic Text Alignment  
Search Pool Size: 120-150
Similarity Threshold: 0.65
Max Video Reuse: 2
Diversity Threshold: 10
Segmentation: Paragraphs
Min Segment Length: 40

Enable Image Similarity: Yes
Image Threshold: 0.65
```

**Kết quả:**
- ✅ Có thể lặp nhưng cách xa
- ✅ Video liên quan tốt
- ⚠️ Cần search pool lớn

#### 🎥 **Very Long Video (> 3 mins)**

```yaml
Video Concat Mode: Semantic Text Alignment
Search Pool Size: 150-200
Similarity Threshold: 0.60
Max Video Reuse: 2-3
Diversity Threshold: 12
Segmentation: Paragraphs
Min Segment Length: 50

Enable Image Similarity: Yes  
Image Threshold: 0.60
```

**Lưu ý:**
- Cần **nhiều search terms** (10-15 terms)
- Tăng `search_pool_size` để có đủ video
- Có thể giảm thresholds để đảm bảo đủ video

---

## 📐 Công Thức Tính Toán

### 1. Search Pool Size Tối Thiểu

```python
min_search_pool = (audio_duration / max_clip_duration) * 1.5 * max_video_reuse
```

**Ví dụ:**
- Audio: 60s
- Clip: 5s
- Max reuse: 1

```python
min_pool = (60 / 5) * 1.5 * 1 = 18 videos
Khuyến nghị: 18 * 3 = 54 videos minimum
Tốt nhất: 100 videos
```

### 2. Diversity Threshold Optimal

```python
diversity_threshold = (total_clips / max_video_reuse) / 2
```

**Ví dụ:**
- Total clips: 12
- Max reuse: 1

```python
diversity_threshold = (12 / 1) / 2 = 6
Khuyến nghị: 8-10 (cao hơn công thức)
```

### 3. Number of Search Terms

```python
min_terms = ceil(audio_duration / 10)
```

**Ví dụ:**
- Audio: 60s → minimum 6 terms
- Audio: 120s → minimum 12 terms

---

## 🎯 Quick Config Templates

### Template 1: **Maximum Quality (No Duplicates)** ⭐⭐⭐⭐⭐

```yaml
# Settings trong WebUI
Video Concat Mode: Semantic Text Alignment

# Semantic Settings
Segmentation: Paragraphs
Min Segment Length: 40
Similarity Threshold: 0.70
Diversity Threshold: 10
Max Video Reuse: 1 🔥
Search Pool Size: 120

# Image Similarity  
Enable: Yes
Threshold: 0.70
Model: CLIP ViT-B/32
```

**Phù hợp:** Video ngắn, yêu cầu quality cao

**Kết quả:**
- ✅ KHÔNG BAO GIỜ LẶP VIDEO
- ✅ Video rất liên quan
- ⏱️ Có thể chậm (do search pool lớn)

---

### Template 2: **Balanced (Recommended)** ⭐⭐⭐⭐

```yaml
Video Concat Mode: Semantic Text Alignment

# Semantic Settings
Segmentation: Sentences
Min Segment Length: 35
Similarity Threshold: 0.65
Diversity Threshold: 8
Max Video Reuse: 1
Search Pool Size: 100

# Image Similarity
Enable: Yes
Threshold: 0.65
Model: CLIP ViT-B/32
```

**Phù hợp:** Hầu hết video, balance giữa quality và speed

**Kết quả:**
- ✅ Không lặp
- ✅ Video liên quan tốt
- ⚡ Tốc độ OK

---

### Template 3: **Fast (For Long Videos)** ⭐⭐⭐

```yaml
Video Concat Mode: Semantic Text Alignment

# Semantic Settings
Segmentation: Paragraphs
Min Segment Length: 30
Similarity Threshold: 0.60
Diversity Threshold: 8
Max Video Reuse: 2
Search Pool Size: 80

# Image Similarity
Enable: No (hoặc Yes nếu có GPU)
```

**Phù hợp:** Video dài (> 2 mins), cần tạo nhanh

**Kết quả:**
- ⚠️ Có thể lặp 1 lần (cách xa nhau)
- ✅ Video liên quan khá tốt
- ⚡⚡ Nhanh

---

## 🐛 Troubleshooting

### Issue 1: "No suitable video found - all videos may be overused"

**Nguyên nhân:**
- Search pool quá nhỏ
- Max video reuse = 1 nhưng không đủ video
- Similarity threshold quá cao

**Giải pháp:**
1. ⬆️ Tăng `search_pool_size` to 150-200
2. ⬆️ Tăng `max_video_reuse` to 2
3. ⬇️ Giảm `similarity_threshold` to 0.55

---

### Issue 2: Video vẫn lặp dù set max_video_reuse = 1

**Nguyên nhân:**
- Đang ở mode "Random" thay vì "Semantic"
- Multiple videos generation (tự động fallback to Random)

**Check:**
```python
# Xem logs:
"🎯 Using Semantic Video Matching" → Semantic mode ✅
"Using random video selection" → Random mode ❌
```

**Giải pháp:**
1. Đảm bảo chọn **"Semantic Text Alignment"**
2. Nếu gen nhiều videos cùng lúc → chuyển về 1 video

---

### Issue 3: Video không liên quan dù similarity cao

**Nguyên nhân:**
- Search terms không tốt
- Text similarity cao nhưng không visual match

**Giải pháp:**
1. ✅ **Enable Image Similarity** (quan trọng!)
2. Viết lại search terms cụ thể hơn
3. Increase image similarity threshold to 0.70

---

### Issue 4: Quá chậm

**Nguyên nhân:**
- Search pool quá lớn
- Image similarity enabled với model lớn

**Giải pháp:**
1. Giảm `search_pool_size` xuống 60-80
2. Dùng smaller image model: CLIP ViT-B/32
3. Tắt image similarity nếu không cần thiết

---

## 📊 Metrics để Đánh Giá Quality

### 1. Video Diversity Score
```
Diversity Score = (Unique Videos / Total Clips) × 100%
```

**Targets:**
- 100% → Perfect (no duplicates) ⭐⭐⭐⭐⭐
- 80-99% → Excellent ⭐⭐⭐⭐
- 60-79% → Good ⭐⭐⭐
- < 60% → Poor ⚠️

### 2. Average Similarity Score
```
Check logs cho "final_score"
```

**Targets:**
- > 0.70 → Excellent match ⭐⭐⭐⭐⭐
- 0.60-0.70 → Good match ⭐⭐⭐⭐
- 0.50-0.60 → OK ⭐⭐⭐
- < 0.50 → Poor ⚠️

### 3. Video Coverage per Search Term
```
Check logs cho "Diversity metrics"
```

**Target:**
- Mỗi search term được dùng ít nhất 1 video
- Không có term nào chiếm > 40% total videos

---

## 🎓 Advanced Tips

### 1. Custom Search Terms Strategy

**Thay vì dùng LLM generate**, tự viết search terms:

```python
# Bad (LLM auto-generate)
"technology, innovation, future, digital, computer"

# Good (manual, specific)
"programmer typing code on laptop, 
 tech startup office meeting,
 smartphone closeup hands,
 data center server racks,
 person using tablet in cafe"
```

### 2. Video Source Optimization

**Pexels vs Pixabay:**
- **Pexels:** Nhiều video, quality tốt hơn ⭐⭐⭐⭐⭐
- **Pixabay:** Ít hơn nhưng free API

**Khuyến nghị:** Dùng Pexels và get API key

### 3. Segment Script Manually

Thay vì để system auto-segment, tự chia script thành các đoạn có ý nghĩa:

```
Đoạn 1: Introduction về topic
Đoạn 2: Problem statement  
Đoạn 3: Solution explanation
Đoạn 4: Call to action
```

Mỗi đoạn nên 40-80 chữ.

### 4. Semantic Model Selection

**Models available:**
- `all-mpnet-base-v2` → Best accuracy, slower ⭐⭐⭐⭐⭐ **KHUYẾN NGHỊ**
- `all-MiniLM-L12-v2` → Balanced ⭐⭐⭐⭐
- `all-MiniLM-L6-v2` → Fast, lower accuracy ⭐⭐⭐

**Khuyến nghị:** Dùng `all-mpnet-base-v2` trừ khi gen video quá chậm

---

## 📋 Checklist Trước Khi Generate

### ✅ Pre-Generation Checklist

**Basic Settings:**
- [ ] Video Concat Mode = "Semantic Text Alignment"
- [ ] Search Pool Size ≥ 100
- [ ] Max Video Reuse = 1 (for short videos)
- [ ] Similarity Threshold = 0.65-0.70

**Search Terms:**
- [ ] Có ít nhất `audio_duration / 10` terms
- [ ] Terms cụ thể, mô tả hành động/visual
- [ ] Không dùng abstract concepts

**Image Similarity:**
- [ ] Enabled (nếu có GPU hoặc đủ thời gian)
- [ ] Threshold = 0.65-0.70
- [ ] Model = CLIP ViT-B/32

**Testing:**
- [ ] Test với 1 video trước
- [ ] Check logs xem có lỗi "No suitable video"
- [ ] Review diversity metrics

---

## 🎯 Summary: Best Practices

### **Top 5 Settings để Tránh Lặp Video** 🔥

1. ⭐⭐⭐⭐⭐ **Max Video Reuse = 1**
2. ⭐⭐⭐⭐⭐ **Search Pool Size = 100-150**
3. ⭐⭐⭐⭐ **Enable Image Similarity**
4. ⭐⭐⭐⭐ **Similarity Threshold = 0.65-0.70**
5. ⭐⭐⭐ **Tốt Search Terms (specific, visual)**

### **Top 5 Settings để Video Liên Quan Hơn** 🎯

1. ⭐⭐⭐⭐⭐ **Enable Image Similarity + 0.70 threshold**
2. ⭐⭐⭐⭐⭐ **Good Search Terms (cụ thể, visual)**
3. ⭐⭐⭐⭐ **Similarity Threshold ≥ 0.65**
4. ⭐⭐⭐⭐ **Large Search Pool (100+)**
5. ⭐⭐⭐ **Min Segment Length ≥ 35**

---

## 🔗 Related Docs

- [Semantic Video Matching Technical Details](../app/services/semantic_video.py)
- [Image Similarity Service](../app/services/image_similarity.py)
- [Configuration Guide](../config.example.toml)

---

**Last Updated:** 2026-02-11  
**Version:** 1.0  
**Author:** MoneyPrinterTurbo Extended Team
