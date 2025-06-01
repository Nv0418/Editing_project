#!/usr/bin/env python3
"""
Simple test script to generate videos for all subtitle styles using Game of Thrones images
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import movis as mv
from movis.transform import Transform
from pathlib import Path
import json
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer
from datetime import datetime
import numpy as np
from PIL import Image


def load_parakeet_data(json_path):
    """Load parakeet transcription data"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    words = []
    for item in data["word_timestamps"]:
        words.append({
            "word": item["word"],
            "start": item["start"],
            "end": item["end"]
        })
    return data["transcript"], words


def create_got_video_with_style(style_name, output_dir):
    """Create a test video for a specific style with Game of Thrones images"""
    
    print(f"\n🎬 Testing style: {style_name}")
    print("-" * 40)
    
    # Paths
    project_root = Path(__file__).resolve().parent
    audio_file = project_root / "other_root_files" / "got_script.mp3"
    transcription_file = project_root / "other_root_files" / "parakeet_output.json"
    json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    images_dir = project_root / "game_of_thrones_images"
    
    # Verify files exist
    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_file}")
        return False
        
    if not transcription_file.exists():
        print(f"ERROR: Transcription file not found: {transcription_file}")
        return False
    
    if not json_file.exists():
        print(f"ERROR: JSON config not found: {json_file}")
        return False
    
    # Get all images
    images = sorted([str(images_dir / f) for f in os.listdir(images_dir) if f.endswith('.png')])
    if not images:
        print(f"ERROR: No images found in {images_dir}")
        return False
    
    print(f"Found {len(images)} images")
    
    try:
        # Load audio to get duration
        audio = mv.layer.Audio(str(audio_file))
        duration = audio.duration
        
        # Create base composition
        scene = mv.layer.Composition(size=(1080, 1920), duration=duration)
        
        # Calculate duration for each image
        image_duration = duration / len(images)
        
        # Create image slideshow
        for i, image_path in enumerate(images):
            # Load and resize image to fit
            img = Image.open(image_path)
            
            # Calculate scale to fit in 1080x1920
            img_w, img_h = img.size
            scale_w = 1080 / img_w
            scale_h = 1920 / img_h
            scale = min(scale_w, scale_h)  # Use smaller scale to ensure it fits
            
            # Create image layer with transform
            img_layer = mv.layer.Image(
                image_path, 
                duration=image_duration,
                transform=Transform(
                    scale=(scale, scale),
                    position=(540, 960),  # Center of 1080x1920
                    anchor_point=(img_w/2, img_h/2)  # Center of original image
                )
            )
            
            # Set timing offset
            img_layer = img_layer.with_offset(i * image_duration)
            
            # Add to scene
            scene.add_layer(img_layer)
        
        # Add audio
        scene.add_layer(audio)
        
        # Load subtitle configuration
        style_loader = StyleLoader(str(json_file))
        
        # Load transcription data
        transcript, word_timestamps = load_parakeet_data(str(transcription_file))
        
        # Create and add subtitle layer
        subtitle_layer = StyledSubtitleLayer(
            style_config=style_loader.get_style(style_name),
            word_timestamps=word_timestamps,
            duration=duration
        )
        scene.add_layer(subtitle_layer)
        
        # Create output filename
        output_file = output_dir / f"{style_name}_got.mp4"
        
        print(f"📹 Rendering {style_name}...")
        
        # Render with high quality
        scene.write_video(
            str(output_file),
            codec='libx264',
            crf=23,
            preset='medium',
            pix_fmt='yuv420p',
            audio_codec='aac',
            audio_bitrate='192k'
        )
        
        print(f"✅ Success: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_all_styles():
    """Test all subtitle styles from the config"""
    
    # Load subtitle styles config
    json_file = Path("subtitle_styles/config/subtitle_styles_v3.json")
    with open(json_file, 'r') as f:
        styles_config = json.load(f)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output_test/got_styles_test_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all style names
    style_names = list(styles_config.keys())
    
    print(f"\n{'='*60}")
    print(f"Testing {len(style_names)} subtitle styles with Game of Thrones images")
    print(f"{'='*60}")
    for style in style_names:
        print(f"  - {style}")
    
    # Process each style
    successful_styles = []
    failed_styles = []
    
    for i, style_name in enumerate(style_names, 1):
        print(f"\n[{i}/{len(style_names)}] Processing...")
        
        success = create_got_video_with_style(style_name, output_dir)
        
        if success:
            successful_styles.append(style_name)
        else:
            failed_styles.append(style_name)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY - Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"Total styles tested: {len(style_names)}")
    print(f"Successful: {len(successful_styles)}")
    print(f"Failed: {len(failed_styles)}")
    print(f"\nOutput directory: {output_dir}")
    
    if successful_styles:
        print(f"\nSuccessful styles ({len(successful_styles)}):")
        for style in successful_styles:
            print(f"  ✓ {style}")
    
    if failed_styles:
        print(f"\nFailed styles ({len(failed_styles)}):")
        for style in failed_styles:
            print(f"  ✗ {style}")
    
    print(f"\nAll videos saved to: {output_dir}/")


if __name__ == "__main__":
    test_all_styles()