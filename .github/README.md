# GitHub Actions CI/CD

Workflow tự động build, tối ưu Docker image với docker-slim và push lên GitHub Container Registry.

## 🚀 Workflows

### `docker-build-optimized.yml`

Workflow chính để build và tối ưu Docker images:

**Trigger:**
- Push to `main` hoặc `develop` branch
- Pull requests to `main`
- Manual dispatch

**Các bước thực hiện:**

1. ✅ Checkout source code
2. 🔧 Setup Docker Buildx
3. 🔐 Login to GitHub Container Registry
4. 📦 Build Docker image gốc
5. 📊 Thu thập size của image gốc
6. ⚙️ Cài đặt docker-slim
7. 🎯 Tối ưu image với docker-slim
8. 📊 Thu thập size của image đã tối ưu
9. 📈 So sánh và hiển thị kết quả
10. 🚀 Push images đã tối ưu lên registry
11. 💬 Comment kết quả trên PR (nếu là PR)

## 📊 Docker Image Size Comparison

Workflow sẽ tự động so sánh và hiển thị:
- Size của image gốc
- Size của image đã tối ưu
- Phần trăm giảm sau khi tối ưu

Kết quả được hiển thị trong:
- GitHub Actions logs
- GitHub Actions summary
- PR comments (nếu là PR)

## 🐳 Sử dụng Images

### Pull image từ GitHub Container Registry

```bash
# Pull latest version
docker pull ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest

# Pull by branch
docker pull ghcr.io/cong-ty-tnnh-q-tech/createvideo:main

# Pull by commit SHA
docker pull ghcr.io/cong-ty-tnnh-q-tech/createvideo:main-abc1234
```

### Run container

```bash
# WebUI
docker run -v $(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \
  -v $(pwd)/storage:/MoneyPrinterTurbo/storage \
  -p 8501:8501 \
  ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest

# API
docker run -v $(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \
  -v $(pwd)/storage:/MoneyPrinterTurbo/storage \
  -p 8080:8080 \
  ghcr.io/cong-ty-tnnh-q-tech/createvideo:latest \
  python3 main.py
```

## 🔧 Docker Slim Configuration

Docker-slim được cấu hình với các options sau:

- `--http-probe=false`: Tắt HTTP probing
- `--continue-after=20`: Tiếp tục sau 20 giây
- `--include-path`: Bao gồm các đường dẫn cần thiết
  - `/MoneyPrinterTurbo`: Application code
  - `/usr/local/lib/python3.11`: Python libraries
  - `/usr/local/bin`: Python binaries
  - `/usr/bin/ffmpeg`: FFmpeg binary
  - `/usr/bin/convert`: ImageMagick binary
  - `/etc/ImageMagick-6`: ImageMagick config
- `--include-bin=/usr/bin/git`: Git binary
- `--preserve-path`: Preserve directories
  - `/tmp`: Temporary files
  - `/root/.cache`: Cache directory

## 📝 Environment Variables

Workflow sử dụng các environment variables sau:

- `REGISTRY`: `ghcr.io` - GitHub Container Registry
- `IMAGE_NAME`: `${{ github.repository }}` - Repository name

## 🔐 Permissions Required

Workflow cần các permissions sau:

- `contents: read` - Đọc repository code
- `packages: write` - Push images to GitHub Container Registry

## 🎯 Image Tags

Images được tag tự động với:

- `latest` - Latest commit on default branch
- `main` hoặc `develop` - Branch name
- `pr-123` - Pull request number
- `main-abc1234` - Branch + commit SHA
- Semantic version tags (nếu có)

## 📈 Monitoring

Kiểm tra kết quả build:

1. Vào tab **Actions** trên GitHub repository
2. Chọn workflow run mới nhất
3. Xem **Summary** để thấy so sánh size
4. Xem logs chi tiết cho từng step

## 🐛 Troubleshooting

### Image quá lớn sau khi optimize

Điều chỉnh docker-slim parameters trong workflow:
- Thêm `--include-path` cho các dependencies còn thiếu
- Điều chỉnh `--continue-after` để tăng thời gian analysis

### Application không chạy sau khi optimize

Kiểm tra logs và thêm các paths cần thiết vào `--include-path` hoặc `--preserve-path`.

### Push to registry fails

Kiểm tra:
- Repository có enable GitHub Packages
- Workflow có permission `packages: write`
- Personal Access Token (nếu dùng) có scope `write:packages`

## 📚 Resources

- [Docker Slim Documentation](https://github.com/slimtoolkit/slim)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [GitHub Actions Docker](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)
