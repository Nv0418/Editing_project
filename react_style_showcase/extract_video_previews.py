#!/usr/bin/env python3
"""
Extract preview frames from actual rendered videos
This ensures previews EXACTLY match the video output
"""

import os
import sys
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Preview configuration
PREVIEW_SIZE = (400, 220)

# Map of style names to their video files
STYLE_VIDEO_MAPPING = {
    'simple_caption': 'simple_caption.mp4',
    'background_caption': 'background_caption.mp4',
    'glow_caption': 'glow_caption.mp4',
    'karaoke_style': 'karaoke_style.mp4',
    'highlight_caption': 'highlight_caption.mp4',
    'deep_diver': 'deep_diver.mp4',
    'popling_caption': 'popling_caption.mp4',
    'greengoblin': 'greengoblin.mp4',
    'sgone_caption': 'sgone_caption.mp4'  # We'll need to generate this one
}

# Style display names
STYLE_NAMES = {
    'simple_caption': 'SIMPLE CAPTION',
    'background_caption': 'BACKGROUND CAPTION',
    'glow_caption': 'GLOW CAPTION',
    'karaoke_style': 'KARAOKE STYLE',
    'highlight_caption': 'HIGHLIGHT CAPTION',
    'deep_diver': 'DEEP DIVER',
    'popling_caption': 'POPLING CAPTION',
    'greengoblin': 'GREEN GOBLIN',
    'sgone_caption': 'SGONE CAPTION'
}

def extract_frame_from_video(video_path, output_path, timestamp=2.0):
    """Extract a frame from video at specific timestamp"""
    try:
        # Use ffmpeg to extract frame
        cmd = [
            'ffmpeg',
            '-ss', str(timestamp),  # Seek to timestamp
            '-i', str(video_path),  # Input video
            '-vframes', '1',  # Extract 1 frame
            '-q:v', '2',  # High quality
            '-y',  # Overwrite output
            str(output_path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        return True
    except Exception as e:
        print(f"Error extracting frame: {e}")
        return False

def create_preview_from_frame(style_id, frame_path, output_path):
    """Create preview image from extracted frame"""
    try:
        # Open the frame
        frame = Image.open(frame_path)
        
        # Crop to 9:16 aspect ratio centered
        width, height = frame.size
        target_aspect = 9/16
        current_aspect = width/height
        
        if current_aspect > target_aspect:
            # Too wide, crop width
            new_width = int(height * target_aspect)
            left = (width - new_width) // 2
            frame = frame.crop((left, 0, left + new_width, height))
        else:
            # Too tall, crop height
            new_height = int(width / target_aspect)
            top = (height - new_height) // 2
            frame = frame.crop((0, top, width, top + new_height))
        
        # Resize to preview size
        frame = frame.resize(PREVIEW_SIZE, Image.Resampling.LANCZOS)
        
        # Add style name overlay
        draw = ImageDraw.Draw(frame)
        style_name = STYLE_NAMES.get(style_id, style_id.upper())
        
        # Load font for style name
        try:
            name_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        except:
            name_font = ImageFont.load_default()
        
        # Add semi-transparent background for name
        overlay = Image.new('RGBA', PREVIEW_SIZE, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        # Draw background bar at bottom
        bar_height = 40
        overlay_draw.rectangle([0, PREVIEW_SIZE[1] - bar_height, PREVIEW_SIZE[0], PREVIEW_SIZE[1]], 
                              fill=(0, 0, 0, 200))
        
        # Composite overlay
        frame = Image.alpha_composite(frame.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(frame)
        
        # Draw style name
        text_y = PREVIEW_SIZE[1] - bar_height // 2
        draw.text((PREVIEW_SIZE[0] // 2, text_y), style_name, 
                 font=name_font, fill=(255, 255, 255), anchor="mm")
        
        # Save preview
        frame.save(output_path, quality=95)
        print(f"✓ Created preview: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating preview: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Extract previews from existing test videos"""
    # Paths
    project_root = Path(__file__).parent.parent
    video_dir = project_root / "output_test" / "test_result_20250530_210541"
    output_dir = Path(__file__).parent / "subtitle_preview_app" / "public" / "style_previews"
    temp_dir = Path(__file__).parent / "temp_frames"
    
    # Create directories
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    print("Extracting previews from rendered videos...")
    print(f"Looking for videos in: {video_dir}")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    
    for style_id, video_filename in STYLE_VIDEO_MAPPING.items():
        video_path = video_dir / video_filename
        
        if not video_path.exists():
            print(f"⚠️  Video not found: {video_path}")
            continue
        
        # Extract frame
        temp_frame = temp_dir / f"{style_id}_frame.png"
        if extract_frame_from_video(video_path, temp_frame):
            # Create preview
            output_path = output_dir / f"{style_id}.png"
            if create_preview_from_frame(style_id, temp_frame, output_path):
                success_count += 1
            
            # Clean up temp frame
            temp_frame.unlink(missing_ok=True)
    
    # Clean up temp directory
    temp_dir.rmdir()
    
    print(f"\nExtracted {success_count}/{len(STYLE_VIDEO_MAPPING)} previews successfully!")

if __name__ == "__main__":
    main()