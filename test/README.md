# MoneyPrinterTurbo Test Directory

This directory contains unit tests for the **MoneyPrinterTurbo** project.

## Directory Structure

- `services/`: Tests for components in the `app/services` directory  
  - `test_video.py`: Tests for the video service  
  - `test_task.py`: Tests for the task service  
  - `test_voice.py`: Tests for the voice service  
- `test_parallel_downloads.py`: Test for parallel video download optimization

## Running Tests

### Standard Unit Tests

You can run the tests using Python’s built-in `unittest` framework:

```bash
# Run all tests
python -m unittest discover -s test

# Run a specific test file
python -m unittest test/services/test_video.py

# Run a specific test class
python -m unittest test.services.test_video.TestVideoService

# Run a specific test method
python -m unittest test.services.test_video.TestVideoService.test_preprocess_video
````

### 🚀 Performance Optimization Tests

#### Test Parallel Downloads

Test the parallel video download optimization (60-80% faster):

```bash
# Full test (downloads actual videos)
python test/test_parallel_downloads.py

# Quick test (config check only, no downloads)
python test/test_parallel_downloads.py --skip-download

# Test with specific video source
python test/test_parallel_downloads.py --source pexels

# Test with custom duration
python test/test_parallel_downloads.py --duration 60
```

**What to expect:**
- 🚀 Speedup metric: Look for "🚀 Speedup: X.X× faster than sequential"
- ✅ Good result: Speedup > 3× (e.g., 4-5× is typical with 5 workers)
- ⚠️ Poor result: Speedup < 2× (may need to increase `max_download_workers`)

**Configuration:**
```toml
# In config.toml
[app]
max_download_workers = 5  # 3-10 recommended
```

**Troubleshooting:**
- If speedup is low: Increase `max_download_workers` (try 8-10)
- If errors occur: Decrease `max_download_workers` (try 3)
- Check network speed and API rate limits

## Adding New Tests

To add tests for other components, follow these guidelines:

1. Create test files prefixed with `test_` in the appropriate subdirectory
2. Use `unittest.TestCase` as the base class for your test classes
3. Name test methods with the `test_` prefix

## Test Resources

Place any resource files required for testing in the `test/resources` directory.