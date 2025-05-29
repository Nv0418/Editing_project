"""
JSON Style Loader
Loads subtitle styles from JSON configuration and creates appropriate style instances
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from subtitle_styles.core.base_style import BaseSubtitleStyle
from subtitle_styles.effects.text_effects import TextEffects
import numpy as np
from PIL import Image


class JSONConfiguredStyle(BaseSubtitleStyle):
    """A style that is configured via JSON"""
    
    def __init__(self, config: Dict[str, Any]):
        self.json_config = config
        super().__init__()
        
    def get_default_config(self) -> Dict[str, Any]:
        """Return the JSON configuration"""
        return self.json_config
    
    def apply_effects(self, text_layer: Any, time: float, word_timing: Dict) -> Any:
        """Apply effects based on effect_type"""
        # This is handled by the specific rendering methods
        return text_layer
    
    def create_styled_text(self, text: str, font_size: int, time: float = 0, is_highlighted: bool = False, word_index: int = -1) -> np.ndarray:
        """Create styled text based on effect_type"""
        effect_type = self.config.get('effect_type', 'simple')
        
        if effect_type == 'outline':
            return self._create_outline_text(text, font_size, is_highlighted)
        elif effect_type == 'background':
            return self._create_background_text(text, font_size, is_highlighted)
        elif effect_type == 'glow':
            return self._create_glow_text(text, font_size, time, is_highlighted)
        elif effect_type == 'dual_glow':
            return self._create_dual_glow_text(text, font_size, time, is_highlighted, word_index)
        elif effect_type == 'text_shadow':
            return self._create_text_shadow_text(text, font_size, time, is_highlighted, word_index)
        else:
            # Fallback to simple text
            return self._create_simple_text(text, font_size, is_highlighted)
    
    def _create_outline_text(self, text: str, font_size: int, is_highlighted: bool = False) -> np.ndarray:
        """Create text with outline effect"""
        typo = self.config['typography']
        effects = self.config.get('effect_parameters', {})
        
        # Transform text if needed
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Use larger size for highlighted
        if is_highlighted:
            font_size = typo.get('font_size_highlighted', font_size)
        
        # Get text color (handle both formats)
        if 'text' in typo['colors']:
            text_color = tuple(typo['colors']['text'])
        elif 'normal' in typo['colors']:
            text_color = tuple(typo['colors']['normal'])
        else:
            text_color = (255, 255, 255)
        
        # Get outline color
        if 'outline' in typo['colors']:
            outline_color = tuple(typo['colors']['outline'])
        else:
            outline_color = (0, 0, 0)  # Default black outline
        
        return TextEffects.create_outline_effect(
            text=text,
            font_path=typo['font_family'],
            font_size=int(font_size),
            text_color=text_color,
            outline_color=outline_color,
            outline_width=effects.get('outline_width', 3),
            image_size=(1080, 200)
        )
    
    def _create_background_text(self, text: str, font_size: int, is_highlighted: bool = False) -> np.ndarray:
        """Create text with background box"""
        typo = self.config['typography']
        effects = self.config.get('effect_parameters', {})
        
        # Transform text
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Handle highlight
        if is_highlighted:
            font_size = typo.get('font_size_highlighted', font_size)
            bg_color = typo['colors'].get('background_highlighted', typo['colors']['background'])
            # Apply brightness boost if specified
            brightness_boost = effects.get('highlight_brightness_boost', 0)
            bg_color = [min(255, c + brightness_boost) for c in bg_color]
        else:
            bg_color = typo['colors']['background']
        
        # Create image
        img_width, img_height = 1080, 300
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(typo['font_family'], int(font_size))
        except:
            font = ImageFont.load_default()
        
        # Split text into lines if needed
        lines = text.split('\n') if '\n' in text else [text]
        
        # Calculate text dimensions
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
        line_spacing = int(font_size * (typo.get('line_height', 1.1) - 1))
        total_height += line_spacing * (len(lines) - 1)
        
        # Get padding
        padding = effects.get('background_padding', {'x': 20, 'y': 10})
        pad_x = padding.get('x', padding) if isinstance(padding, dict) else padding
        pad_y = padding.get('y', padding) if isinstance(padding, dict) else padding
        
        # Calculate background dimensions
        bg_width = max_width + (pad_x * 2)
        bg_height = total_height + (pad_y * 2)
        
        # Center background
        bg_x = (img_width - bg_width) // 2
        bg_y = (img_height - bg_height) // 2
        
        # Draw background
        opacity = int(255 * effects.get('background_opacity', 1.0))
        corners = effects.get('rounded_corners', 0)
        
        if corners > 0:
            draw.rounded_rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                radius=corners,
                fill=(*bg_color, opacity)
            )
        else:
            draw.rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                fill=(*bg_color, opacity)
            )
        
        # Draw text
        current_y = bg_y + pad_y
        # Handle both new format (text) and old format (normal)
        if 'text' in typo['colors']:
            text_color = tuple(typo['colors']['text'])
        elif 'normal' in typo['colors']:
            text_color = tuple(typo['colors']['normal'])
        else:
            text_color = (255, 255, 255)
        
        for line, (line_width, line_height) in zip(lines, line_bboxes):
            text_x = (img_width - line_width) // 2
            draw.text((text_x, current_y), line, font=font, fill=(*text_color, 255))
            current_y += line_height + line_spacing
        
        return np.array(img)
    
    def _create_glow_text(self, text: str, font_size: int, time: float, is_highlighted: bool = False) -> np.ndarray:
        """Create text with glow effect"""
        typo = self.config['typography']
        effects = self.config.get('effect_parameters', {})
        
        # Transform text
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Handle highlight
        if is_highlighted:
            font_size = typo.get('font_size_highlighted', font_size)
            base_intensity = effects.get('glow_intensity_highlighted', 1.2)
            glow_color = typo['colors'].get('glow_highlighted', typo['colors']['glow'])
            # Apply color multiplier
            multiplier = effects.get('highlight_color_multiplier', 1.0)
            glow_color = [min(255, int(c * multiplier)) for c in glow_color]
        else:
            base_intensity = effects.get('glow_intensity', 0.8)
            glow_color = typo['colors']['glow']
        
        # Get text color (handle both formats)
        if 'text' in typo['colors']:
            text_color = tuple(typo['colors']['text'])
        elif 'normal' in typo['colors']:
            text_color = tuple(typo['colors']['normal'])
        else:
            text_color = (255, 255, 255)
        
        # Check if pulsing is enabled
        pulse_config = effects.get('pulse', {})
        if pulse_config.get('enabled', False) and not is_highlighted:
            return TextEffects.create_animated_glow_pulse(
                text=text,
                font_path=typo['font_family'],
                font_size=int(font_size),
                text_color=text_color,
                glow_color=tuple(glow_color),
                time=time,
                pulse_frequency=pulse_config.get('frequency', 0.5),
                min_intensity=pulse_config.get('min_intensity', 0.3) * base_intensity,
                max_intensity=pulse_config.get('max_intensity', 1.0) * base_intensity,
                image_size=(1080, 200)
            )
        else:
            return TextEffects.create_glow_effect(
                text=text,
                font_path=typo['font_family'],
                font_size=int(font_size),
                text_color=text_color,
                glow_color=tuple(glow_color),
                glow_radius=effects.get('glow_radius', 15),
                glow_intensity=base_intensity,
                image_size=(1080, 200)
            )
    
    def _create_dual_glow_text(self, text: str, font_size: int, time: float, is_highlighted: bool = False, word_index: int = -1) -> np.ndarray:
        """Create text with dual-tone glow effect (white words + red highlighted words)"""
        typo = self.config['typography']
        effects = self.config.get('effect_parameters', {})
        
        # Transform text
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Split text into words
        words = text.split()
        
        # Get colors
        normal_text_color = tuple(typo['colors']['text_normal'])
        highlighted_text_color = tuple(typo['colors']['text_highlighted'])
        normal_glow_color = tuple(typo['colors']['glow_normal'])
        highlighted_glow_color = tuple(typo['colors']['glow_highlighted'])
        
        # Get glow parameters
        normal_glow_radius = effects.get('glow_radius_normal', 12)
        highlighted_glow_radius = effects.get('glow_radius_highlighted', 15)
        normal_glow_intensity = effects.get('glow_intensity_normal', 0.4)
        highlighted_glow_intensity = effects.get('glow_intensity_highlighted', 0.6)
        
        # Determine which word is highlighted based on timing or word_index
        highlighted_word_index = word_index if word_index >= 0 else -1
        
        # Use the new two-tone glow effect
        return TextEffects.create_two_tone_glow_effect(
            words=words,
            font_path=typo['font_family'],
            font_size=int(font_size),
            normal_text_color=normal_text_color,
            highlighted_text_color=highlighted_text_color,
            normal_glow_color=normal_glow_color,
            highlighted_glow_color=highlighted_glow_color,
            normal_glow_radius=normal_glow_radius,
            highlighted_glow_radius=highlighted_glow_radius,
            normal_glow_intensity=normal_glow_intensity,
            highlighted_glow_intensity=highlighted_glow_intensity,
            highlighted_word_index=highlighted_word_index,
            image_size=(1080, 200)
        )
    
    def _create_text_shadow_text(self, text: str, font_size: int, time: float, is_highlighted: bool = False, word_index: int = -1) -> np.ndarray:
        """Create text with text-shadow glow effects using currentColor logic"""
        typo = self.config['typography']
        shadow_config = self.config.get('text_shadow', {})
        
        # Transform text
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        # Split text into words
        words = text.split()
        
        # Get base colors
        normal_text_color = tuple(typo['colors']['text_normal'])
        highlighted_text_color = tuple(typo['colors']['text_highlighted'])
        
        # Use the enhanced text shadow effect
        return TextEffects.create_text_shadow_glow_effect(
            words=words,
            font_path=typo['font_family'],
            font_size=int(font_size),
            normal_text_color=normal_text_color,
            highlighted_text_color=highlighted_text_color,
            shadow_blur_1=shadow_config.get('shadowBlur', 18),
            shadow_opacity_1=0.8,  # from rgba(currentColor, 0.8)
            shadow_blur_2=shadow_config.get('extraShadows', [{}])[0].get('blur', 27),
            shadow_opacity_2=0.6,  # from rgba(currentColor, 0.6)
            highlighted_word_index=word_index if word_index >= 0 else -1,
            image_size=(1080, 200)
        )
    
    def _create_simple_text(self, text: str, font_size: int, is_highlighted: bool = False) -> np.ndarray:
        """Create simple text (fallback)"""
        typo = self.config['typography']
        
        if typo.get('text_transform') == 'uppercase':
            text = text.upper()
        
        if is_highlighted:
            font_size = typo.get('font_size_highlighted', font_size)
        
        # Create simple text image
        img = Image.new('RGBA', (1080, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype(typo['font_family'], int(font_size))
        except:
            font = ImageFont.load_default()
        
        # Get text color
        if 'colors' in typo:
            if 'text' in typo['colors']:
                color = tuple(typo['colors']['text'])
            elif 'normal' in typo['colors']:
                color = tuple(typo['colors']['normal'])
            else:
                color = (255, 255, 255)
        else:
            color = (255, 255, 255)
        
        # Center text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (1080 - text_width) // 2
        y = (200 - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=(*color, 255))
        
        return np.array(img)


class StyleLoader:
    """Loads styles from JSON configuration files"""
    
    @staticmethod
    def load_style_from_json(json_path: Path, style_name: str) -> Optional[JSONConfiguredStyle]:
        """Load a specific style from JSON file"""
        try:
            with open(json_path, 'r') as f:
                styles = json.load(f)
            
            if style_name not in styles:
                print(f"Style '{style_name}' not found in {json_path}")
                print(f"Available styles: {list(styles.keys())}")
                return None
            
            style_config = styles[style_name]
            return JSONConfiguredStyle(style_config)
            
        except FileNotFoundError:
            print(f"Style file not found: {json_path}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
    
    @staticmethod
    def list_available_styles(json_path: Path) -> Dict[str, str]:
        """List all available styles in JSON file"""
        try:
            with open(json_path, 'r') as f:
                styles = json.load(f)
            
            return {
                name: config.get('name', name) 
                for name, config in styles.items()
            }
        except:
            return {}


# Make necessary imports available
from PIL import ImageDraw, ImageFont