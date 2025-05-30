#!/usr/bin/env python3
"""Test karaoke style with Alverata Bold Italic font"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
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

def test_karaoke_alverata():
    """Test karaoke style with Alverata Bold Italic font"""
    
    # File paths
    parakeet_json = "/Users/naman/Desktop/movie_py/other_root_files/parakeet_output.json"
    audio_file = "/Users/naman/Desktop/movie_py/other_root_files/got_script.mp3"
    output_path = "/Users/naman/Desktop/movie_py/output_test/karaoke_alverata_final.mp4"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load timing data
    transcript, word_timings = load_parakeet_data(parakeet_json)
    print(f"Loaded transcript: {transcript}")
    print(f"Number of words: {len(word_timings)}")
    
    # Calculate video duration based on last word + buffer
    if word_timings:
        video_duration = word_timings[-1]['end'] + 2.0  # 2 second buffer
    else:
        video_duration = 10.0
    
    print(f"Video duration: {video_duration:.1f} seconds")
    
    # Load karaoke style
    style_loader = StyleLoader()
    karaoke_style = style_loader.load_style_from_json(
        style_name='karaoke_style', 
        json_path='/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json'
    )
    
    # Create black background video
    black_bg = mv.layer.Rectangle(
        size=(1080, 1920),
        color=(0, 0, 0),  # Black background
        duration=video_duration
    )
    
    # Create audio layer
    audio_layer = mv.layer.Audio(audio_file)
    
    # Create composition
    scene = mv.layer.Composition(size=(1080, 1920), duration=video_duration)
    
    # Add layers
    scene.add_layer(black_bg, name='background')
    scene.add_layer(audio_layer, name='audio')
    
    # Create subtitle layer with real timing
    subtitle_layer = StyledSubtitleLayer(
        words=word_timings,
        style=karaoke_style,
        resolution=(1080, 1920)
    )
    
    # Add subtitle layer
    scene.add_layer(subtitle_layer, name='subtitles')
    
    # Export settings
    print(f"\\nRendering final karaoke style video with:")
    print(f"- Font: Alverata Bold Italic (108px)")
    print(f"- Normal text: White")
    print(f"- Highlighted text: Bright Yellow")
    print(f"- Real audio timing from parakeet")
    print(f"- Black background")
    print(f"- Output: {output_path}")
    
    # Render video
    scene.write_video(output_path, codec='libx264')
    print(f"\\n✅ Final karaoke video created: {output_path}")

if __name__ == "__main__":
    test_karaoke_alverata()