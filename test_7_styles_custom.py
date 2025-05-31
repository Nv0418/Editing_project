#!/usr/bin/env python3
"""
Test script for all 7 finalized subtitle styles
Outputs to /Users/naman/Desktop/movie_py/30may_test/test_results_7/
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import movis as mv
from pathlib import Path
import json
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer


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


def create_test_video(style_name, json_file, output_dir):
    """Create a test video for a specific style"""
    
    print(f"\n🎬 Testing style: {style_name}")
    print("-" * 40)
    
    # Paths
    project_root = Path(__file__).resolve().parent
    audio_file = project_root / "other_root_files" / "got_script.mp3"
    transcription_file = project_root / "other_root_files" / "parakeet_output.json"
    
    # Verify files exist
    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_file}")
        return False
        
    if not transcription_file.exists():
        print(f"ERROR: Transcription file not found: {transcription_file}")
        return False
    
    # Load style
    style = StyleLoader.load_style_from_json(json_file, style_name)
    if not style:
        print(f"ERROR: Could not load style: {style_name}")
        return False
    
    # Get style info
    config = style.config
    style_display_name = config.get('name', style_name)
    description = config.get('description', 'No description')
    effect_type = config.get('effect_type', 'unknown')
    
    print(f"Style: {style_display_name}")
    print(f"Description: {description}")
    print(f"Effect type: {effect_type}")
    
    # Load transcription and audio
    transcript, words = load_parakeet_data(transcription_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    # Create composition
    composition = mv.layer.Composition(
        size=(1080, 1920),  # 9:16 aspect ratio
        duration=duration
    )
    
    # Add black background
    background = mv.layer.Rectangle(
        size=(1080, 1920),
        duration=duration,
        color=(0, 0, 0)
    )
    composition.add_layer(background, name='background')
    
    # Create subtitle layer
    subtitle_layer = StyledSubtitleLayer(
        words=words,
        style=style,
        resolution=(1080, 1920),
        position="bottom",
        safe_zones=True
    )
    composition.add_layer(subtitle_layer, name='subtitles')
    composition.add_layer(audio_layer, name='audio')
    
    # Output file - named with style name only
    output_file = output_dir / f"{style_name}.mp4"
    
    print(f"Rendering to: {output_file.name}")
    
    try:
        # Render video
        composition.write_video(
            str(output_file),
            codec='libx264',
            fps=30,
            audio_codec='aac'
        )
        
        print(f"✅ Success: {style_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error rendering {style_name}: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_7_finalized_styles():
    """Test the 7 finalized styles"""
    
    project_root = Path(__file__).resolve().parent
    json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    
    if not json_file.exists():
        print(f"ERROR: v3 configuration not found: {json_file}")
        return
    
    # Use custom output directory
    test_dir = Path("/Users/naman/Desktop/movie_py/30may_test/test_results_7")
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🎯 VinVideo 7 Finalized Subtitle Styles Test")
    print("=" * 60)
    print(f"Configuration: {json_file.name}")
    print(f"Output directory: {test_dir}")
    print("=" * 60)
    
    # Define the 7 finalized styles
    finalized_styles = [
        "simple_caption",
        "background_caption", 
        "glow_caption",
        "karaoke_style",
        "highlight_caption",
        "deep_diver",
        "popling_caption"
    ]
    
    # Get style info
    available_styles = StyleLoader.list_available_styles(json_file)
    
    print(f"Testing {len(finalized_styles)} finalized styles:")
    for style_key in finalized_styles:
        style_name = available_styles.get(style_key, style_key)
        print(f"  - {style_key}: {style_name}")
    print("=" * 60)
    
    # Test each style
    successful = 0
    failed = 0
    
    for i, style_key in enumerate(finalized_styles, 1):
        print(f"\n[{i}/{len(finalized_styles)}] Processing: {style_key}")
        
        success = create_test_video(style_key, json_file, test_dir)
        if success:
            successful += 1
        else:
            failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 FINAL RESULTS")
    print("=" * 60)
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Output directory: {test_dir}")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 All 7 finalized styles rendered successfully!")
    else:
        print(f"⚠️  {failed} style(s) failed to render")


if __name__ == "__main__":
    test_7_finalized_styles()