@echo off
REM Script để test Docker build và optimization locally trên Windows
REM Similar to CI/CD workflow nhưng chạy trên Windows

setlocal enabledelayedexpansion

REM Configuration
set IMAGE_NAME=moneyprinterturbo
set ORIGINAL_TAG=%IMAGE_NAME%:original
set OPTIMIZED_TAG=%IMAGE_NAME%:optimized
set LATEST_TAG=%IMAGE_NAME%:latest

echo.
echo ========================================
echo MoneyPrinter Turbo - Local Docker Build
echo ========================================
echo.

REM Check if docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker Desktop first.
    exit /b 1
)

echo [OK] Docker is installed
echo.

REM Step 1: Build original image
echo [STEP 1/5] Building original Docker image...
echo ========================================
docker build -t %ORIGINAL_TAG% .
if errorlevel 1 (
    echo [ERROR] Failed to build original image
    exit /b 1
)
echo [OK] Original image built successfully
echo.

REM Step 2: Get original image size
echo [STEP 2/5] Analyzing original image size...
echo ========================================
for /f "tokens=*" %%i in ('docker inspect %ORIGINAL_TAG% --format="{{.Size}}"') do set ORIGINAL_SIZE_BYTES=%%i
for /f "tokens=*" %%i in ('docker images %ORIGINAL_TAG% --format "{{.Size}}"') do set ORIGINAL_SIZE_HR=%%i
echo [OK] Original image size: !ORIGINAL_SIZE_HR! (!ORIGINAL_SIZE_BYTES! bytes)
echo.

REM Step 3: Check docker-slim
echo [STEP 3/5] Checking docker-slim installation...
echo ========================================
docker-slim --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] docker-slim not found!
    echo.
    echo Please install docker-slim manually:
    echo 1. Download from: https://github.com/slimtoolkit/slim/releases/download/1.40.11/dist_windows.zip
    echo 2. Extract to a folder
    echo 3. Add the folder to your PATH
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('docker-slim --version') do set SLIM_VERSION=%%i
echo [OK] docker-slim is installed: !SLIM_VERSION!
echo.

REM Step 4: Optimize image
echo [STEP 4/5] Optimizing image with docker-slim...
echo ========================================
echo [INFO] This may take 2-5 minutes. Please be patient...
echo.

docker-slim build ^
    --target %ORIGINAL_TAG% ^
    --tag %OPTIMIZED_TAG% ^
    --http-probe=false ^
    --continue-after=20 ^
    --include-path=/MoneyPrinterTurbo ^
    --include-path=/usr/local/lib/python3.11 ^
    --include-path=/usr/local/bin ^
    --include-path=/usr/bin/ffmpeg ^
    --include-path=/usr/bin/convert ^
    --include-path=/etc/ImageMagick-6 ^
    --include-bin=/usr/bin/git ^
    --preserve-path=/tmp ^
    --preserve-path=/root/.cache

echo [OK] Image optimization completed
echo.

REM Step 5: Compare sizes
echo [STEP 5/5] Comparing image sizes...
echo ========================================

for /f "tokens=*" %%i in ('docker inspect %OPTIMIZED_TAG% --format="{{.Size}}"') do set OPTIMIZED_SIZE_BYTES=%%i
for /f "tokens=*" %%i in ('docker images %OPTIMIZED_TAG% --format "{{.Size}}"') do set OPTIMIZED_SIZE_HR=%%i

set /a REDUCTION_BYTES=!ORIGINAL_SIZE_BYTES! - !OPTIMIZED_SIZE_BYTES!

REM Calculate percentage (using powershell for float calculation)
for /f %%i in ('powershell -command "[math]::Round(((!REDUCTION_BYTES! / !ORIGINAL_SIZE_BYTES!) * 100), 2)"') do set REDUCTION_PERCENT=%%i

echo.
echo ========================================
echo    Size Comparison Report
echo ========================================
echo Metric              ^| Original         ^| Optimized
echo ----------------------------------------
echo Size                ^| !ORIGINAL_SIZE_HR!         ^| !OPTIMIZED_SIZE_HR!
echo Size (bytes)        ^| !ORIGINAL_SIZE_BYTES! ^| !OPTIMIZED_SIZE_BYTES!
echo ----------------------------------------
echo Reduction           ^| !REDUCTION_PERCENT!%%
echo ========================================
echo.

REM Tag optimized as latest
docker tag %OPTIMIZED_TAG% %LATEST_TAG%
echo [OK] Tagged optimized image as '%LATEST_TAG%'
echo.

REM Summary
echo ========================================
echo [SUCCESS] Build and optimization completed!
echo ========================================
echo.
echo Available images:
echo   - %ORIGINAL_TAG% (original, larger)
echo   - %OPTIMIZED_TAG% (optimized, smaller)
echo   - %LATEST_TAG% (alias to optimized)
echo.
echo To run the optimized image:
echo.
echo   # WebUI (Streamlit)
echo   docker run -v %cd%/config.toml:/MoneyPrinterTurbo/config.toml ^
echo              -v %cd%/storage:/MoneyPrinterTurbo/storage ^
echo              -p 8501:8501 ^
echo              %LATEST_TAG%
echo.
echo   # API Server
echo   docker run -v %cd%/config.toml:/MoneyPrinterTurbo/config.toml ^
echo              -v %cd%/storage:/MoneyPrinterTurbo/storage ^
echo              -p 8080:8080 ^
echo              %LATEST_TAG% python3 main.py
echo.
echo To clean up original image (keep optimized only):
echo   docker rmi %ORIGINAL_TAG%
echo.
pause
