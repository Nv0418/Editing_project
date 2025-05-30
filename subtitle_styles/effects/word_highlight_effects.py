"""
Word-by-word background highlighting effects for subtitle styles
Similar to karaoke color changes but using background highlights instead
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import List, Tuple, Optional

class WordHighlightEffects:
    """Text effects that highlight individual words with background colors based on audio timing"""
    
    @staticmethod
    def create_word_background_highlight_effect(words: List[str],
                                              font_path: str,
                                              font_size: int,
                                              text_color: Tuple[int, int, int],
                                              normal_bg_color: Optional[Tuple[int, int, int]] = None,
                                              highlight_bg_color: Tuple[int, int, int] = (138, 43, 226),  # Purple
                                              highlighted_word_index: int = -1,
                                              background_padding: Tuple[int, int] = (20, 10),
                                              corner_radius: int = 15,
                                              image_size: Tuple[int, int] = (1080, 200)) -> np.ndarray:
        """
        Create text with word-by-word background highlighting
        Each word can have its own background color based on audio timing
        
        Args:
            words: List of words to render
            font_path: Path to font file
            font_size: Font size in pixels
            text_color: RGB color for text
            normal_bg_color: RGB color for normal word backgrounds (None = transparent)
            highlight_bg_color: RGB color for highlighted word background
            highlighted_word_index: Index of word to highlight (-1 = none)
            background_padding: (x, y) padding around each word background
            corner_radius: Radius for rounded corners on backgrounds
            image_size: Output image dimensions
        """
        width, height = image_size
        padding = max(background_padding) * 3
        
        # Create main canvas
        img = Image.new('RGBA', (width + padding*2, height + padding*2), (0, 0, 0, 0))
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text layout - all words in one line
        full_text = ' '.join(words)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        total_width = bbox[2] - bbox[0]
        total_height = bbox[3] - bbox[1]
        
        # Auto-scale font if text is too wide (ensure 5% margins on each side)
        max_text_width = width * 0.9  # Use 90% of canvas width
        if total_width > max_text_width:
            scale_factor = max_text_width / total_width
            new_font_size = int(font_size * scale_factor)
            
            # Reload font with new size
            try:
                font = ImageFont.truetype(font_path, new_font_size)
            except:
                font = ImageFont.load_default()
                
            # Recalculate dimensions with new font
            bbox = draw.textbbox((0, 0), full_text, font=font)
            total_width = bbox[2] - bbox[0]
            total_height = bbox[3] - bbox[1]
            
            # Uncomment for debugging: print(f"Auto-scaled font in word highlight: {font_size}px -> {new_font_size}px")
        
        # Center the entire text block
        start_x = (width + padding*2 - total_width) // 2
        start_y = (height + padding*2 - total_height) // 2
        
        # Calculate individual word positions and sizes
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
        
        # Draw background highlights first (behind text)
        for i, word_pos in enumerate(word_positions):
            is_highlighted = (i == highlighted_word_index)
            
            # Only draw background for highlighted word
            if is_highlighted:
                bg_color = highlight_bg_color
            else:
                continue  # Skip background for normal words - they should have no background
            
            # Calculate background rectangle with padding
            bg_x = word_pos['x'] - background_padding[0]
            bg_y = word_pos['y'] - background_padding[1]
            bg_width = word_pos['width'] + (background_padding[0] * 2)
            bg_height = word_pos['height'] + (background_padding[1] * 2)
            
            # Draw rounded rectangle background
            if corner_radius > 0:
                draw.rounded_rectangle(
                    [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                    radius=corner_radius,
                    fill=(*bg_color, 255)
                )
            else:
                draw.rectangle(
                    [(bg_x, bg_y), (bg_x + bg_width, bg_y + bg_height)],
                    fill=(*bg_color, 255)
                )
        
        # Draw text on top of backgrounds
        for i, word_pos in enumerate(word_positions):
            draw.text(
                (word_pos['x'], word_pos['y']), 
                word_pos['word'], 
                font=font, 
                fill=(*text_color, 255)
            )
        
        # Crop to original size
        img = img.crop((padding, padding, width + padding, height + padding))
        
        return np.array(img)
    
    @staticmethod
    def create_gradient_word_highlight_effect(words: List[str],
                                            font_path: str,
                                            font_size: int,
                                            text_color: Tuple[int, int, int],
                                            gradient_start: Tuple[int, int, int] = (138, 43, 226),  # Purple
                                            gradient_end: Tuple[int, int, int] = (255, 20, 147),    # Pink
                                            highlighted_word_index: int = -1,
                                            background_padding: Tuple[int, int] = (25, 12),
                                            corner_radius: int = 20,
                                            image_size: Tuple[int, int] = (1080, 200)) -> np.ndarray:
        """
        Create text with gradient background highlighting for the active word
        Similar to word_background_highlight but with gradient backgrounds
        """
        width, height = image_size
        padding = max(background_padding) * 3
        
        # Create main canvas
        img = Image.new('RGBA', (width + padding*2, height + padding*2), (0, 0, 0, 0))
        
        # Load font and calculate layout (same as above)
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        full_text = ' '.join(words)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), full_text, font=font)
        total_width = bbox[2] - bbox[0]
        total_height = bbox[3] - bbox[1]
        
        # Auto-scale font if needed
        max_text_width = width * 0.9
        if total_width > max_text_width:
            scale_factor = max_text_width / total_width
            new_font_size = int(font_size * scale_factor)
            try:
                font = ImageFont.truetype(font_path, new_font_size)
            except:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), full_text, font=font)
            total_width = bbox[2] - bbox[0]
            total_height = bbox[3] - bbox[1]
        
        start_x = (width + padding*2 - total_width) // 2
        start_y = (height + padding*2 - total_height) // 2
        
        # Calculate word positions
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
            
            space_width = draw.textbbox((0, 0), ' ', font=font)[2]
            current_x += word_width + space_width
        
        # Draw gradient background for highlighted word only
        if highlighted_word_index >= 0 and highlighted_word_index < len(word_positions):
            word_pos = word_positions[highlighted_word_index]
            
            # Create gradient background
            bg_x = word_pos['x'] - background_padding[0]
            bg_y = word_pos['y'] - background_padding[1]
            bg_width = word_pos['width'] + (background_padding[0] * 2)
            bg_height = word_pos['height'] + (background_padding[1] * 2)
            
            # Create gradient image
            gradient = Image.new('RGBA', (bg_width, bg_height), (0, 0, 0, 0))
            gradient_draw = ImageDraw.Draw(gradient)
            
            # Simple horizontal gradient
            for x in range(bg_width):
                ratio = x / bg_width
                r = int(gradient_start[0] * (1 - ratio) + gradient_end[0] * ratio)
                g = int(gradient_start[1] * (1 - ratio) + gradient_end[1] * ratio)
                b = int(gradient_start[2] * (1 - ratio) + gradient_end[2] * ratio)
                
                gradient_draw.line([(x, 0), (x, bg_height)], fill=(r, g, b, 255))
            
            # Apply corner radius if needed
            if corner_radius > 0:
                # Create mask for rounded corners
                mask = Image.new('L', (bg_width, bg_height), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rounded_rectangle(
                    [(0, 0), (bg_width, bg_height)],
                    radius=corner_radius,
                    fill=255
                )
                gradient.putalpha(mask)
            
            # Paste gradient onto main image
            img.paste(gradient, (bg_x, bg_y), gradient)
        
        # Draw text on top
        for word_pos in word_positions:
            draw.text(
                (word_pos['x'], word_pos['y']), 
                word_pos['word'], 
                font=font, 
                fill=(*text_color, 255)
            )
        
        # Crop to original size
        img = img.crop((padding, padding, width + padding, height + padding))
        
        return np.array(img)