#!/usr/bin/env python3
"""
Test script for 6 caption styles with Game of Thrones audio and word timestamps
Creates videos in /Users/naman/Desktop/movie_py/output_test/30may_test/
"""

import sys
import os
import json
import movis as mv
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from subtitle_styles.core.json_style_loader import StyleLoader, JSONConfiguredStyle
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def create_black_background(duration=25.0, resolution=(1080, 1920)):
    """Create a black background layer"""
    return mv.layer.Rectangle(
        size=resolution,
        color=(0, 0, 0),
        duration=duration
    )

def test_style(style_name, output_path, audio_path, transcript_data):
    """Test a single style with the Game of Thrones transcript"""
    print(f"\n🎬 Testing {style_name}...")
    
    try:
        # Load style from JSON
        json_path = Path("/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json")
        style_instance = StyleLoader.load_style_from_json(json_path, style_name)
        
        if not style_instance:
            print(f"❌ Failed to load style: {style_name}")
            return False
        
        # Create composition
        duration = 25.0  # Approximate duration of the audio
        composition = mv.layer.Composition(size=(1080, 1920), duration=duration)
        
        # Add black background
        bg = mv.layer.Rectangle(
            size=(1080, 1920),
            color=(0, 0, 0),
            duration=duration
        )
        composition.add_layer(bg, name="background")
        
        # Add audio
        if os.path.exists(audio_path):
            audio = mv.layer.Audio(str(audio_path))
            composition.add_layer(audio, name="audio")
        
        # Convert transcript data to words format expected by StyledSubtitleLayer
        words = []
        for item in transcript_data["word_timestamps"]:
            words.append({
                "word": item["word"],
                "start": item["start"],
                "end": item["end"]
            })
        
        # Create styled subtitle layer
        layout = style_instance.json_config.get('layout', {})
        position = layout.get('text_positioning', 'bottom')
        safe_zones = layout.get('safe_zones', True)
        resolution = (1080, 1920)
        
        subtitle_layer = StyledSubtitleLayer(
            words=words,
            style=style_instance,
            resolution=resolution,
            position=position,
            safe_zones=safe_zones
        )
        
        # Add subtitle layer to composition
        composition.add_layer(subtitle_layer, name="subtitles")
        
        # Render video
        print(f"🎯 Rendering {style_name} to {output_path}")
        composition.write_video(str(output_path), codec='libx264', fps=30)
        print(f"✅ {style_name} completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing {style_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Paths
    output_dir = Path("/Users/naman/Desktop/movie_py/output_test/30may_test")
    audio_path = "/Users/naman/Desktop/movie_py/other_root_files/got_script.mp3"
    transcript_path = "/Users/naman/Desktop/movie_py/other_root_files/parakeet_output.json"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load transcript data
    try:
        with open(transcript_path, 'r') as f:
            transcript_data = json.load(f)
        print(f"📝 Loaded transcript: {transcript_data['transcript'][:50]}...")
    except Exception as e:
        print(f"❌ Failed to load transcript: {e}")
        return
    
    # Styles to test
    styles_to_test = [
        "simple_caption",
        "background_caption", 
        "glow_caption",
        "karaoke_style",
        "highlight_caption",
        "deep_diver"
    ]
    
    print(f"🚀 Starting 6-style test with Game of Thrones content")
    print(f"📂 Output directory: {output_dir}")
    print(f"🎵 Audio file: {audio_path}")
    print(f"📄 Transcript: {transcript_path}")
    
    # Test each style
    successful_tests = 0
    for style in styles_to_test:
        output_file = output_dir / f"{style}_got_test.mp4"
        
        if test_style(style, str(output_file), audio_path, transcript_data):
            successful_tests += 1
    
    print(f"\n🎉 Testing completed!")
    print(f"✅ Successful: {successful_tests}/{len(styles_to_test)} styles")
    print(f"📁 Videos saved in: {output_dir}")

if __name__ == "__main__":
    main()