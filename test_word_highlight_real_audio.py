#!/usr/bin/env python3
"""Real-world test of word highlighting with Game of Thrones audio and Parakeet timing"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
from subtitle_styles.core.json_style_loader import JSONConfiguredStyle
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

def create_word_highlight_style():
    """Create word highlight style configuration"""
    return {
        "name": "WORD HIGHLIGHT STYLE",
        "description": "Real-world word-by-word background highlighting with Game of Thrones audio",
        "version": "3.0",
        "effect_type": "word_highlight",
        "format": {
            "resolution": [1080, 1920],
            "aspect_ratio": "9:16",
            "target_platform": ["Instagram", "YouTube Shorts", "TikTok"]
        },
        "layout": {
            "text_positioning": "bottom",
            "safe_zones": True,
            "safe_margins": {
                "horizontal": 100,
                "top": 220,
                "bottom": 450
            },
            "words_per_window": 3,
            "max_width": 900
        },
        "typography": {
            "font_family": "/Users/naman/Library/Fonts/Montserrat-Black.ttf",
            "font_size": 85,
            "font_size_highlighted": 85,
            "text_alignment": "center",
            "text_transform": "uppercase",
            "font_weight": "900",
            "colors": {
                "text": [255, 255, 255],  # White text
                "background_highlighted": [138, 43, 226]  # Purple background for highlighted word only
            }
        },
        "effect_parameters": {
            "background_padding": {
                "x": 25,
                "y": 15
            },
            "rounded_corners": 20,
            "auto_scaling": True
        },
        "animation": {
            "type": "word_highlight",
            "highlight_method": "background_highlight",
            "transition_duration": 0.2,
            "word_level_styling": True
        }
    }

def test_real_world_word_highlight():
    """Test word highlighting with real Game of Thrones audio and timing"""
    
    # File paths
    parakeet_json = "/Users/naman/Desktop/movie_py/other_root_files/parakeet_output.json"
    audio_file = "/Users/naman/Desktop/movie_py/other_root_files/got_script.mp3"
    output_path = "/Users/naman/Desktop/movie_py/output_test/word_highlight_got_real.mp4"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load real timing data
    transcript, word_timings = load_parakeet_data(parakeet_json)
    print(f"Loaded transcript: {transcript}")
    print(f"Number of words: {len(word_timings)}")
    
    # Calculate video duration based on last word + buffer
    if word_timings:
        video_duration = word_timings[-1]['end'] + 2.0  # 2 second buffer
    else:
        video_duration = 10.0
    
    print(f"Video duration: {video_duration:.1f} seconds")
    
    # Create word highlight style
    style_config = create_word_highlight_style()
    word_highlight_style = JSONConfiguredStyle(style_config)
    
    # Create black background video
    black_bg = mv.layer.Rectangle(
        size=(1080, 1920),
        color=(0, 0, 0),  # Pure black background
        duration=video_duration
    )
    
    # Create audio layer
    audio_layer = mv.layer.Audio(audio_file)
    
    # Create composition
    scene = mv.layer.Composition(size=(1080, 1920), duration=video_duration)
    
    # Add layers
    scene.add_layer(black_bg, name='background')
    scene.add_layer(audio_layer, name='audio')
    
    # Create subtitle layer with word highlighting
    subtitle_layer = StyledSubtitleLayer(
        words=word_timings,
        style=word_highlight_style,
        resolution=(1080, 1920)
    )
    
    # Add subtitle layer
    scene.add_layer(subtitle_layer, name='subtitles')
    
    # Export settings
    print(f"\\nRendering real-world word highlight video:")
    print(f"- Font: Montserrat Black (85px)")
    print(f"- Normal words: White text, no background")
    print(f"- Highlighted word: White text, purple background")
    print(f"- Real Game of Thrones audio with NVIDIA Parakeet timing")
    print(f"- Auto-scaling: Enabled for long words")
    print(f"- Black background for maximum contrast")
    print(f"- Output: {output_path}")
    
    # Render video
    scene.write_video(output_path, codec='libx264')
    print(f"\\n✅ Real-world word highlight test completed: {output_path}")
    
    # Print some sample timings for verification
    print(f"\\nSample word timings:")
    for i, word in enumerate(word_timings[:10]):
        print(f"  {i+1:2d}. '{word['word']:10}' {word['start']:5.2f}s - {word['end']:5.2f}s")
    if len(word_timings) > 10:
        print(f"  ... and {len(word_timings) - 10} more words")

if __name__ == "__main__":
    test_real_world_word_highlight()