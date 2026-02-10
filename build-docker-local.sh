#!/usr/bin/env bash

# Script để test Docker build và optimization locally
# Similar to CI/CD workflow nhưng chạy trên máy local

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="moneyprinterturbo"
ORIGINAL_TAG="${IMAGE_NAME}:original"
OPTIMIZED_TAG="${IMAGE_NAME}:optimized"
LATEST_TAG="${IMAGE_NAME}:latest"

echo -e "${BLUE}🚀 MoneyPrinter Turbo - Local Docker Build & Optimization${NC}"
echo "================================================================"

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to format bytes to human readable
format_bytes() {
    local bytes=$1
    if [ $bytes -gt 1073741824 ]; then
        echo "$(awk "BEGIN {printf \"%.2f GB\", $bytes/1073741824}")"
    elif [ $bytes -gt 1048576 ]; then
        echo "$(awk "BEGIN {printf \"%.2f MB\", $bytes/1048576}")"
    elif [ $bytes -gt 1024 ]; then
        echo "$(awk "BEGIN {printf \"%.2f KB\", $bytes/1024}")"
    else
        echo "${bytes} bytes"
    fi
}

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

print_success "Docker is installed"

# Step 1: Build original image
echo ""
print_info "Step 1/5: Building original Docker image..."
echo "================================================================"

docker build -t "$ORIGINAL_TAG" .

print_success "Original image built successfully"

# Step 2: Get original image size
echo ""
print_info "Step 2/5: Analyzing original image size..."
echo "================================================================"

ORIGINAL_SIZE_BYTES=$(docker inspect "$ORIGINAL_TAG" --format='{{.Size}}')
ORIGINAL_SIZE_HR=$(format_bytes $ORIGINAL_SIZE_BYTES)

print_success "Original image size: $ORIGINAL_SIZE_HR ($ORIGINAL_SIZE_BYTES bytes)"

# Step 3: Install docker-slim if not present
echo ""
print_info "Step 3/5: Checking docker-slim installation..."
echo "================================================================"

if ! command -v docker-slim &> /dev/null; then
    print_warning "docker-slim not found. Installing..."
    
    # Detect OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -L -o ds.tar.gz https://github.com/slimtoolkit/slim/releases/download/1.40.11/dist_linux.tar.gz
        tar -xvf ds.tar.gz
        sudo mv dist_linux/* /usr/local/bin/
        rm ds.tar.gz
        rm -rf dist_linux
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        curl -L -o ds.tar.gz https://github.com/slimtoolkit/slim/releases/download/1.40.11/dist_mac.tar.gz
        tar -xvf ds.tar.gz
        sudo mv dist_mac/* /usr/local/bin/
        rm ds.tar.gz
        rm -rf dist_mac
    else
        print_error "Unsupported OS. Please install docker-slim manually."
        exit 1
    fi
    
    print_success "docker-slim installed successfully"
else
    print_success "docker-slim is already installed"
fi

# Show version
SLIM_VERSION=$(docker-slim --version)
print_info "docker-slim version: $SLIM_VERSION"

# Step 4: Optimize image
echo ""
print_info "Step 4/5: Optimizing image with docker-slim..."
echo "================================================================"
print_warning "This may take 2-5 minutes. Please be patient..."

docker-slim build \
    --target "$ORIGINAL_TAG" \
    --tag "$OPTIMIZED_TAG" \
    --http-probe=false \
    --continue-after=20 \
    --include-path=/MoneyPrinterTurbo \
    --include-path=/usr/local/lib/python3.11 \
    --include-path=/usr/local/bin \
    --include-path=/usr/bin/ffmpeg \
    --include-path=/usr/bin/convert \
    --include-path=/etc/ImageMagick-6 \
    --include-bin=/usr/bin/git \
    --preserve-path=/tmp \
    --preserve-path=/root/.cache \
    || print_warning "Docker-slim completed with warnings (this is often normal)"

print_success "Image optimization completed"

# Step 5: Compare sizes
echo ""
print_info "Step 5/5: Comparing image sizes..."
echo "================================================================"

OPTIMIZED_SIZE_BYTES=$(docker inspect "$OPTIMIZED_TAG" --format='{{.Size}}')
OPTIMIZED_SIZE_HR=$(format_bytes $OPTIMIZED_SIZE_BYTES)

REDUCTION_BYTES=$((ORIGINAL_SIZE_BYTES - OPTIMIZED_SIZE_BYTES))
REDUCTION_HR=$(format_bytes $REDUCTION_BYTES)
REDUCTION_PERCENT=$(awk "BEGIN {printf \"%.2f\", ($REDUCTION_BYTES / $ORIGINAL_SIZE_BYTES) * 100}")

# Print comparison table
echo ""
echo "📊 Size Comparison Report"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-20s %20s %20s\n" "Metric" "Original" "Optimized"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-20s %20s %20s\n" "Size" "$ORIGINAL_SIZE_HR" "$OPTIMIZED_SIZE_HR"
printf "%-20s %20s %20s\n" "Size (bytes)" "$ORIGINAL_SIZE_BYTES" "$OPTIMIZED_SIZE_BYTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-20s %20s\n" "Reduction" "$REDUCTION_HR ($REDUCTION_PERCENT%)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Tag optimized as latest
docker tag "$OPTIMIZED_TAG" "$LATEST_TAG"
print_success "Tagged optimized image as '$LATEST_TAG'"

# Summary
echo ""
print_success "Build and optimization completed successfully!"
echo ""
echo "📦 Available images:"
echo "   - $ORIGINAL_TAG (original, larger)"
echo "   - $OPTIMIZED_TAG (optimized, smaller)"
echo "   - $LATEST_TAG (alias to optimized)"
echo ""
echo "🚀 To run the optimized image:"
echo ""
echo "   # WebUI (Streamlit)"
echo "   docker run -v \$(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \\"
echo "              -v \$(pwd)/storage:/MoneyPrinterTurbo/storage \\"
echo "              -p 8501:8501 \\"
echo "              $LATEST_TAG"
echo ""
echo "   # API Server"
echo "   docker run -v \$(pwd)/config.toml:/MoneyPrinterTurbo/config.toml \\"
echo "              -v \$(pwd)/storage:/MoneyPrinterTurbo/storage \\"
echo "              -p 8080:8080 \\"
echo "              $LATEST_TAG python3 main.py"
echo ""
echo "🧹 To clean up original image (keep optimized only):"
echo "   docker rmi $ORIGINAL_TAG"
echo ""
