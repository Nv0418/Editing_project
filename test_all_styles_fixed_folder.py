#!/usr/bin/env python3
"""
Test script for all subtitle styles in v3 configuration
Creates videos named by style only in test_result folder
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
    
    # Load style from JSON
    style = StyleLoader.load_style_from_json(json_file, style_name)
    
    if style is None:
        print(f"Failed to load style: {style_name}")
        return False
    
    # Load data
    transcript, words = load_parakeet_data(transcription_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    print(f"Style: {style.config.get('name', style_name)}")
    print(f"Description: {style.config.get('description', 'N/A')}")
    print(f"Effect type: {style.config.get('effect_type', 'unknown')}")
    print(f"Font: {Path(style.config['typography']['font_family']).name}")
    
    # Create composition
    resolution = tuple(style.config['format']['resolution'])
    composition = mv.layer.Composition(size=resolution, duration=duration)
    
    # Add black background
    background = mv.layer.Rectangle(
        size=resolution,
        color=(0, 0, 0),
        duration=duration
    )
    composition.add_layer(background, name="background")
    
    # Add audio
    composition.add_layer(audio_layer, name="audio")
    
    # Create styled subtitle layer
    layout = style.config.get('layout', {})
    position = layout.get('text_positioning', 'bottom')
    safe_zones = layout.get('safe_zones', True)
    
    subtitle_layer = StyledSubtitleLayer(
        words=words,
        style=style,
        resolution=resolution,
        position=position,
        safe_zones=safe_zones
    )
    
    # Add subtitle layer to composition
    composition.add_layer(subtitle_layer, name="subtitles")
    
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


def test_all_v3_styles():
    """Test all styles from v3 configuration"""
    
    project_root = Path(__file__).resolve().parent
    json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    
    if not json_file.exists():
        print(f"ERROR: v3 configuration not found: {json_file}")
        return
    
    # Use fixed test_result directory
    test_dir = project_root / "output_test" / "test_result"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🎯 VinVideo Subtitle Styles Comprehensive Test")
    print("=" * 60)
    print(f"Configuration: {json_file.name}")
    print(f"Output directory: {test_dir}")
    print("=" * 60)
    
    # Get all available styles
    available_styles = StyleLoader.list_available_styles(json_file)
    
    # Skip draft/planned styles
    styles_to_test = []
    for style_id, style_name in available_styles.items():
        if "draft" not in style_id.lower() and "planned" not in style_name.lower():
            styles_to_test.append(style_id)
    
    print(f"Found {len(styles_to_test)} styles to test:")
    for style_id in styles_to_test:
        print(f"  - {style_id}: {available_styles[style_id]}")
    print("=" * 60)
    
    # Test each style
    results = {
        "success": [],
        "failed": []
    }
    
    for i, style_id in enumerate(styles_to_test, 1):
        print(f"\n[{i}/{len(styles_to_test)}] Processing: {style_id}")
        
        success = create_test_video(style_id, json_file, test_dir)
        
        if success:
            results["success"].append(style_id)
        else:
            results["failed"].append(style_id)
    
    # Create summary report
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total styles tested: {len(styles_to_test)}")
    print(f"✅ Successful: {len(results['success'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results["success"]:
        print("\nSuccessful styles:")
        for style_id in results["success"]:
            print(f"  ✅ {style_id}")
    
    if results["failed"]:
        print("\nFailed styles:")
        for style_id in results["failed"]:
            print(f"  ❌ {style_id}")
    
    # Create a summary file
    summary_file = test_dir / "test_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("VinVideo Subtitle Styles Test Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Configuration: {json_file.name}\n")
        f.write(f"Total styles tested: {len(styles_to_test)}\n")
        f.write(f"Successful: {len(results['success'])}\n")
        f.write(f"Failed: {len(results['failed'])}\n")
        f.write("\nSuccessful styles:\n")
        for style_id in results["success"]:
            style_name = available_styles.get(style_id, style_id)
            f.write(f"  - {style_id}: {style_name}\n")
        if results["failed"]:
            f.write("\nFailed styles:\n")
            for style_id in results["failed"]:
                style_name = available_styles.get(style_id, style_id)
                f.write(f"  - {style_id}: {style_name}\n")
    
    print(f"\n📁 All test videos saved to: {test_dir}")
    print(f"📄 Summary report: {summary_file}")
    
    return test_dir, results


if __name__ == "__main__":
    test_all_v3_styles()
