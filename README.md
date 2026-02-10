# MoneyPrinterTurbo - Phiên Bản Nâng Cấp

> **[🌐 Read in English](README_EN.md)** | **[📖 Đọc bản tiếng Việt](README.md)**

Đây là phiên bản nâng cấp của [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) với nhiều cải tiến đáng kể về hệ thống phụ đề và khả năng TTS. Xin gửi lời cảm ơn đến tác giả gốc và các cộng tác viên.

## 🌟 Điểm Khác Biệt Trong Phiên Bản Này

### Hệ Thống Phụ Đề Nâng Cao
- **Làm nổi bật từng từ**: Mỗi từ sáng lên chính xác khi được phát âm, tạo video hấp dẫn hơn
- **Đồng bộ thời gian thực**: Timing hoàn hảo với ranh giới từ của TTS
- **Hỗ trợ đa dòng**: Hoạt động với văn bản xuống dòng và bố cục phụ đề phức tạp
- **Màu sắc tùy chỉnh**: Cấu hình màu highlight qua giao diện web

### Khớp Video-Văn Bản Thông Minh
- **Tìm kiếm ngữ nghĩa**: Phân tích nội dung kịch bản để tìm video clip phù hợp thay vì chọn ngẫu nhiên
- **Độ tương đồng văn bản**: Khớp nội dung video với ý nghĩa kịch bản để đạt độ liên quan cao hơn
- **Phân tích thumbnail**: Tùy chọn so sánh thumbnail video cho các nguồn như Pexels

### TTS Mã Nguồn Mở với Nhân Bản Giọng Nói
Fork này bao gồm **Chatterbox TTS** - một giải pháp thay thế hoàn toàn miễn phí cho Azure TTS chạy trên máy của bạn.

**Ưu điểm chính:**
- **Không mất phí API**: Hoàn toàn miễn phí, không giới hạn tốc độ
- **Nhân bản giọng nói**: Clone bất kỳ giọng nói nào chỉ với 10-60 giây audio tham khảo
- **Timing cấp từ**: Đồng bộ phụ đề hoàn hảo với tích hợp WhisperX
- **Kiểm soát tốc độ tự động**: Điều chỉnh nhịp độ giọng nói qua biến môi trường

### 🎤 Google Translate TTS (gTTS) - Miễn Phí
Thêm hỗ trợ **gTTS** - giải pháp TTS miễn phí từ Google Translate.

**Tính năng:**
- **Hoàn toàn miễn phí**: Không cần API key, không giới hạn
- **25+ ngôn ngữ**: Tiếng Việt, Tiếng Anh, Tiếng Trung, Tiếng Nhật, Hàn Quốc, và nhiều hơn nữa
- **Dễ sử dụng**: Chỉ cần chọn ngôn ngữ và bắt đầu tạo video
- **Chất lượng ổn định**: Sử dụng công nghệ TTS của Google

**Cách sử dụng gTTS:**
1. Mở WebUI
2. Chọn "gTTS (Google Translate TTS - Free)" trong TTS Servers
3. Chọn ngôn ngữ mong muốn (ví dụ: Vietnamese-VN, English-US)
4. Tạo video như bình thường

### 📥 Tải Xuống Video Trực Tiếp
**Tính năng mới** - Preview và tải video ngay trong giao diện web.

**Tính năng:**
- **Video player tích hợp**: Xem video ngay sau khi tạo xong
- **Nút tải xuống**: Download video trực tiếp từ trình duyệt
- **Hỗ trợ đa ngôn ngữ**: Interface đa ngôn ngữ (VI, EN, CN, DE, PT)
- **Layout tối ưu**: Hiển thị video và nút download rõ ràng

## 🎬 Video Mẫu

Xem các tính năng nâng cao trong thực tế:

**Video Dài Hoàn Chỉnh**

[![MoneyPrinterTurbo Example Video](https://img.youtube.com/vi/yXc07ROgj80/maxresdefault.jpg)](https://www.youtube.com/watch?v=yXc07ROgj80)

**YouTube Shorts**  

[![MoneyPrinterTurbo Shorts Example](https://img.youtube.com/vi/JBAuXpVHt40/maxresdefault.jpg)](https://www.youtube.com/shorts/JBAuXpVHt40)

**Video Tạo Bằng Chatterbox TTS**  

[![MoneyPrinterTurbo Chatterbox Example](https://img.youtube.com/vi/ZAttF-cVce8/maxresdefault.jpg)](https://youtube.com/shorts/ZAttF-cVce8?feature=share)

> **Tính Năng Được Giới Thiệu**: Tổng hợp giọng nói tự nhiên • Highlight phụ đề theo từ • Đồng bộ timing • Chất lượng TTS mã nguồn mở

## 🖼️ Ảnh Chụp Màn Hình - Thiết Lập Tạo Video

Để đảm bảo tính minh bạch và khả năng tái tạo, vui lòng xem các cài đặt được sử dụng để tạo video ở trên

<div align="center">
<img src="docs/ui_config_1.png" alt="Giao Diện Chính" width="800"/>

<img src="docs/ui_config_2.png" alt="Cài Đặt Giọng Nói" width="800"/>
</div>
## 🐳 CI/CD & Docker Deployment

### Tự Động Build & Tối Ưu với GitHub Actions

Repository này được tích hợp **CI/CD pipeline** tự động build, tối ưu Docker images với **docker-slim** và push lên **GitHub Container Registry**.

#### ✨ Tính Năng CI/CD

- 🔄 **Auto Build**: Tự động build khi push code to main/develop
- 📦 **Docker Slim**: Tối ưu image size giảm **60-70%** (từ ~1.2GB → ~400MB)
- 📊 **Size Comparison**: Tự động so sánh và báo cáo size reduction
- 🚀 **Auto Deploy**: Push optimized images to GitHub Container Registry
- 💬 **PR Comments**: Comment kết quả size comparison trên Pull Requests
- 🏷️ **Smart Tagging**: Tự động tag theo branch, commit SHA, và semantic version

#### 🎯 Kết Quả Tối Ưu

```
📊 Docker Image Optimization Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Size:    1.23 GB
Optimized Size:   421 MB
Reduction:        65.77% ⬇️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 📦 Pull Pre-built Images

```bash
# Pull latest optimized image
docker pull ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest

# Run WebUI
docker run -v $(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \
           -v $(pwd)/storage:/MoneyPrinterTurbo/storage \
           -p 8501:8501 \
           ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest

# Run API Server
docker run -v $(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \
           -v $(pwd)/storage:/MoneyPrinterTurbo/storage \
           -p 8080:8080 \
           ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest \
           python3 main.py
```

#### 🛠️ Build & Optimize Locally

Muốn test build locally trước khi push?

```bash
# Linux/Mac
chmod +x build-docker-local.sh
./build-docker-local.sh

# Windows
build-docker-local.bat
```

Script sẽ tự động:
1. Build Docker image gốc
2. Thu thập size metrics
3. Cài đặt docker-slim (nếu chưa có)
4. Optimize image với docker-slim
5. So sánh và hiển thị kết quả
6. Tag optimized image as `latest`

#### 📖 Chi Tiết Hướng Dẫn

Để biết chi tiết về:
- Setup GitHub Container Registry
- Cấu hình workflows
- Tuning docker-slim parameters
- Troubleshooting tips

👉 Xem [**docs/CI_CD_SETUP.md**](docs/CI_CD_SETUP.md)

#### 🔧 Workflows Có Sẵn

| Workflow | Trigger | Mục Đích |
|----------|---------|----------|
| **docker-build-optimized.yml** | Push to main/develop, PRs | Build, optimize & deploy production images |
| **docker-quick-build.yml** | Manual dispatch | Quick test builds without optimization |
## � Tài Liệu Hướng Dẫn

### Jupyter Notebook - Hướng Dẫn Cài Đặt Nhanh

Chúng tôi cung cấp một Jupyter Notebook chi tiết để giúp bạn bắt đầu nhanh chóng:

📓 **[docs/MoneyPrinterTurbo.ipynb](docs/MoneyPrinterTurbo.ipynb)**

**Nội dung notebook:**
- 🚀 Hướng dẫn cài đặt từng bước (bao gồm hỗ trợ CUDA)
- ⚙️ Cấu hình API keys và các tham số
- 🎯 Khởi chạy WebUI và API server
- 💡 Tips về các tính năng tối ưu hiệu suất

**Cách sử dụng:**
1. Mở notebook trong Jupyter Lab/Notebook hoặc VS Code
2. Làm theo các cell theo thứ tự
3. Chạy các lệnh để cài đặt và khởi động hệ thống

> 💡 **Tip**: Notebook đặc biệt hữu ích cho người dùng mới hoặc khi cần setup trên môi trường mới (Google Colab, remote server, etc.)

## �📝 Prompt Hệ Thống

Đây là prompt chính xác mà chúng tôi sử dụng để tạo nội dung YouTube hấp dẫn:

<details>
<summary><strong>Prompt Hoàn Chỉnh Để Tạo Video Cho LLM Của Bạn (Nhấp để mở rộng)</strong></summary>

```
VAI TRÒ: Bạn là một chuyên gia viết kịch bản YouTube và chiến lược nội dung chuyên tạo nội dung hấp dẫn, dựa trên khoa học cho đối tượng rộng.

MỤC TIÊU: Tạo một gói nội dung văn bản hoàn chỉnh cho video YouTube 5 phút. Mục đích là chọn một chủ đề hấp dẫn và tạo tất cả các tài sản cần thiết để sản xuất video, được tối ưu hóa cho khả năng giữ chân khán giả và thuật toán YouTube.

TIÊU CHÍ CHỌN CHỦ ĐỀ:
• Trending & Phù Hợp: Chủ đề phải có lượng quan tâm và tìm kiếm cao hiện nay
• Thu Hút Rộng: Liên quan đến đối tượng rộng (năng suất, sức khỏe, tài chính cá nhân, tâm lý học)
• Dựa Trên Khoa Học: Căn cứ vào sự đồng thuận khoa học chính thống được chấp nhận rộng rãi
• An Toàn & Không Gây Tranh Cãi: Tập trung vào kiến thức nền tảng, có thể hành động

CÁC KHOẢN GIAO HÀNG YÊU CẦU:

1. Tùy Chọn Tiêu Đề Video (3x)
   Mục Tiêu: Tạo ba tiêu đề YouTube riêng biệt, có thể click được, tối ưu cho CTR cao
   Ví Dụ Phong Cách: "Lập Trình Lại Não Bộ Lo Âu Của Bạn Trong 3 Bước Đơn Giản"

2. Kịch Bản Video Đầy Đủ
   Độ Dài: 800-900 từ (~5 phút nói)
   Định Dạng: Đoạn văn đơn với dấu câu phù hợp cho tối ưu TTS
   Tone: Có thẩm quyền nhưng khuyến khích, dễ tiêu hóa cho khán giả chung
   Tối Ưu TTS: Kết thúc câu với dấu câu rõ ràng cho ngắt nghỉ tự nhiên

3. Từ Khóa Tìm Kiếm Video Pexels
   Cấu Trúc: Từ khóa được tổ chức theo khái niệm kịch bản để đa dạng hình ảnh
   Đầu Ra: Dòng đơn phân tách bằng dấu phẩy
   Ví Dụ: brain animation, neural network, person thinking, scrolling on phone

4. Mô Tả YouTube & Hashtag
   Mô Tả: Tóm tắt tối ưu SEO (2-3 dòng) với lời kêu gọi hành động rõ ràng
   Hashtag: 10-15 hashtag liên quan để tối đa khả năng phát hiện
```
</details>

## 💻 Cài Đặt

**Bắt Đầu Nhanh (Khuyến Nghị):**

```bash
# 1. Clone và thiết lập
git clone https://github.com/Cong-ty-TNNH-Q-Tech/CreateVideo.git
cd CreateVideo
conda env create -f environment.yml
conda activate MoneyPrinterTurbo

# 2. Cài đặt Chatterbox TTS (nhân bản giọng nói)
git clone https://github.com/resemble-ai/chatterbox.git
cd chatterbox && pip install -e . && cd ..

# 3. Cài đặt gTTS (TTS miễn phí)
pip install gTTS==2.5.4

## Cho thiết lập CUDA cụ thể (nếu cần)
source ./setup_cuda_env.sh    
```

**Sử Dụng:**
```bash
# Giao Diện Web (Khuyến Nghị)
./webui.sh            

## Tùy Chọn: Tùy chỉnh tốc độ giọng nói khi sử dụng chatterbox
export CHATTERBOX_CFG_WEIGHT=0.1  # Rất chậm
export CHATTERBOX_CFG_WEIGHT=0.2  # Chậm (mặc định)
export CHATTERBOX_CFG_WEIGHT=0.3  # Tốc độ bình thường
```

Giao diện web mở tại `http://localhost:8501`

## 🎨 Các Tùy Chọn TTS Có Sẵn

1. **Azure TTS V1/V2** - TTS chất lượng cao từ Microsoft (cần API key)
2. **SiliconFlow TTS** - TTS từ SiliconFlow (cần API key)
3. **Chatterbox TTS** - TTS mã nguồn mở với nhân bản giọng nói (miễn phí, chạy local)
4. **gTTS** - Google Translate TTS (miễn phí, không cần API key) ✨ MỚI

## 🔧 Xử Lý Sự Cố

<details>
<summary><strong>Các Vấn Đề Thường Gặp & Giải Pháp (Nhấp để mở rộng)</strong></summary>

**Vấn đề Chatterbox TTS:**
- **Audio bị loạn**: Văn bản tự động được tiền xử lý và chia nhỏ để rõ ràng hơn
- **Lỗi CUDA**: Hệ thống tự động chuyển sang chế độ CPU
- **Buộc chế độ CPU**: `export CHATTERBOX_DEVICE=cpu`
- **Vấn đề nhân bản giọng nói**: Đảm bảo audio rõ ràng và chỉ có một người nói
- **Kiểm soát tốc độ**: Sử dụng biến môi trường `CHATTERBOX_CFG_WEIGHT`

**Vấn đề gTTS:**
- **Cần kết nối internet**: gTTS sử dụng Google Translate API online
- **Tốc độ giọng nói**: gTTS có tùy chọn slow (chậm) hoặc normal (bình thường)
- **Không hỗ trợ điều chỉnh pitch**: gTTS không cho phép thay đổi cao độ giọng nói

**Vấn đề tương thích CUDA/cuDNN:**
- **Lỗi**: `libcudnn_ops_infer.so.8: cannot open shared object file`
- **Nguyên Nhân**: Thiếu thư viện cuDNN 8.x cần thiết cho một số package
- **Giải Pháp**: Tự động xử lý bởi script khởi động (`setup_cuda_env.sh`)
- **Fix thủ công**: `pip install nvidia-cudnn-cu12==8.9.2.26`

**Vấn đề MoviePy TextClip:**
- **Lỗi**: `got an unexpected keyword argument 'align'`
- **Nguyên Nhân**: Các phiên bản MoviePy mới hơn đã loại bỏ tham số `align`
- **Giải Pháp**: Loại bỏ hoặc comment tham số `align` trong các lời gọi `TextClip`

**Vấn đề chung:**
- Kiểm tra tất cả dependencies đã được cài đặt đúng
- Đảm bảo môi trường Python của bạn đã được kích hoạt
- Đối với vấn đề GPU, chế độ CPU cung cấp giải pháp dự phòng đáng tin cậy

**Thiết Lập CUDA Nâng Cao:**
Dự án bao gồm cấu hình môi trường CUDA tự động:
- `setup_cuda_env.sh` - Thiết lập môi trường CUDA dùng chung
- `webui.sh` - Giao diện web với hỗ trợ CUDA

Nếu bạn gặp vấn đề thư viện CUDA, các script khởi động tự động:
1. Thêm đường dẫn thư viện cuDNN vào `LD_LIBRARY_PATH` (Linux)
2. Đặt cài đặt phân bổ bộ nhớ CUDA tối ưu

</details>

## 🤝 Đóng Góp và Hỗ Trợ

Nếu bạn thấy dự án này hữu ích, vui lòng cho nó một star và cân nhắc đóng góp vào nó hoặc mở một issue nếu bạn có ý tưởng có thể làm cho nó hữu ích hơn.

## 📜 Tín Dụng Dự Án Gốc

Fork này duy trì khả năng tương thích hoàn toàn với MoneyPrinterTurbo gốc trong khi thêm các tính năng mới. Kiểm tra [repository gốc](https://github.com/harry0703/MoneyPrinterTurbo) cho tài liệu dự án cơ bản và các tính năng bổ sung.

## 📄 Giấy Phép

Dự án này kế thừa giấy phép từ dự án gốc MoneyPrinterTurbo.

---

**Được phát triển với ❤️ bởi Q-Tech Company**

Repository: https://github.com/Cong-ty-TNNH-Q-Tech/CreateVideo
