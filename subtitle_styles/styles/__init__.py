"""
Subtitle Style Templates
Collection of pre-built subtitle styles inspired by Aicut
"""

from .simple_caption import SimpleCaptionStyle
from .background_caption import BackgroundCaptionStyle
from .glow_caption import GlowCaptionStyle

# Style registry
AVAILABLE_STYLES = {
    'simple': SimpleCaptionStyle,
    'background': BackgroundCaptionStyle,
    'glow': GlowCaptionStyle,
}

def get_style(style_id):
    """Get style class by ID"""
    if style_id not in AVAILABLE_STYLES:
        raise ValueError(f"Unknown style: {style_id}. Available styles: {list(AVAILABLE_STYLES.keys())}")
    return AVAILABLE_STYLES[style_id]()

__all__ = [
    'SimpleCaptionStyle',
    'BackgroundCaptionStyle', 
    'GlowCaptionStyle',
    'AVAILABLE_STYLES',
    'get_style'
]