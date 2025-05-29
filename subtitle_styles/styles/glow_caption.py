"""
Glow/Neon Caption Style

Text with vibrant glow effect - perfect for energetic content
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


class GlowCaptionStyle(BaseSubtitleStyle):
    """Caption with neon glow effect"""
    
    def get_default_config(self):
        return {
            'name': 'GLOW / NEON',
            'description': 'Bold text with vibrant neon glow effect',
            'preview_text': 'GLOW',
            'typography': {
                'font_family': 'Arial Black',
                'font_size': 68,
                'font_size_highlighted': 76,
                'color': [255, 255, 255],  # White text
                'alignment': 'center',
                'text_transform': 'uppercase',
                'font_weight': 'bold'
            },
            'glow': {
                'enabled': True,
                'color': [255, 0, 128],  # Hot pink/red glow like in Aicut
                'radius': 20,
                'intensity': 0.9,
                'pulse': {
                    'enabled': True,
                    'frequency': 0.5,  # Pulses per second
                    'min_intensity': 0.6,
                    'max_intensity': 1.0
                }
            },
            'layout': {
                'position': 'bottom',
                'safe_zones': True,
                'max_width': 900
            },
            'animation': {
                'type': 'word_highlight',
                'highlight_method': 'glow_intensify',
                'transition_duration': 0.3
            }
        }
    
    def create_glowing_text(self, text, font_size, time, is_highlighted=False):
        """Create text with animated glow effect"""
        config = self.config
        typo_config = config['typography']
        glow_config = config['glow']
        
        # Transform text
        if typo_config.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Adjust for highlight
        if is_highlighted:
            font_size = typo_config.get('font_size_highlighted', font_size)
            # Intensify glow when highlighted
            base_intensity = min(1.0, glow_config['intensity'] * 1.3)
            glow_color = glow_config['color']
            # Make glow brighter when highlighted
            glow_color = [min(255, int(c * 1.2)) for c in glow_color]
        else:
            base_intensity = glow_config['intensity']
            glow_color = glow_config['color']
        
        # Calculate pulsing intensity if enabled
        if glow_config['pulse']['enabled'] and not is_highlighted:
            pulse_config = glow_config['pulse']
            intensity = TextEffects.create_animated_glow_pulse(
                text=text,
                font_path=typo_config['font_family'],
                font_size=int(font_size),
                text_color=tuple(typo_config['color']),
                glow_color=tuple(glow_color),
                time=time,
                pulse_frequency=pulse_config['frequency'],
                min_intensity=pulse_config['min_intensity'] * base_intensity,
                max_intensity=pulse_config['max_intensity'] * base_intensity,
                image_size=(1080, 200)
            )
            return intensity
        else:
            # Static or highlighted glow
            return TextEffects.create_glow_effect(
                text=text,
                font_path=typo_config['font_family'],
                font_size=int(font_size),
                text_color=tuple(typo_config['color']),
                glow_color=tuple(glow_color),
                glow_radius=glow_config['radius'],
                glow_intensity=base_intensity,
                image_size=(1080, 200)
            )
    
    def apply_effects(self, text_layer, time, word_timing):
        """Apply glow effects"""
        # Glow is already applied in create_glowing_text
        return text_layer
    
    def create_word_layer(self, word, word_timing, window_timing):
        """Create a word layer with glow caption style"""
        
        class GlowWordLayer:
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
                
                # Create glowing text
                img_array = self.style.create_glowing_text(
                    self.word,
                    self.style.config['typography']['font_size'],
                    time,
                    is_highlighted
                )
                
                return img_array
            
            def get_key(self, time):
                if time < self.window_start or time > self.window_end:
                    return None
                is_highlighted = self.word_start <= time <= self.word_end
                # Include time in key for animated glow
                return (self.word, is_highlighted, round(time, 1))
        
        return GlowWordLayer(
            word['word'],
            word['start'],
            word['end'],
            window_timing['start'],
            window_timing['end'],
            self
        )