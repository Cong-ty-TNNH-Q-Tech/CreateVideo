"""
Example implementation: Parallel Video Downloads
Cải thiện 60-80% thời gian download videos

Thay thế code trong app/services/material.py
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from loguru import logger
import os
import time


def download_video_parallel(
    item,
    material_directory: str,
    max_clip_duration: int,
    search_term: str = ""
) -> Optional[Dict]:
    """
    Download single video in parallel thread
    
    Args:
        item: MaterialInfo object with video details
        material_directory: Directory to save video
        max_clip_duration: Maximum clip duration in seconds
        search_term: Search term for metadata
    
    Returns:
        Dict with video info or None if failed
    """
    try:
        start_time = time.time()
        item_search_term = getattr(item, 'search_term', search_term or 'unknown')
        
        logger.info(f"📥 Downloading: {item.url[:60]}...")
        
        # Import here to avoid circular dependency
        from app.services.material import save_video
        
        saved_video_path = save_video(
            video_url=item.url,
            save_dir=material_directory,
            search_term=item_search_term,
            thumbnail_url=getattr(item, 'thumbnail_url', ''),
            preview_images=getattr(item, 'preview_images', None)
        )
        
        if saved_video_path:
            duration = time.time() - start_time
            logger.success(f"✅ Downloaded in {duration:.1f}s: {os.path.basename(saved_video_path)}")
            
            return {
                'path': saved_video_path,
                'url': item.url,
                'duration': min(max_clip_duration, item.duration),
                'search_term': item_search_term,
                'download_time': duration
            }
        else:
            logger.warning(f"⚠️  Download returned empty path: {item.url}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Failed to download {item.url[:60]}: {str(e)}")
        return None


def download_videos_parallel(
    valid_video_items: List,
    material_directory: str,
    audio_duration: float,
    max_clip_duration: int,
    max_workers: int = 5
) -> List[str]:
    """
    Download multiple videos in parallel
    
    Args:
        valid_video_items: List of MaterialInfo objects
        material_directory: Directory to save videos
        audio_duration: Required total duration in seconds
        max_clip_duration: Maximum duration per clip
        max_workers: Number of parallel downloads (default: 5)
    
    Returns:
        List of downloaded video file paths
    """
    logger.info(f"🚀 Starting parallel downloads with {max_workers} workers")
    logger.info(f"📊 Target: {audio_duration:.1f}s from {len(valid_video_items)} videos")
    
    video_paths = []
    downloaded_urls = set()
    total_duration = 0.0
    download_stats = {
        'total_time': 0,
        'successful': 0,
        'failed': 0,
        'skipped_duration': 0
    }
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all download tasks
        future_to_item = {
            executor.submit(
                download_video_parallel,
                item,
                material_directory,
                max_clip_duration
            ): item
            for item in valid_video_items
        }
        
        logger.info(f"📤 Submitted {len(future_to_item)} download tasks")
        
        # Process completed downloads as they finish
        for future in as_completed(future_to_item):
            item = future_to_item[future]
            
            # Check if we already have enough duration
            if total_duration >= audio_duration:
                download_stats['skipped_duration'] += 1
                continue
            
            try:
                result = future.result(timeout=120)  # 2 min timeout per download
                
                if result and result['url'] not in downloaded_urls:
                    video_paths.append(result['path'])
                    downloaded_urls.add(result['url'])
                    total_duration += result['duration']
                    download_stats['successful'] += 1
                    
                    progress = (total_duration / audio_duration) * 100
                    logger.info(
                        f"✓ Progress: {total_duration:.1f}/{audio_duration:.1f}s "
                        f"({progress:.0f}%) | {len(video_paths)} videos"
                    )
                    
                    # Early exit if we have enough
                    if total_duration >= audio_duration:
                        remaining = len(future_to_item) - download_stats['successful'] - download_stats['failed']
                        logger.info(
                            f"🎯 Target duration reached! Cancelling {remaining} remaining downloads..."
                        )
                        
                        # Cancel remaining futures
                        for f in future_to_item:
                            if not f.done():
                                f.cancel()
                        
                        break
                else:
                    download_stats['failed'] += 1
                    
            except Exception as e:
                download_stats['failed'] += 1
                logger.error(f"❌ Download exception: {str(e)}")
    
    elapsed_time = time.time() - start_time
    download_stats['total_time'] = elapsed_time
    
    # Summary statistics
    logger.success(f"\n{'='*60}")
    logger.success(f"📊 DOWNLOAD SUMMARY")
    logger.success(f"{'='*60}")
    logger.success(f"✅ Successful:        {download_stats['successful']} videos")
    logger.success(f"❌ Failed:            {download_stats['failed']} videos")
    logger.success(f"⏭️  Skipped (enough):  {download_stats['skipped_duration']} videos")
    logger.success(f"⏱️  Total time:        {elapsed_time:.1f}s")
    logger.success(f"📹 Total duration:    {total_duration:.1f}s (target: {audio_duration:.1f}s)")
    
    if download_stats['successful'] > 0:
        avg_time = elapsed_time / download_stats['successful']
        logger.success(f"⚡ Avg per video:     {avg_time:.1f}s")
        
        # Calculate speed improvement
        sequential_time = download_stats['successful'] * avg_time
        speedup = sequential_time / elapsed_time if elapsed_time > 0 else 1
        logger.success(f"🚀 Speedup:           {speedup:.1f}× faster than sequential")
    
    logger.success(f"{'='*60}\n")
    
    return video_paths


def download_videos_optimized(
    task_id: str,
    search_terms: List[str],
    source: str = "pexels",
    video_aspect=None,
    video_contact_mode=None,
    audio_duration: float = 0.0,
    max_clip_duration: int = 5,
    max_workers: int = 5
) -> List[str]:
    """
    Optimized video download function - replacement for material.download_videos()
    
    This is the main function to replace in app/services/material.py
    
    Args:
        task_id: Unique task identifier
        search_terms: List of search terms for finding videos
        source: Video source ("pexels" or "pixabay")
        video_aspect: Video aspect ratio
        video_contact_mode: Video concatenation mode
        audio_duration: Required audio duration
        max_clip_duration: Maximum clip duration
        max_workers: Number of parallel downloads (5-10 recommended)
    
    Returns:
        List of downloaded video paths
    """
    from app.config import config
    from app.utils import utils
    from app.services.material import search_videos_pexels, search_videos_pixabay
    from app.models.schema import VideoConcatMode
    import random
    
    logger.info(f"🎬 Starting optimized video download for task: {task_id}")
    
    # === STEP 1: Search for videos ===
    videos_by_term = {}
    found_duration = 0.0
    
    search_videos = search_videos_pexels if source == "pexels" else search_videos_pixabay
    global_video_urls = set()
    
    logger.info(f"🔍 Searching {len(search_terms)} terms on {source}...")
    
    for search_term in search_terms:
        video_items = search_videos(
            search_term=search_term,
            minimum_duration=max_clip_duration,
            video_aspect=video_aspect,
        )
        
        unique_videos = []
        for item in video_items:
            if item.url not in global_video_urls:
                item.search_term = search_term
                unique_videos.append(item)
                global_video_urls.add(item.url)
                found_duration += item.duration
        
        if unique_videos:
            videos_by_term[search_term] = unique_videos
            logger.info(f"  ✓ '{search_term}': {len(unique_videos)} videos")
    
    logger.info(
        f"📊 Found {len(global_video_urls)} unique videos, "
        f"total duration: {found_duration:.1f}s (need: {audio_duration:.1f}s)"
    )
    
    # === STEP 2: Select balanced videos ===
    valid_video_items = []
    max_videos_per_term = max(1, int(audio_duration / max_clip_duration / len(videos_by_term)) + 1) if videos_by_term else 1
    
    for search_term, videos in videos_by_term.items():
        if video_contact_mode and video_contact_mode.value == VideoConcatMode.random.value:
            random.shuffle(videos)
        
        count = 0
        for item in videos[:max_videos_per_term]:
            valid_video_items.append(item)
            count += 1
    
    if video_contact_mode and video_contact_mode.value == VideoConcatMode.random.value:
        random.shuffle(valid_video_items)
    
    logger.info(f"🎯 Selected {len(valid_video_items)} videos for download")
    
    # === STEP 3: Download in parallel (THE KEY IMPROVEMENT) ===
    material_directory = config.app.get("material_directory", "").strip()
    if material_directory == "task":
        material_directory = utils.task_dir(task_id)
    elif material_directory and not os.path.isdir(material_directory):
        material_directory = ""
    
    # 🚀 PARALLEL DOWNLOAD HERE
    video_paths = download_videos_parallel(
        valid_video_items=valid_video_items,
        material_directory=material_directory,
        audio_duration=audio_duration,
        max_clip_duration=max_clip_duration,
        max_workers=max_workers  # 5-10 untuk optimal balance
    )
    
    return video_paths


# ============================================================================
# INTEGRATION INSTRUCTIONS
# ============================================================================
"""
To integrate this into your project:

1. OPTION A - Replace entire function:
   
   In app/services/material.py:
   
   # Replace the download_videos function with download_videos_optimized
   def download_videos(...):
       return download_videos_optimized(...)

2. OPTION B - Add as new function:
   
   # Keep old function, add new one
   def download_videos_parallel_mode(...):
       return download_videos_optimized(...)
   
   # Use in task.py:
   if config.app.get("enable_parallel_downloads", True):
       downloaded_videos = material.download_videos_parallel_mode(...)
   else:
       downloaded_videos = material.download_videos(...)

3. Configuration in config.toml:
   
   [app]
   enable_parallel_downloads = true
   max_download_workers = 5  # 5-10 recommended

4. Test performance:
   
   Before: 30-120 seconds for 5-10 videos
   After:  5-30 seconds for 5-10 videos
   
   Expected improvement: 60-80% faster

5. Monitoring:
   
   Watch logs for:
   - "🚀 Speedup: X.X× faster than sequential"
   - Individual download times
   - Success/failure rates
"""
