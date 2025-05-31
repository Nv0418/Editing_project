#!/usr/bin/env python3
"""
Test script for Simple Caption style
Clean, educational text for tutorials and how-to content
"""
import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def load_parakeet_data(file_path):
    """Load word timestamps from Parakeet JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['word_timestamps']

def create_simple_caption_video():
    """Create a video with Simple Caption style."""
    
    # Configuration
    resolution = (1080, 1920)  # Instagram 9:16 format
    fps = 30
    
    # File paths
    project_root = os.path.join(os.path.dirname(__file__), '..', '..')
    parakeet_file = os.path.join(project_root, 'other_root_files', 'parakeet_output.json')
    audio_file = os.path.join(project_root, 'other_root_files', 'got_script.mp3')
    output_file = os.path.join(os.path.dirname(__file__), 'simple_caption_test.mp4')
    json_style_file = os.path.join(project_root, 'subtitle_styles', 'config', 'subtitle_styles_v3.json')
    
    # Load word timestamps
    word_timestamps = load_parakeet_data(parakeet_file)
    
    # Load audio to get duration
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    # Load Simple Caption style configuration
    style = StyleLoader.load_style_from_json(json_style_file, "simple_caption")
    
    # Create composition
    scene = mv.layer.Composition(
        size=resolution,
        duration=duration
    )
    
    # Add black background
    background = mv.layer.Rectangle(
        size=resolution,
        duration=duration,
        color=(0, 0, 0)
    )
    scene.add_layer(background, name='background')
    
    # Create subtitle layer
    subtitle_layer = StyledSubtitleLayer(
        words=word_timestamps,
        style=style,
        resolution=resolution,
        position="bottom",
        safe_zones=True
    )
    
    # Add layers
    scene.add_layer(subtitle_layer, name='subtitles', offset=0.0)
    scene.add_layer(audio_layer, name='audio')
    
    # Export video
    print(f"Generating Simple Caption style video...")
    print(f"Output: {output_file}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Features: White text with black outline, size-pulse highlighting")
    
    scene.write_video(
        output_file,
        fps=fps,
        audio_codec='aac'
    )
    
    print(f"Simple Caption video successfully generated at: {output_file}")

if __name__ == "__main__":
    create_simple_caption_video()