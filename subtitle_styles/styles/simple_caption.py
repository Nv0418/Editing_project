"""
Simple Caption Style
Clean, bold text with black outline - perfect for maximum readability
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from subtitle_styles.core.base_style import BaseSubtitleStyle
from subtitle_styles.effects.text_effects import TextEffects
import movis as mv
from movis.layer.drawing import Text
from movis.enum import TextAlignment
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class SimpleCaptionStyle(BaseSubtitleStyle):
    """Simple caption with bold text and black outline"""
    
    def get_default_config(self):
        return {
            'name': 'SIMPLE CAPTION',
            'description': 'Clean, bold text with black outline for maximum readability',
            'preview_text': 'SIMPLE CAPTION',
            'typography': {
                'font_family': 'Arial Black',  # Bold sans-serif
                'font_size': 72,
                'font_size_highlighted': 80,
                'color': [255, 255, 255],  # White
                'outline_color': [0, 0, 0],  # Black outline
                'outline_width': 4,
                'alignment': 'center',
                'text_transform': 'uppercase'  # All caps
            },
            'layout': {
                'position': 'bottom',
                'safe_zones': True,
                'max_width': 900  # Maximum text width before wrapping
            },
            'animation': {
                'type': 'word_highlight',
                'highlight_method': 'size_pulse',
                'transition_duration': 0.2
            }
        }
    
    def create_text_with_outline(self, text, font_size, is_highlighted=False):
        """Create text with black outline for better readability"""
        config = self.config['typography']
        
        # Use larger size for highlighted text
        if is_highlighted:
            font_size = config.get('font_size_highlighted', font_size * 1.1)
        
        # Transform text to uppercase
        if config.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Create the text layer with outline effect
        outline_img = TextEffects.create_outline_effect(
            text=text,
            font_path=config['font_family'],
            font_size=int(font_size),
            text_color=tuple(config['color']),
            outline_color=tuple(config['outline_color']),
            outline_width=config['outline_width'],
            image_size=(1080, 200)  # Smaller height for single line
        )
        
        return outline_img
    
    def apply_effects(self, text_layer, time, word_timing):
        """Apply simple caption effects"""
        # For simple caption, we just return the text with outline
        # The outline is already applied in create_text_with_outline
        return text_layer
    
    def create_word_layer(self, word, word_timing, window_timing):
        """Create a word layer with simple caption style"""
        
        class SimpleWordLayer:
            def __init__(self, word, word_start, word_end, window_start, window_end, style):
                self.word = word
                self.word_start = word_start
                self.word_end = word_end
                self.window_start = window_start
                self.window_end = window_end
                self.style = style
                self.duration = window_end - window_start
                
            def __call__(self, time):
                # Only visible during window
                if time < self.window_start or time > self.window_end:
                    return None
                
                # Check if word is highlighted
                is_highlighted = self.word_start <= time <= self.word_end
                
                # Create text with outline
                img_array = self.style.create_text_with_outline(
                    self.word, 
                    self.style.config['typography']['font_size'],
                    is_highlighted
                )
                
                return img_array
            
            def get_key(self, time):
                if time < self.window_start or time > self.window_end:
                    return None
                is_highlighted = self.word_start <= time <= self.word_end
                return (self.word, is_highlighted, round(time, 2))
        
        return SimpleWordLayer(
            word['word'],
            word['start'],
            word['end'],
            window_timing['start'],
            window_timing['end'],
            self
        )