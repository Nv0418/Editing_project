"""
Base Style Class for Subtitle System
Provides the foundation for all subtitle styles
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
import movis as mv
from movis.layer.drawing import Text
from movis.enum import TextAlignment
import numpy as np


class BaseSubtitleStyle(ABC):
    """Abstract base class for all subtitle styles"""
    
    def __init__(self):
        self.config = self.get_default_config()
        
    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for this style"""
        pass
    
    @abstractmethod
    def apply_effects(self, text_layer: Any, time: float, word_timing: Dict) -> Any:
        """Apply style-specific effects to text layer"""
        pass
    
    def create_text_layer(self, 
                         text: str, 
                         duration: float,
                         position: Optional[Tuple[int, int]] = None) -> Text:
        """Create a basic text layer with style configuration"""
        config = self.config
        
        # Extract typography settings
        font_config = config.get('typography', {})
        font_family = font_config.get('font_family', 'Arial')
        font_size = font_config.get('font_size', 60)
        text_color = tuple(font_config.get('color', [255, 255, 255]))
        alignment = font_config.get('alignment', 'center')
        
        # Convert alignment string to enum
        alignment_map = {
            'left': TextAlignment.LEFT,
            'center': TextAlignment.CENTER,
            'right': TextAlignment.RIGHT
        }
        text_alignment = alignment_map.get(alignment, TextAlignment.CENTER)
        
        # Create text layer
        text_layer = Text(
            text=text,
            font_size=font_size,
            font_family=font_family,
            color=text_color,
            text_alignment=text_alignment,
            duration=duration
        )
        
        return text_layer
    
    def calculate_safe_position(self, 
                               resolution: Tuple[int, int],
                               position_type: str = 'bottom',
                               safe_zones: bool = True) -> Tuple[int, int]:
        """Calculate position respecting Instagram safe zones"""
        width, height = resolution
        
        # Instagram safe zones (increased side margins for better visibility)
        safe_top = 220 if safe_zones else 50
        safe_bottom = 450 if safe_zones else 50
        safe_sides = 100 if safe_zones else 50  # Increased from 35 to 100
        
        x = width // 2  # Center horizontally by default
        
        if position_type == 'top':
            y = safe_top + 50
        elif position_type == 'center':
            y = height // 2
        elif position_type == 'bottom':
            y = height - safe_bottom - 50
        else:
            y = height - safe_bottom - 50  # Default to bottom
            
        return (x, y)
    
    def interpolate_color(self, 
                         color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         factor: float) -> Tuple[int, int, int]:
        """Interpolate between two colors"""
        factor = max(0, min(1, factor))  # Clamp to [0, 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        
        return (r, g, b)
    
    def ease_in_out_cubic(self, t: float) -> float:
        """Cubic easing function for smooth animations"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 1 + p * p * p / 2
    
    def ease_out_elastic(self, t: float) -> float:
        """Elastic easing for bouncy effects"""
        if t == 0 or t == 1:
            return t
        
        p = 0.3
        s = p / 4
        return np.power(2, -10 * t) * np.sin((t - s) * (2 * np.pi) / p) + 1
    
    def get_style_info(self) -> Dict[str, str]:
        """Return style information for UI display"""
        return {
            'id': self.__class__.__name__.lower(),
            'name': self.config.get('name', 'Unknown Style'),
            'description': self.config.get('description', ''),
            'preview_text': self.config.get('preview_text', 'SAMPLE TEXT')
        }