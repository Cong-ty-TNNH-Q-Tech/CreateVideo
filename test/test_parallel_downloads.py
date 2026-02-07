"""
Test script for parallel video downloads
Run this to verify the optimization is working correctly
"""

import sys
import os

# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

from app.services import material
from app.models.schema import VideoAspect, VideoConcatMode
from loguru import logger


def test_parallel_downloads():
    """Test parallel video downloads with sample task"""
    
    logger.info("="*70)
    logger.info("🧪 TESTING PARALLEL VIDEO DOWNLOADS")
    logger.info("="*70)
    
    # Test configuration
    task_id = "test_parallel_downloads"
    search_terms = ["nature", "technology"]
    source = "pexels"  # or "pixabay"
    video_aspect = VideoAspect.portrait
    audio_duration = 30.0  # 30 seconds of video needed
    max_clip_duration = 5
    
    logger.info(f"\n📋 Test Configuration:")
    logger.info(f"   Task ID: {task_id}")
    logger.info(f"   Search terms: {search_terms}")
    logger.info(f"   Source: {source}")
    logger.info(f"   Target duration: {audio_duration}s")
    logger.info(f"   Max clip duration: {max_clip_duration}s")
    
    try:
        # Run download
        logger.info(f"\n🚀 Starting download test...\n")
        
        video_paths = material.download_videos(
            task_id=task_id,
            search_terms=search_terms,
            source=source,
            video_aspect=video_aspect,
            video_contact_mode=VideoConcatMode.random,
            audio_duration=audio_duration,
            max_clip_duration=max_clip_duration
        )
        
        # Results
        logger.info("\n" + "="*70)
        logger.info("✅ TEST COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        logger.info(f"📊 Downloaded videos: {len(video_paths)}")
        
        if video_paths:
            logger.info(f"\n📁 Video files:")
            for i, path in enumerate(video_paths, 1):
                file_size = os.path.getsize(path) / (1024 * 1024)  # MB
                logger.info(f"   {i}. {os.path.basename(path)} ({file_size:.1f} MB)")
        
        logger.info("\n💡 Look for the speedup metric in the logs above:")
        logger.info("   '🚀 Speedup: X.X× faster than sequential'")
        logger.info("\n✨ If speedup > 3×, parallel downloads are working great!")
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_config_loading():
    """Test if config has max_download_workers setting"""
    from app.config import config
    
    logger.info("\n" + "="*70)
    logger.info("🧪 TESTING CONFIGURATION")
    logger.info("="*70)
    
    max_workers = config.app.get("max_download_workers", None)
    
    if max_workers is not None:
        logger.success(f"✅ max_download_workers is configured: {max_workers}")
        
        if 3 <= max_workers <= 10:
            logger.success(f"✅ Value is in recommended range (3-10)")
        else:
            logger.warning(f"⚠️  Value {max_workers} is outside recommended range (3-10)")
    else:
        logger.warning(f"⚠️  max_download_workers not found in config, using default: 5")
    
    return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test parallel video downloads")
    parser.add_argument(
        "--skip-download", 
        action="store_true",
        help="Skip actual download test (only check config)"
    )
    parser.add_argument(
        "--source",
        default="pexels",
        choices=["pexels", "pixabay"],
        help="Video source to use"
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Target video duration in seconds"
    )
    
    args = parser.parse_args()
    
    print("\n" + "🔧 " + "="*68)
    print("   PARALLEL DOWNLOAD OPTIMIZATION TEST")
    print("   " + "="*68 + "\n")
    
    # Test 1: Configuration
    test_config_loading()
    
    # Test 2: Actual download (if not skipped)
    if not args.skip_download:
        logger.info("\n⏳ Starting download test in 3 seconds...")
        logger.info("   (Press Ctrl+C to cancel)\n")
        
        import time
        try:
            time.sleep(3)
            success = test_parallel_downloads()
            
            if success:
                print("\n" + "="*70)
                print("🎉 ALL TESTS PASSED!")
                print("="*70)
                print("\n📝 Next steps:")
                print("   1. Check the speedup metric in logs")
                print("   2. Adjust max_download_workers in config.toml if needed")
                print("   3. Run a full video generation task to see overall improvement")
                print()
            else:
                print("\n" + "="*70)
                print("❌ TESTS FAILED - Check errors above")
                print("="*70)
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Test cancelled by user")
            sys.exit(0)
    else:
        print("\n✅ Configuration test complete (download test skipped)")
        print("   Run without --skip-download to test actual downloads\n")
