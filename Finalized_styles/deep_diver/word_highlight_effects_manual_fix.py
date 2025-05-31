"""
Word-by-word background highlighting effects for subtitle styles
Manual fix version with adjustable horizontal offset for Deep Diver
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import List, Tuple, Optional

# Import the original class
from subtitle_styles.effects.word_highlight_effects import WordHighlightEffects as OriginalWordHighlightEffects

class WordHighlightEffects:
    """Text effects with manual offset fix for Deep Diver"""
    
    # Copy other methods from original
    create_word_background_highlight_effect = OriginalWordHighlightEffects.create_word_background_highlight_effect
    create_full_background_with_word_highlight = OriginalWordHighlightEffects.create_full_background_with_word_highlight
    create_horizontal_flip_effect = OriginalWordHighlightEffects.create_horizontal_flip_effect
    create_underline_effect = OriginalWordHighlightEffects.create_underline_effect
    
    @staticmethod
    def create_deep_diver_effect(words: List[str],
                                font_path: str,
                                font_size: int,
                                active_text_color: Tuple[int, int, int] = (0, 0, 0),
                                inactive_text_color: Tuple[int, int, int] = (128, 128, 128),
                                background_color: Tuple[int, int, int] = (192, 192, 192),
                                highlighted_word_index: int = -1,
                                background_padding: Tuple[int, int] = (40, 15),
                                corner_radius: int = 25,
                                image_size: Tuple[int, int] = (1080, 200)) -> np.ndarray:
        """
        Create deep diver effect with manual horizontal offset
        ADJUST THE MANUAL_OFFSET VALUE BELOW TO FINE-TUNE CENTERING
        """
        # *** ADJUST THIS VALUE TO SHIFT THE TEXT LEFT (negative) OR RIGHT (positive) ***
        MANUAL_OFFSET = -40  # pixels to shift left
        
        # Call the original implementation
        result = OriginalWordHighlightEffects.create_deep_diver_effect(
            words=words,
            font_path=font_path,
            font_size=font_size,
            active_text_color=active_text_color,
            inactive_text_color=inactive_text_color,
            background_color=background_color,
            highlighted_word_index=highlighted_word_index,
            background_padding=background_padding,
            corner_radius=corner_radius,
            image_size=image_size
        )
        
        # Apply horizontal shift
        if MANUAL_OFFSET != 0:
            # Create new canvas
            shifted_img = np.zeros_like(result)
            
            # Calculate shift boundaries
            if MANUAL_OFFSET < 0:  # Shift left
                src_start = -MANUAL_OFFSET
                src_end = image_size[0]
                dst_start = 0
                dst_end = image_size[0] + MANUAL_OFFSET
            else:  # Shift right
                src_start = 0
                src_end = image_size[0] - MANUAL_OFFSET
                dst_start = MANUAL_OFFSET
                dst_end = image_size[0]
            
            # Copy shifted content
            shifted_img[:, dst_start:dst_end] = result[:, src_start:src_end]
            
            return shifted_img
        
        return result