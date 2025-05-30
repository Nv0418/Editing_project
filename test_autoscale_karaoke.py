#!/usr/bin/env python3
"""Test karaoke auto-scaling with very long text"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def test_autoscale():
    """Test auto-scaling with extremely long text"""
    
    # Test with very long text to force auto-scaling
    long_text = "This is an extremely long sentence that should definitely exceed the normal frame width and trigger the auto-scaling functionality"
    words = long_text.split()
    
    # Create fake timing data for the long text
    word_timings = []
    current_time = 1.0
    
    for word in words:
        duration = 0.5
        word_timings.append({
            "word": word,
            "start": current_time,
            "end": current_time + duration
        })
        current_time += duration + 0.1
    
    video_duration = current_time + 2.0
    output_path = "/Users/naman/Desktop/movie_py/output_test/karaoke_autoscale_test.mp4"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load karaoke style
    style_loader = StyleLoader()
    karaoke_style = style_loader.load_style_from_json(
        style_name='karaoke_style', 
        json_path='/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json'
    )
    
    # Create black background
    black_bg = mv.layer.Rectangle(
        size=(1080, 1920),
        color=(0, 0, 0),
        duration=video_duration
    )
    
    # Create composition
    scene = mv.layer.Composition(size=(1080, 1920), duration=video_duration)
    scene.add_layer(black_bg, name='background')
    
    # Create subtitle layer
    subtitle_layer = StyledSubtitleLayer(
        words=word_timings,
        style=karaoke_style,
        resolution=(1080, 1920)
    )
    
    scene.add_layer(subtitle_layer, name='subtitles')
    
    print(f"Testing auto-scaling with long text:")
    print(f"- Text: '{long_text}'")
    print(f"- Words: {len(words)}")
    print(f"- Font: Alverata Bold Italic (108px)")
    print(f"- Expected: Auto-scaling should activate")
    print(f"- Output: {output_path}")
    
    # Render video
    scene.write_video(output_path, codec='libx264')
    print(f"\\n✅ Auto-scale test completed: {output_path}")

if __name__ == "__main__":
    test_autoscale()