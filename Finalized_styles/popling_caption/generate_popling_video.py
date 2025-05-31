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
    """Create a video with Popling Caption style."""
    
    # Configuration
    resolution = (1080, 1920)  # Instagram 9:16 format
    fps = 30
    
    # File paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    parakeet_file = os.path.join(project_root, 'other_root_files', 'parakeet_output.json')
    audio_file = os.path.join(project_root, 'other_root_files', 'got_script.mp3')
    output_file = os.path.join(project_root, 'popling_caption_final.mp4')
    json_style_file = os.path.join(project_root, 'subtitle_styles', 'config', 'subtitle_styles_v3.json')
    
    # Load word timestamps
    word_timestamps = load_parakeet_data(parakeet_file)
    
    # Load audio to get duration
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    # Load Popling Caption style configuration
    style = StyleLoader.load_style_from_json(json_style_file, "popling_caption")
    
    # Create composition
    scene = mv.layer.Composition(
        size=resolution,
        duration=duration
    )
    
    # Add black background using Rectangle
    background = mv.layer.Rectangle(
        size=resolution,
        duration=duration,
        color=(0, 0, 0)  # RGB tuple for pure black
    )
    scene.add_layer(background, name='background')
    
    # Create subtitle layer with Popling Caption style
    subtitle_layer = StyledSubtitleLayer(
        words=word_timestamps,
        style=style,
        resolution=resolution,
        position="bottom",  # Bottom positioning as per config
        safe_zones=True     # Instagram safe zone compliance
    )
    
    # Add subtitle layer to composition
    scene.add_layer(
        subtitle_layer,
        name='subtitles',
        offset=0.0
    )
    
    # Add audio track
    scene.add_layer(audio_layer, name='audio')
    
    # Export video
    print(f"Generating Popling Caption style video...")
    print(f"Output: {output_file}")
    print(f"Duration: {duration:.1f} seconds")
    print(f"Resolution: {resolution[0]}x{resolution[1]} (9:16)")
    print(f"Using Parakeet timestamps from: {parakeet_file}")
    
    scene.write_video(
        output_file,
        fps=fps,
        audio_codec='aac'
    )
    
    print(f"Video successfully generated at: {output_file}")

if __name__ == "__main__":
    create_popling_video()