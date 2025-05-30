#!/usr/bin/env python3
"""Test word highlighting feature with audio timing like karaoke"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
from subtitle_styles.core.json_style_loader import JSONConfiguredStyle
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def create_test_word_highlight_style():
    """Create a test style configuration for word highlighting"""
    return {
        "name": "WORD HIGHLIGHT TEST",
        "description": "Test word-by-word background highlighting",
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
            "font_size": 80,
            "font_size_highlighted": 80,
            "text_alignment": "center",
            "text_transform": "lowercase",
            "font_weight": "bold",
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
            "highlight_brightness_boost": 0
        },
        "animation": {
            "type": "word_highlight",
            "highlight_method": "background_highlight",
            "transition_duration": 0.2,
            "word_level_styling": True
        }
    }

def test_word_highlight_with_audio():
    """Test word highlighting with simulated audio timing"""
    
    # Test text with timing
    test_text = "this is word by word highlighting"
    words = test_text.split()
    
    # Create fake timing data
    word_timings = []
    current_time = 1.0
    
    for word in words:
        duration = 0.8
        word_timings.append({
            "word": word,
            "start": current_time,
            "end": current_time + duration
        })
        current_time += duration + 0.3  # 0.3 second gap between words
    
    video_duration = current_time + 2.0
    output_path = "/Users/naman/Desktop/movie_py/output_test/word_highlight_audio_test.mp4"
    
    # Create output directory
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Create test style
    style_config = create_test_word_highlight_style()
    word_highlight_style = JSONConfiguredStyle(style_config)
    
    # Create black background
    black_bg = mv.layer.Rectangle(
        size=(1080, 1920),
        color=(0, 0, 0),
        duration=video_duration
    )
    
    # Create composition
    scene = mv.layer.Composition(size=(1080, 1920), duration=video_duration)
    scene.add_layer(black_bg, name='background')
    
    # Create subtitle layer with word highlighting
    subtitle_layer = StyledSubtitleLayer(
        words=word_timings,
        style=word_highlight_style,
        resolution=(1080, 1920)
    )
    
    scene.add_layer(subtitle_layer, name='subtitles')
    
    print(f"Testing word-by-word background highlighting:")
    print(f"- Text: '{test_text}'")
    print(f"- Words: {len(words)}")
    print(f"- Font: Montserrat Black")
    print(f"- Normal words: White text, no background")
    print(f"- Highlighted word: White text, purple background")
    print(f"- Effect: Only currently spoken word gets purple background")
    print(f"- Output: {output_path}")
    
    # Render video
    scene.write_video(output_path, codec='libx264')
    print(f"\\n✅ Word highlight audio test completed: {output_path}")

if __name__ == "__main__":
    test_word_highlight_with_audio()