"""
Word-by-word background highlighting effects for subtitle styles
Fixed version with proper centering for Deep Diver
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import List, Tuple, Optional

# Import everything from the original
from subtitle_styles.effects.word_highlight_effects import *

class WordHighlightEffects:
    """Text effects that highlight individual words with background colors based on audio timing"""
    
    # Copy other methods from original
    create_word_background_highlight_effect = staticmethod(
        __import__('subtitle_styles.effects.word_highlight_effects', fromlist=['WordHighlightEffects']).WordHighlightEffects.create_word_background_highlight_effect
    )
    
    create_gradient_word_highlight_effect = staticmethod(
        __import__('subtitle_styles.effects.word_highlight_effects', fromlist=['WordHighlightEffects']).WordHighlightEffects.create_gradient_word_highlight_effect
    )
    
    @staticmethod
    def create_deep_diver_effect(words: List[str],
                                font_path: str,
                                font_size: int,
                                active_text_color: Tuple[int, int, int] = (0, 0, 0),  # Black for active
                                inactive_text_color: Tuple[int, int, int] = (128, 128, 128),  # Grey for inactive
                                background_color: Tuple[int, int, int] = (192, 192, 192),  # Light grey background
                                highlighted_word_index: int = -1,
                                background_padding: Tuple[int, int] = (40, 15),
                                corner_radius: int = 25,
                                image_size: Tuple[int, int] = (1080, 200)) -> np.ndarray:
        """
        Create deep diver effect with proper centering - FIXED VERSION
        """
        width, height = image_size
        
        # Create main canvas WITHOUT extra padding
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text layout - all words in one line
        full_text = ' '.join(words)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        total_width = bbox[2] - bbox[0]
        total_height = bbox[3] - bbox[1]
        
        # Auto-scale font if text is too wide
        max_text_width = width * 0.85  # Use 85% of canvas width
        if total_width > max_text_width:
            scale_factor = max_text_width / total_width
            new_font_size = int(font_size * scale_factor)
            
            try:
                font = ImageFont.truetype(font_path, new_font_size)
            except:
                font = ImageFont.load_default()
                
            # Recalculate dimensions with new font
            bbox = draw.textbbox((0, 0), full_text, font=font)
            total_width = bbox[2] - bbox[0]
            total_height = bbox[3] - bbox[1]
        
        # Get font metrics for proper vertical centering
        ascent, descent = font.getmetrics()
        text_height = ascent + descent
        
        # Center the entire text block horizontally ON THE ACTUAL CANVAS
        # Manual adjustment: shift left by 30 pixels to fix centering issue
        start_x = (width - total_width) // 2 - 30
        
        # Center the text vertically using font metrics
        canvas_center_y = height // 2
        start_y = canvas_center_y - ascent // 2
        
        # Calculate background rectangle for entire text with padding
        bg_x = start_x - background_padding[0]
        bg_y = canvas_center_y - text_height//2 - background_padding[1]
        bg_width = total_width + (background_padding[0] * 2)
        bg_height = text_height + (background_padding[1] * 2)
        
        # Draw grey background for entire text block
        if corner_radius > 0:
            draw.rounded_rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                radius=corner_radius,
                fill=(*background_color, 255)
            )
        else:
            draw.rectangle(
                [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                fill=(*background_color, 255)
            )
        
        # Calculate individual word positions
        word_positions = []
        current_x = start_x
        
        for word in words:
            word_bbox = draw.textbbox((0, 0), word, font=font)
            word_width = word_bbox[2] - word_bbox[0]
            word_height = word_bbox[3] - word_bbox[1]
            
            word_positions.append({
                'word': word,
                'x': current_x,
                'y': start_y,
                'width': word_width,
                'height': word_height
            })
            
            # Move to next word position (add space)
            space_width = draw.textbbox((0, 0), ' ', font=font)[2]
            current_x += word_width + space_width
        
        # Draw text with appropriate colors
        for i, word_pos in enumerate(word_positions):
            is_highlighted = (i == highlighted_word_index)
            text_color = active_text_color if is_highlighted else inactive_text_color
            
            draw.text(
                (word_pos['x'], word_pos['y']), 
                word_pos['word'], 
                font=font, 
                fill=(*text_color, 255)
            )
        
        # Return the image as numpy array (no cropping needed)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        return np.array(img)