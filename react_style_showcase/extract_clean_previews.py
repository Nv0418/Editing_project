#!/usr/bin/env python3
"""
Extract clean preview frames without stretching or style names
"""

import os
import sys
from pathlib import Path
import subprocess
from PIL import Image

# Preview configuration
# We want a wider preview that shows the subtitle area well
PREVIEW_WIDTH = 320
PREVIEW_HEIGHT = 180  # 16:9 aspect ratio for preview cards

print(f"Preview dimensions: {PREVIEW_WIDTH}x{PREVIEW_HEIGHT}")

# All styles with their video locations
STYLE_VIDEO_MAPPING = {
    'simple_caption': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/simple_caption.mp4',
    'background_caption': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/background_caption.mp4',
    'glow_caption': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/glow_caption.mp4',
    'karaoke_style': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/karaoke_style.mp4',
    'highlight_caption': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/highlight_caption.mp4',
    'deep_diver': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/deep_diver.mp4',
    'popling_caption': '/Users/naman/Desktop/movie_py/output_test/test_result_20250530_210541/popling_caption.mp4',
    'greengoblin': '/Users/naman/Desktop/movie_py/output_test/json_test/json_styled_greengoblin.mp4',
    'sgone_caption': '/Users/naman/Desktop/movie_py/output_test/json_test/json_styled_sgone_caption.mp4'
}

def extract_and_resize_frame(video_path, output_path, timestamp=2.0):
    """Extract frame focusing on subtitle area"""
    try:
        # First extract full frame to get dimensions
        temp_frame = output_path.parent / f"temp_{output_path.name}"
        
        # Extract full frame first
        cmd1 = [
            'ffmpeg',
            '-ss', str(timestamp),
            '-i', str(video_path),
            '-vframes', '1',
            '-q:v', '2',
            '-y',
            str(temp_frame)
        ]
        
        result = subprocess.run(cmd1, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
        
        # Open the frame to get dimensions
        img = Image.open(temp_frame)
        width, height = img.size
        
        # For 9:16 videos, we want to crop the bottom area where subtitles appear
        # Take bottom 40% of the video which should contain the subtitles
        crop_height = int(height * 0.4)
        crop_y = height - crop_height
        
        # Use ffmpeg to crop and resize
        cmd2 = [
            'ffmpeg',
            '-i', str(temp_frame),
            '-vf', f'crop={width}:{crop_height}:0:{crop_y},scale={PREVIEW_WIDTH}:{PREVIEW_HEIGHT}',
            '-q:v', '2',
            '-y',
            str(output_path)
        ]
        
        result = subprocess.run(cmd2, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            temp_frame.unlink(missing_ok=True)
            return False
        
        # Clean up temp frame
        temp_frame.unlink(missing_ok=True)
        
        print(f"✓ Extracted: {output_path}")
        return True
    except Exception as e:
        print(f"Error extracting frame: {e}")
        return False

def main():
    """Extract clean previews for all styles"""
    output_dir = Path(__file__).parent / "subtitle_preview_app" / "public" / "style_previews"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Extracting clean previews without style names...")
    print(f"Output directory: {output_dir}\n")
    
    success_count = 0
    
    for style_id, video_path in STYLE_VIDEO_MAPPING.items():
        if not Path(video_path).exists():
            print(f"⚠️  Video not found: {video_path}")
            continue
            
        output_path = output_dir / f"{style_id}.png"
        
        # Try different timestamps to get a good frame with text
        timestamps = [2.0, 3.0, 4.0, 5.0]
        
        for timestamp in timestamps:
            if extract_and_resize_frame(video_path, output_path, timestamp):
                success_count += 1
                break
        else:
            print(f"❌ Failed to extract preview for {style_id}")
    
    print(f"\n✅ Extracted {success_count}/{len(STYLE_VIDEO_MAPPING)} previews successfully!")
    print(f"Preview size: {PREVIEW_WIDTH}x{PREVIEW_HEIGHT} (maintains 9:16 aspect ratio)")

if __name__ == "__main__":
    main()