#!/usr/bin/env python3
"""Test the new word-by-word background highlighting feature"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
import numpy as np
import movis as mv
from subtitle_styles.effects.word_highlight_effects import WordHighlightEffects
from PIL import Image

def test_word_highlight_feature():
    """Test the new word background highlighting feature"""
    
    # Test parameters
    test_words = ["highlight", "caption", "feature", "working"]
    font_path = "/Users/naman/Library/Fonts/Montserrat-Black.ttf"
    font_size = 80
    
    # Colors - only highlighted word gets background
    text_color = (255, 255, 255)  # White text
    normal_bg_color = None  # No background for normal words
    highlight_bg_color = (138, 43, 226)  # Purple background for highlighted word only
    
    print("Testing word-by-word background highlighting feature...")
    print(f"Words: {test_words}")
    print(f"Font: Montserrat Black")
    print(f"Normal words: White text, no background")
    print(f"Highlighted word: White text, purple background")
    
    # Test highlighting each word one by one
    for highlight_idx in range(len(test_words)):
        print(f"\\nGenerating frame {highlight_idx + 1}: highlighting '{test_words[highlight_idx]}'")
        
        # Create the highlighted text image
        text_img = WordHighlightEffects.create_word_background_highlight_effect(
            words=test_words,
            font_path=font_path,
            font_size=font_size,
            text_color=text_color,
            normal_bg_color=normal_bg_color,
            highlight_bg_color=highlight_bg_color,
            highlighted_word_index=highlight_idx,
            background_padding=(25, 15),  # Nice padding around words
            corner_radius=20,  # Rounded corners like in screenshot
            image_size=(1080, 200)
        )
        
        # Save as test image
        output_path = f"/Users/naman/Desktop/movie_py/output_test/word_highlight_test_{highlight_idx + 1}.png"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert to PIL and save
        img_pil = Image.fromarray(text_img)
        img_pil.save(output_path)
        print(f"Saved: {output_path}")
    
    print(f"\\n✅ Word highlight feature test completed!")
    print(f"Check the generated images to see the highlighting effect.")
    print(f"Each image shows a different word highlighted with purple background.")

def test_gradient_highlight():
    """Test the gradient version of word highlighting"""
    
    test_words = ["gradient", "highlight", "effect"]
    font_path = "/Users/naman/Library/Fonts/alverata-bold-italic.ttf"
    font_size = 80
    text_color = (255, 255, 255)
    
    print("\\n\\nTesting gradient word highlighting...")
    
    # Test highlighting with gradient
    text_img = WordHighlightEffects.create_gradient_word_highlight_effect(
        words=test_words,
        font_path=font_path,
        font_size=font_size,
        text_color=text_color,
        gradient_start=(138, 43, 226),  # Purple
        gradient_end=(255, 20, 147),    # Pink
        highlighted_word_index=1,  # Highlight "highlight"
        background_padding=(30, 18),
        corner_radius=25,
        image_size=(1080, 200)
    )
    
    # Save gradient test
    output_path = "/Users/naman/Desktop/movie_py/output_test/word_gradient_test.png"
    img_pil = Image.fromarray(text_img)
    img_pil.save(output_path)
    print(f"Saved gradient test: {output_path}")

if __name__ == "__main__":
    test_word_highlight_feature()
    test_gradient_highlight()