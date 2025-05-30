#!/usr/bin/env python3
"""
Test script for the resized DeepDiver style with smaller background box
"""

import sys
import os
import json
import movis as mv
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def test_deepdiver_resized():
    """Test the resized DeepDiver style with smaller background box"""
    
    print("🎨 Testing DeepDiver with smaller background box...")
    
    # Paths
    output_dir = Path("/Users/naman/Desktop/movie_py/output_test/30may_test")
    audio_path = "/Users/naman/Desktop/movie_py/other_root_files/got_script.mp3"
    transcript_path = "/Users/naman/Desktop/movie_py/other_root_files/parakeet_output.json"
    
    # Load transcript data
    with open(transcript_path, 'r') as f:
        transcript_data = json.load(f)
    
    # Convert to words format
    words = []
    for item in transcript_data["word_timestamps"]:
        words.append({
            "word": item["word"],
            "start": item["start"],
            "end": item["end"]
        })
    
    # Load DeepDiver style
    json_path = Path("/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json")
    style_instance = StyleLoader.load_style_from_json(json_path, "deep_diver")
    
    if not style_instance:
        print("❌ Failed to load deep_diver style")
        return False
    
    print(f"📝 Background padding: x={style_instance.json_config['effect_parameters']['background_padding']['x']}, y={style_instance.json_config['effect_parameters']['background_padding']['y']}")
    
    # Create composition
    duration = 25.0
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
    
    # Output path
    output_file = output_dir / "deep_diver_RESIZED_box.mp4"
    
    # Render video
    print(f"🎯 Rendering resized DeepDiver to {output_file}")
    composition.write_video(str(output_file), codec='libx264', fps=30)
    print(f"✅ DeepDiver resized box test completed!")
    
    return True

if __name__ == "__main__":
    test_deepdiver_resized()