#!/usr/bin/env python3
"""
Simple test script to generate videos for all subtitle styles with black background
Focus on testing subtitle styles, not image handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import movis as mv
from pathlib import Path
import json
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer
from datetime import datetime


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


def create_style_video_simple(style_name, output_dir):
    """Create a test video for a specific style with black background"""
    
    print(f"\n🎬 Testing style: {style_name}")
    print("-" * 40)
    
    # Paths
    project_root = Path(__file__).resolve().parent
    audio_file = project_root / "other_root_files" / "got_script.mp3"
    transcription_file = project_root / "other_root_files" / "parakeet_output.json"
    json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    
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
    
    try:
        # Load audio to get duration
        audio = mv.layer.Audio(str(audio_file))
        duration = audio.duration
        
        # Create base composition
        scene = mv.layer.Composition(size=(1080, 1920), duration=duration)
        
        # Add black background
        background = mv.layer.Rectangle(
            size=(1080, 1920),
            duration=duration,
            color=(0, 0, 0)  # Black background
        )
        scene.add_layer(background, name='background')
        
        # Add audio
        scene.add_layer(audio, name='audio')
        
        # Load subtitle configuration
        style_config = StyleLoader.load_style_from_json(json_file, style_name)
        if not style_config:
            print(f"ERROR: Failed to load style {style_name}")
            return False
        
        # Load transcription data
        transcript, word_timestamps = load_parakeet_data(str(transcription_file))
        
        # Create and add subtitle layer
        subtitle_layer = StyledSubtitleLayer(
            words=word_timestamps,
            style=style_config,
            resolution=(1080, 1920),
            position="bottom",
            safe_zones=True
        )
        scene.add_layer(subtitle_layer, name='subtitles')
        
        # Create output filename
        output_file = output_dir / f"{style_name}_got_black_bg.mp4"
        
        print(f"📹 Rendering {style_name}...")
        
        # Render video
        scene.write_video(
            str(output_file),
            fps=30,
            audio_codec='aac'
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
    output_dir = Path(f"output_test/got_styles_black_bg_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all style names
    style_names = list(styles_config.keys())
    
    print(f"\n{'='*60}")
    print(f"Testing {len(style_names)} subtitle styles (Black Background)")
    print(f"{'='*60}")
    for style in style_names:
        print(f"  - {style}")
    
    # Process each style
    successful_styles = []
    failed_styles = []
    
    for i, style_name in enumerate(style_names, 1):
        print(f"\n[{i}/{len(style_names)}] Processing...")
        
        success = create_style_video_simple(style_name, output_dir)
        
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
    
    # Verification summary
    print(f"\n{'='*60}")
    print("SUBTITLE STYLES VERIFICATION")
    print(f"{'='*60}")
    print(f"✅ Total styles in config: {len(style_names)}")
    print(f"✅ Includes GREENGOBLIN: {'greengoblin' in style_names}")
    print(f"✅ Includes SGONE: {'sgone_caption' in style_names}")
    print(f"\nAll {len(style_names)} styles tested:")
    for i, style in enumerate(style_names, 1):
        status = "✓" if style in successful_styles else "✗"
        print(f"{i:2d}. {status} {style}")


if __name__ == "__main__":
    test_all_styles()