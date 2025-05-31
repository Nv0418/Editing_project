#!/usr/bin/env python3
"""
Test script to generate videos with JSON-configured subtitle styles
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


def create_json_styled_video(style_name='simple_caption', json_file=None, output_name=None):
    """Create a video with JSON-configured subtitle style"""
    
    print(f"\n🎬 Creating video with JSON style: {style_name}")
    print("=" * 60)
    
    # Paths
    project_root = Path(__file__).resolve().parent
    audio_file = project_root / "other_root_files" / "got_script.mp3"
    transcription_file = project_root / "other_root_files" / "parakeet_output.json"
    
    # Default JSON style file - use v3 (latest) by default
    if json_file is None:
        json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    else:
        json_file = Path(json_file)
    
    # Verify files exist
    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_file}")
        return None
        
    if not transcription_file.exists():
        print(f"ERROR: Transcription file not found: {transcription_file}")
        return None
    
    if not json_file.exists():
        print(f"ERROR: Style JSON file not found: {json_file}")
        return None
    
    # Load style from JSON
    print(f"Loading style from: {json_file}")
    style = StyleLoader.load_style_from_json(json_file, style_name)
    
    if style is None:
        print(f"Failed to load style: {style_name}")
        return None
    
    # Load data
    print("Loading audio and transcription...")
    transcript, words = load_parakeet_data(transcription_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    print(f"Audio duration: {duration:.2f}s")
    print(f"Total words: {len(words)}")
    print(f"Style: {style.config.get('name', style_name)}")
    print(f"Effect type: {style.config.get('effect_type', 'unknown')}")
    
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
    
    # Output path
    output_dir = project_root / "output_test" / "json_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if output_name:
        output_file = output_dir / output_name
    else:
        output_file = output_dir / f"json_styled_{style_name}.mp4"
    
    print(f"\n🎥 Rendering video to: {output_file}")
    print("This may take a few minutes...")
    
    try:
        # Render video
        composition.write_video(
            str(output_file),
            codec='libx264',
            fps=30,
            audio_codec='aac'
        )
        
        print("\n✅ SUCCESS! Video created with JSON-styled subtitles!")
        print(f"📁 Output: {output_file}")
        print(f"📊 Duration: {duration:.2f}s")
        print(f"📊 Resolution: {resolution[0]}x{resolution[1]}")
        
        return str(output_file)
        
    except Exception as e:
        print(f"\n❌ Error rendering video: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_all_json_styles():
    """Test all styles from JSON configuration"""
    
    project_root = Path(__file__).resolve().parent
    json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v2.json"
    
    # Get available styles
    available_styles = StyleLoader.list_available_styles(json_file)
    
    print("🎯 Testing all JSON-configured subtitle styles")
    print("=" * 60)
    print(f"Found {len(available_styles)} styles in {json_file.name}:")
    for style_id, style_name in available_styles.items():
        print(f"  - {style_id}: {style_name}")
    print("=" * 60)
    
    # Test our three main styles
    styles_to_test = ['simple_caption', 'background_caption', 'glow_caption']
    
    results = []
    for style_id in styles_to_test:
        if style_id in available_styles:
            output_file = create_json_styled_video(style_id)
            if output_file:
                results.append((style_id, output_file))
        else:
            print(f"⚠️  Style '{style_id}' not found in JSON")
    
    # Also test the legacy style to ensure backward compatibility
    print("\n📊 Testing backward compatibility with legacy style...")
    legacy_style = 'Background_opacity_style_draft_1'
    if legacy_style in available_styles:
        output_file = create_json_styled_video(legacy_style)
        if output_file:
            results.append((legacy_style, output_file))
    
    print("\n📊 Summary:")
    print("=" * 60)
    for style_id, output_file in results:
        print(f"✅ {style_id}: {output_file}")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate video with JSON-configured styled subtitles')
    parser.add_argument('--style', default='simple_caption',
                       help='Style name from JSON configuration')
    parser.add_argument('--json', help='Path to custom JSON style file')
    parser.add_argument('--all', action='store_true',
                       help='Test all available styles')
    parser.add_argument('--list', action='store_true',
                       help='List available styles')
    
    args = parser.parse_args()
    
    if args.list:
        # List available styles
        project_root = Path(__file__).resolve().parent
        json_file = Path(args.json) if args.json else project_root / "subtitle_styles" / "config" / "subtitle_styles_v2.json"
        styles = StyleLoader.list_available_styles(json_file)
        print("Available styles:")
        for style_id, style_name in styles.items():
            print(f"  {style_id}: {style_name}")
    elif args.all:
        test_all_json_styles()
    else:
        create_json_styled_video(args.style, args.json)