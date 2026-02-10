# Quick Settings Reference - Tránh Video Lặp & Tăng Độ Liên Quan

## 🚀 Quick Fix - Copy Settings Này Vào WebUI

### ⭐ Cấu Hình Khuyến Nghị (No Duplicate Videos)

```
┌─────────────────────────────────────────────┐
│     VIDEO SETTINGS                          │
├─────────────────────────────────────────────┤
│ Video Concat Mode: Semantic Text Alignment │
│ Search Pool Size: 120                       │
│                                             │
│ Segmentation: Paragraphs                    │
│ Min Segment Length: 40                      │
│ Similarity Threshold: 0.70                  │
│ Diversity Threshold: 10                     │
│ Max Video Reuse: 1  ← 🔥 QUAN TRỌNG        │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│     IMAGE SIMILARITY                        │
├─────────────────────────────────────────────┤
│ ✅ Enable Image Similarity                  │
│ Image Similarity Threshold: 0.70            │
│ Model: CLIP ViT-B/32 (Recommended)         │
└─────────────────────────────────────────────┘
```

### 📊 Kết Quả Mong Đợi
- ✅ **KHÔNG BAO GIỜ LẶP VIDEO**
- ✅ Video rất liên quan với nội dung
- ✅ Diversity score: 100%

---

## 🎯 So Sánh Settings

| Setting | Mặc Định | Khuyến Nghị | Aggressive | Lý Do |
|---------|----------|-------------|-----------|-------|
| **Max Video Reuse** | 2 | **1** | 1 | 🔥 Không lặp |
| **Similarity Threshold** | 0.50 | **0.70** | 0.75 | Liên quan hơn |
| **Search Pool Size** | 50 | **120** | 150 | Nhiều lựa chọn |
| **Diversity Threshold** | 5 | **10** | 12 | Cách xa hơn |
| **Image Similarity** | No | **Yes** | Yes | +30% accuracy |

---

## 🔧 Tùy Chỉnh Theo Loại Video

### Video Shorts (< 60s)
```yaml
Max Video Reuse: 1
Search Pool Size: 100
Similarity Threshold: 0.70
```

### Video Dài (1-3 mins)
```yaml
Max Video Reuse: 2
Search Pool Size: 150
Similarity Threshold: 0.65
```

### Video Rất Dài (> 3 mins)
```yaml
Max Video Reuse: 2-3
Search Pool Size: 200
Similarity Threshold: 0.60
```

---

## ⚡ Nếu Bị Lỗi "No suitable video found"

**Lỗi này có nghĩa:** Không đủ video trong pool

**Fix nhanh:**

```
1. ⬆️ Tăng Search Pool Size → 150-200
2. ⬆️ Tăng Max Video Reuse → 2
3. ⬇️ Giảm Similarity Threshold → 0.60
```

---

## 📝 Viết Search Terms Tốt Hơn

### ❌ Bad (Chung chung)
```
success, motivation, money, business
```

### ✅ Good (Cụ thể, visual)
```
businessman shaking hands in office,
person climbing mountain peak,
money falling from sky slow motion,
entrepreneur presenting to investors,
laptop keyboard typing closeup
```

**Rule:** Mô tả **hành động** và **cảnh visuals cụ thể**

---

## 🎓 Hiểu Max Video Reuse

### Max Video Reuse = 1 (No Duplicates)
```
Video A → Segment 1
Video B → Segment 2
Video C → Segment 3
Video D → Segment 4
...
```
✅ Mỗi video chỉ dùng **1 lần**

### Max Video Reuse = 2 (Allow Duplicates)
```
Video A → Segment 1, Segment 6
Video B → Segment 2, Segment 7
Video C → Segment 3
Video D → Segment 4
...
```
⚠️ Video có thể lặp **tối đa 2 lần**

### Khi nào dùng > 1?
- Video dài (> 2 mins)
- Ít search terms
- Pool video nhỏ (< 80)

---

## 🚨 Checklist Trước Khi Generate

### Ensure Settings
- [ ] Video Concat Mode = **"Semantic Text Alignment"**
- [ ] Max Video Reuse = **1** (hoặc 2 cho video dài)
- [ ] Search Pool Size ≥ **100**
- [ ] Similarity Threshold ≥ **0.65**
- [ ] ✅ **Enable Image Similarity**

### Check Search Terms
- [ ] Có ít nhất 5-8 terms
- [ ] Terms cụ thể, mô tả visual
- [ ] Không dùng abstract words

### Ready to Generate!
- [ ] Test với 1 video trước
- [ ] Monitor logs không có "No suitable video"

---

## 📈 Đánh Giá Kết Quả

### Check Logs After Generation

**Look for:**
```
🎯 Diversity metrics:
   📊 Search terms represented: 5/5
   📹 'businessman meeting': 3 videos (25.0%)
   📹 'mountain climbing': 2 videos (16.7%)
   ...

✅ Good: Mỗi term được dùng đều
⚠️  Bad: 1 term chiếm > 50%
```

**Check Video Usage:**
```
🔄 Video usage statistics:
   Used 0 times: 50 videos
   Used 1 times: 12 videos
   Used 2 times: 0 videos

✅ Perfect: Chỉ có "Used 1 times"
⚠️  Warning: Có "Used 2 times" hoặc "Used 3 times"
```

---

## 🎯 Golden Rules

1. **Max Video Reuse = 1** → No duplicates ⭐⭐⭐⭐⭐
2. **Search Pool ≥ 100** → Many choices ⭐⭐⭐⭐⭐
3. **Similarity ≥ 0.65** → Relevant videos ⭐⭐⭐⭐
4. **Enable Image Similarity** → Better matching ⭐⭐⭐⭐
5. **Good Search Terms** → Everything else depends on this! ⭐⭐⭐⭐⭐

---

## 🔗 Full Documentation

👉 [VIDEO_QUALITY_OPTIMIZATION.md](VIDEO_QUALITY_OPTIMIZATION.md) - Complete guide with all details

---

**Quick Tip:** Nếu vẫn lặp video, double-check bạn đang ở mode **"Semantic"** chứ không phải **"Random"**! 🎯
