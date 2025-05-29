"""
Background Caption Style
Text with solid color background box - perfect for emphasis
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


class BackgroundCaptionStyle(BaseSubtitleStyle):
    """Caption with solid background box"""
    
    def get_default_config(self):
        return {
            'name': 'BACKGROUND CAPTION',
            'description': 'Bold text with vibrant background box for emphasis',
            'preview_text': 'BACKGROUND\nCAPTION',
            'typography': {
                'font_family': 'Arial Black',
                'font_size': 56,
                'font_size_highlighted': 60,
                'color': [255, 255, 255],  # White text
                'alignment': 'center',
                'text_transform': 'uppercase',
                'line_height': 1.1
            },
            'background': {
                'enabled': True,
                'color': [0, 255, 255],  # Cyan/turquoise
                'padding': {'x': 40, 'y': 20},
                'rounded_corners': 0,  # Sharp corners like in Aicut
                'opacity': 1.0  # Fully opaque
            },
            'layout': {
                'position': 'bottom',
                'safe_zones': True,
                'max_width': 800,
                'multi_line': True
            },
            'animation': {
                'type': 'word_highlight',
                'highlight_method': 'background_pulse',
                'transition_duration': 0.15
            }
        }
    
    def create_text_with_background(self, text, font_size, is_highlighted=False):
        """Create text with background box"""
        config = self.config
        typo_config = config['typography']
        bg_config = config['background']
        
        # Transform text
        if typo_config.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Use larger size for highlighted
        if is_highlighted:
            font_size = typo_config.get('font_size_highlighted', font_size)
            # Make background slightly brighter when highlighted
            bg_color = [min(255, c + 30) for c in bg_config['color']]
        else:
            bg_color = bg_config['color']
        
        # Create image
        img_width, img_height = 1080, 300
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(typo_config['font_family'], int(font_size))
        except:
            font = ImageFont.load_default()
        
        # Split text into lines if needed
        lines = text.split('\n') if '\n' in text else [text]
        
        # Calculate text dimensions for all lines
        line_bboxes = []
        total_height = 0
        max_width = 0
        
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            line_bboxes.append((line_width, line_height))
            max_width = max(max_width, line_width)
            total_height += line_height
        
        # Add line spacing
        line_spacing = int(font_size * (typo_config.get('line_height', 1.1) - 1))
        total_height += line_spacing * (len(lines) - 1)
        
        # Calculate background dimensions
        pad_x = bg_config['padding']['x']
        pad_y = bg_config['padding']['y']
        bg_width = max_width + (pad_x * 2)
        bg_height = total_height + (pad_y * 2)
        
        # Center background
        bg_x = (img_width - bg_width) // 2
        bg_y = (img_height - bg_height) // 2
        
        # Draw background box
        if bg_config['rounded_corners'] > 0:
            # Rounded rectangle
            draw.rounded_rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                radius=bg_config['rounded_corners'],
                fill=(*bg_color, int(255 * bg_config['opacity']))
            )
        else:
            # Sharp rectangle
            draw.rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                fill=(*bg_color, int(255 * bg_config['opacity']))
            )
        
        # Draw text lines
        current_y = bg_y + pad_y
        text_color = tuple(typo_config['color'])
        
        for i, (line, (line_width, line_height)) in enumerate(zip(lines, line_bboxes)):
            # Center each line
            text_x = (img_width - line_width) // 2
            draw.text((text_x, current_y), line, font=font, fill=(*text_color, 255))
            current_y += line_height + line_spacing
        
        return np.array(img)
    
    def apply_effects(self, text_layer, time, word_timing):
        """Apply background caption effects"""
        return text_layer
    
    def create_word_layer(self, word, word_timing, window_timing):
        """Create a word layer with background caption style"""
        
        class BackgroundWordLayer:
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
                
                # Create text with background
                img_array = self.style.create_text_with_background(
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
        
        return BackgroundWordLayer(
            word['word'],
            word['start'],
            word['end'],
            window_timing['start'],
            window_timing['end'],
            self
        )