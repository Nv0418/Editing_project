#!/usr/bin/env python3
"""Test script for updated karaoke style with green highlight and Bebas Neue font"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def test_karaoke_style():
    """Test the updated karaoke style with green text highlighting"""
    
    # Test parameters
    video_path = "/Users/naman/Desktop/movie_py/media/VIDEOS_TEST/comfyuiblog_00004.mp4"
    output_path = "/Users/naman/Desktop/movie_py/output_test/karaoke_green_test.mp4"
    test_text = "Epic battles dragons fire kingdom throne winter coming"
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load the karaoke style
    style_loader = StyleLoader()
    karaoke_style = style_loader.load_style_from_json(
        style_name='karaoke_style', 
        json_path='/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json'
    )
    
    # Create word timing data (simulated)
    words = test_text.split()
    word_timings = []
    current_time = 1.0  # Start at 1 second
    
    for i, word in enumerate(words):
        duration = 0.8  # Each word lasts 0.8 seconds
        word_timings.append({
            'word': word,
            'start': current_time,
            'end': current_time + duration
        })
        current_time += duration + 0.2  # 0.2 second gap between words
    
    # Create the video composition
    video_layer = mv.layer.Video(video_path)
    duration = video_layer.duration
    
    # Create composition
    scene = mv.layer.Composition(size=(1080, 1920), duration=duration)
    
    # Add video layer
    scene.add_layer(video_layer)
    
    # Create subtitle layer
    subtitle_layer = StyledSubtitleLayer(
        words=word_timings,
        style=karaoke_style,
        resolution=(1080, 1920)
    )
    
    # Add subtitle layer with proper timing
    scene.add_layer(subtitle_layer, name='subtitles')
    
    # Export the video
    print(f"Rendering karaoke style test video with:")
    print(f"- Font: Bebas Neue")
    print(f"- Normal text color: White")
    print(f"- Highlighted text color: Green (#00FF00)")
    print(f"- Output: {output_path}")
    
    scene.write_video(output_path, codec='libx264')
    print(f"Test video created successfully at: {output_path}")

if __name__ == "__main__":
    test_karaoke_style()