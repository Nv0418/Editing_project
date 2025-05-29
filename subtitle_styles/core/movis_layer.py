"""
Movis-compatible subtitle layer
Integrates styled subtitles into Movis compositions
"""

import movis as mv
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from PIL import Image


class StyledSubtitleLayer:
    """
    A Movis-compatible layer that renders styled subtitles
    Can be added to any Movis composition
    """
    
    def __init__(self, 
                 words: List[Dict[str, Any]], 
                 style,
                 resolution: Tuple[int, int] = (1080, 1920),
                 position: str = 'bottom',
                 safe_zones: bool = True):
        """
        Initialize styled subtitle layer
        
        Args:
            words: List of word dictionaries with 'word', 'start', 'end' keys
            style: Style instance (SimpleCaptionStyle, etc.)
            resolution: Video resolution (width, height)
            position: Vertical position ('top', 'center', 'bottom')
            safe_zones: Whether to respect Instagram safe zones
        """
        self.words = words
        self.style = style
        self.resolution = resolution
        self.position = position
        self.safe_zones = safe_zones
        
        # Calculate duration from words
        if words:
            self.duration = max(w['end'] for w in words) + 1.0
        else:
            self.duration = 0.0
        
        # Pre-calculate position with adjusted margins
        self.text_position = self.style.calculate_safe_position(
            resolution, position, safe_zones
        )
        
        # Store safe area bounds for text constraint
        self.safe_left = 100 if safe_zones else 50  # Increased from 35
        self.safe_right = resolution[0] - 100 if safe_zones else resolution[0] - 50
        self.safe_width = self.safe_right - self.safe_left
        
        # Group words into windows (3 words per window for now)
        self.word_windows = self._create_word_windows()
        
    def _create_word_windows(self, words_per_window: int = 3):
        """Group words into display windows"""
        windows = []
        
        for i in range(0, len(self.words), words_per_window):
            window_words = self.words[i:i + words_per_window]
            if window_words:
                window = {
                    'words': window_words,
                    'start': window_words[0]['start'],
                    'end': window_words[-1]['end'],
                    'text': ' '.join(w['word'] for w in window_words)
                }
                windows.append(window)
        
        return windows
    
    def __call__(self, time: float) -> Optional[np.ndarray]:
        """
        Render the subtitle at the given time
        Returns RGBA numpy array or None
        """
        if time < 0 or time > self.duration:
            return None
        
        # Find active window
        active_window = None
        for window in self.word_windows:
            if window['start'] <= time <= window['end']:
                active_window = window
                break
        
        if not active_window:
            return None
        
        # Create blank canvas
        canvas = np.zeros((*self.resolution[::-1], 4), dtype=np.uint8)
        
        # Determine which word is currently speaking
        current_word_idx = None
        for i, word in enumerate(active_window['words']):
            if word['start'] <= time <= word['end']:
                current_word_idx = i
                break
        
        # Render based on style type
        # For JSON-based styles, check effect_type
        if hasattr(self.style, 'json_config'):
            effect_type = self.style.config.get('effect_type', 'simple')
            if effect_type == 'outline':
                return self._render_simple_style(canvas, active_window, current_word_idx, time)
            elif effect_type == 'background':
                return self._render_background_style(canvas, active_window, current_word_idx, time)
            elif effect_type == 'glow':
                return self._render_glow_style(canvas, active_window, current_word_idx, time)
            else:
                return self._render_simple_style(canvas, active_window, current_word_idx, time)
        else:
            # Original class-based rendering
            style_name = self.style.__class__.__name__
            
            if 'Simple' in style_name:
                return self._render_simple_style(canvas, active_window, current_word_idx, time)
            elif 'Background' in style_name:
                return self._render_background_style(canvas, active_window, current_word_idx, time)
            elif 'Glow' in style_name:
                return self._render_glow_style(canvas, active_window, current_word_idx, time)
            else:
                # Fallback rendering
                return self._render_simple_style(canvas, active_window, current_word_idx, time)
    
    def _render_simple_style(self, canvas, window, highlight_idx, time):
        """Render simple caption style with outline"""
        # For simple style, show the whole phrase with word highlighting
        text = window['text']
        is_highlighted = highlight_idx is not None
        
        # Get styled text image with constrained width
        # Check if style has create_styled_text method (JSON-based)
        if hasattr(self.style, 'create_styled_text'):
            text_img = self.style.create_styled_text(
                text, 
                self.style.config['typography']['font_size'],
                time,
                is_highlighted
            )
        else:
            # Fallback to old method
            text_img = self.style.create_text_with_outline(
                text, 
                self.style.config['typography']['font_size'],
                is_highlighted
            )
        
        # Check if text exceeds safe width and resize if needed
        if text_img.shape[1] > self.safe_width:
            scale_factor = self.safe_width / text_img.shape[1]
            new_width = int(text_img.shape[1] * scale_factor)
            new_height = int(text_img.shape[0] * scale_factor)
            
            from PIL import Image
            img_pil = Image.fromarray(text_img)
            img_pil = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            text_img = np.array(img_pil)
        
        # Center on canvas
        return self._composite_center(canvas, text_img)
    
    def _render_background_style(self, canvas, window, highlight_idx, time):
        """Render background caption style"""
        text = window['text']
        is_highlighted = highlight_idx is not None
        
        # Get styled text with background
        # Check if style has create_styled_text method (JSON-based)
        if hasattr(self.style, 'create_styled_text'):
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                is_highlighted
            )
        else:
            text_img = self.style.create_text_with_background(
                text,
                self.style.config['typography']['font_size'],
                is_highlighted
            )
        
        # Check if text exceeds safe width and resize if needed
        if text_img.shape[1] > self.safe_width:
            scale_factor = self.safe_width / text_img.shape[1]
            new_width = int(text_img.shape[1] * scale_factor)
            new_height = int(text_img.shape[0] * scale_factor)
            
            from PIL import Image
            img_pil = Image.fromarray(text_img)
            img_pil = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            text_img = np.array(img_pil)
        
        return self._composite_center(canvas, text_img)
    
    def _render_glow_style(self, canvas, window, highlight_idx, time):
        """Render glow caption style"""
        text = window['text']
        is_highlighted = highlight_idx is not None
        
        # Get styled text with glow
        # Check if style has create_styled_text method (JSON-based)
        if hasattr(self.style, 'create_styled_text'):
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                is_highlighted
            )
        else:
            text_img = self.style.create_glowing_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                is_highlighted
            )
        
        # Check if text exceeds safe width and resize if needed
        if text_img.shape[1] > self.safe_width:
            scale_factor = self.safe_width / text_img.shape[1]
            new_width = int(text_img.shape[1] * scale_factor)
            new_height = int(text_img.shape[0] * scale_factor)
            
            from PIL import Image
            img_pil = Image.fromarray(text_img)
            img_pil = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            text_img = np.array(img_pil)
        
        return self._composite_center(canvas, text_img)
    
    def _composite_center(self, canvas, text_img):
        """Composite text image onto canvas at designated position"""
        if text_img.shape[0] > canvas.shape[0] or text_img.shape[1] > canvas.shape[1]:
            # Text image is larger than canvas, need to crop or resize
            # For now, let's crop to fit
            text_img = text_img[:canvas.shape[0], :canvas.shape[1]]
        
        # Calculate position to center text at designated position
        text_h, text_w = text_img.shape[:2]
        canvas_h, canvas_w = canvas.shape[:2]
        
        x = self.text_position[0] - text_w // 2
        y = self.text_position[1] - text_h // 2
        
        # Ensure text stays within safe bounds horizontally
        x = max(self.safe_left, min(x, self.safe_right - text_w))
        
        # Ensure within vertical bounds
        y = max(0, min(y, canvas_h - text_h))
        
        # Composite
        x_end = x + text_w
        y_end = y + text_h
        
        # Alpha blend
        alpha = text_img[..., 3:4] / 255.0
        canvas[y:y_end, x:x_end, :3] = (
            canvas[y:y_end, x:x_end, :3] * (1 - alpha) + 
            text_img[..., :3] * alpha
        ).astype(np.uint8)
        canvas[y:y_end, x:x_end, 3] = np.maximum(
            canvas[y:y_end, x:x_end, 3], 
            text_img[..., 3]
        )
        
        return canvas
    
    def get_key(self, time: float):
        """Get cache key for this time"""
        # Find active window
        for i, window in enumerate(self.word_windows):
            if window['start'] <= time <= window['end']:
                # Find highlighted word
                highlight_idx = None
                for j, word in enumerate(window['words']):
                    if word['start'] <= time <= word['end']:
                        highlight_idx = j
                        break
                return (self.style.__class__.__name__, i, highlight_idx, round(time, 1))
        return None