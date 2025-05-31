#!/usr/bin/env python3
import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def load_parakeet_data(file_path):
    """Load word timestamps from Parakeet JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['word_timestamps']

def create_popling_video():
    """Create a video with popling caption style."""
    
    # Configuration
    resolution = (1080, 1920)  # Instagram 9:16 format
    fps = 30
    
    # File paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    parakeet_file = os.path.join(project_root, 'other_root_files', 'parakeet_output.json')
    audio_file = os.path.join(project_root, 'other_root_files', 'got_script.mp3')
    json_style_file = os.path.join(project_root, 'subtitle_styles', 'config', 'subtitle_styles_v3.json')
    
    # Output file
    output_file = os.path.join(project_root, 'popling_caption_test.mp4')
    
    # Load data
    word_timestamps = load_parakeet_data(parakeet_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    # Load style
    style = StyleLoader.load_style_from_json(json_style_file, 'popling_caption')
    
    # Create composition
    scene = mv.layer.Composition(size=resolution, duration=duration)
    
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
    print(f"Generating popling caption style video...")
    print(f"Output: {output_file}")
    
    scene.write_video(
        output_file,
        fps=fps,
        audio_codec='aac'
    )
    
    print(f"Video successfully generated at: {output_file}")

if __name__ == "__main__":
    create_popling_video()