"""
Word-by-word background highlighting effects for subtitle styles
Fixed version with proper centering for Deep Diver - V2 with precise centering
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
        Create deep diver effect with precise centering - V2
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
        
        # Get the actual bounding box of the text
        # Use a temporary draw to get accurate measurements
        temp_img = Image.new('RGBA', (width * 2, height * 2), (0, 0, 0, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Draw text at a known position to measure
        test_x, test_y = 100, 100
        temp_draw.text((test_x, test_y), full_text, font=font, fill=(255, 255, 255, 255))
        
        # Get the actual bounding box of the drawn text
        bbox = temp_img.getbbox()
        if bbox:
            actual_text_width = bbox[2] - bbox[0]
            actual_text_height = bbox[3] - bbox[1]
            # Calculate the offset between where we drew and where the text actually started
            text_offset_x = bbox[0] - test_x
            text_offset_y = bbox[1] - test_y
        else:
            # Fallback to textbbox if getbbox fails
            bbox = draw.textbbox((0, 0), full_text, font=font)
            actual_text_width = bbox[2] - bbox[0]
            actual_text_height = bbox[3] - bbox[1]
            text_offset_x = bbox[0]
            text_offset_y = bbox[1]
        
        # Auto-scale font if text is too wide
        max_text_width = width * 0.85  # Use 85% of canvas width
        if actual_text_width > max_text_width:
            scale_factor = max_text_width / actual_text_width
            new_font_size = int(font_size * scale_factor)
            
            try:
                font = ImageFont.truetype(font_path, new_font_size)
            except:
                font = ImageFont.load_default()
            
            # Recalculate dimensions with new font
            temp_img = Image.new('RGBA', (width * 2, height * 2), (0, 0, 0, 0))
            temp_draw = ImageDraw.Draw(temp_img)
            temp_draw.text((test_x, test_y), full_text, font=font, fill=(255, 255, 255, 255))
            bbox = temp_img.getbbox()
            if bbox:
                actual_text_width = bbox[2] - bbox[0]
                actual_text_height = bbox[3] - bbox[1]
                text_offset_x = bbox[0] - test_x
                text_offset_y = bbox[1] - test_y
            else:
                bbox = draw.textbbox((0, 0), full_text, font=font)
                actual_text_width = bbox[2] - bbox[0]
                actual_text_height = bbox[3] - bbox[1]
                text_offset_x = bbox[0]
                text_offset_y = bbox[1]
        
        # Calculate the true center position accounting for text rendering offsets
        # This ensures the visual center of the text + background is centered
        bg_width = actual_text_width + (background_padding[0] * 2)
        bg_height = actual_text_height + (background_padding[1] * 2)
        
        # Center the background box
        bg_x = (width - bg_width) // 2
        bg_y = (height - bg_height) // 2
        
        # Calculate text position within the centered background
        # Account for the text rendering offset
        start_x = bg_x + background_padding[0] - text_offset_x
        start_y = bg_y + background_padding[1] - text_offset_y
        
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