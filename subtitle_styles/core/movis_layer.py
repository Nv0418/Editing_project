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
        self.safe_left = 50 if safe_zones else 30  # Reduced to match base_style
        self.safe_right = resolution[0] - 50 if safe_zones else resolution[0] - 30
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
            elif effect_type == 'dual_glow':
                return self._render_dual_glow_style(canvas, active_window, current_word_idx, time)
            elif effect_type == 'text_shadow':
                return self._render_text_shadow_style(canvas, active_window, current_word_idx, time)
            elif effect_type == 'word_highlight':
                return self._render_word_highlight_style(canvas, active_window, current_word_idx, time)
            elif effect_type == 'deep_diver':
                return self._render_deep_diver_style(canvas, active_window, current_word_idx, time)
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
    
    def _render_dual_glow_style(self, canvas, window, highlight_idx, time):
        """Render dual-tone glow caption style (white + red words)"""
        text = window['text']
        
        # Get styled text with dual glow effect
        if hasattr(self.style, 'create_styled_text'):
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                False,  # is_highlighted (not used for dual glow)
                highlight_idx  # word_index for highlighting
            )
        else:
            # Fallback to simple rendering
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                False
            )
        
        # Check if text exceeds safe width and resize if needed
        if text_img.shape[1] > self.safe_width:
            scale_factor = self.safe_width / text_img.shape[1]
            # Add some padding to ensure text doesn't touch edges
            scale_factor *= 0.95  # Use 95% of available width for safety
            new_width = int(text_img.shape[1] * scale_factor)
            new_height = int(text_img.shape[0] * scale_factor)
            
            # Uncomment for debugging: print(f"Auto-scaling karaoke text: {text_img.shape[1]}px -> {new_width}px (factor: {scale_factor:.2f})")
            
            from PIL import Image
            img_pil = Image.fromarray(text_img)
            img_pil = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            text_img = np.array(img_pil)
        
        return self._composite_center(canvas, text_img)
    
    def _render_word_highlight_style(self, canvas, window, highlight_idx, time):
        """Render word-by-word background highlighting style (like highlight caption)"""
        from subtitle_styles.effects.word_highlight_effects import WordHighlightEffects
        
        text = window['text']
        words = text.split()
        
        # Get style configuration
        typo = self.style.config['typography']
        effects = self.style.config.get('effect_parameters', {})
        
        # Transform text if needed
        if typo.get('text_transform') == 'uppercase':
            words = [word.upper() for word in words]
        
        # Get colors
        text_color = tuple(typo['colors']['text'])
        normal_bg_color = typo['colors'].get('background')
        highlight_bg_color = typo['colors'].get('background_highlighted', 
                                                typo['colors'].get('background', [138, 43, 226]))
        
        # Get effect parameters
        bg_padding = effects.get('background_padding', {'x': 20, 'y': 10})
        if isinstance(bg_padding, dict):
            padding_tuple = (bg_padding.get('x', 20), bg_padding.get('y', 10))
        else:
            padding_tuple = (bg_padding, bg_padding // 2)
        
        corner_radius = effects.get('rounded_corners', 15)
        
        # Create word highlight effect
        text_img = WordHighlightEffects.create_word_background_highlight_effect(
            words=words,
            font_path=typo['font_family'],
            font_size=int(typo['font_size']),
            text_color=text_color,
            normal_bg_color=normal_bg_color,
            highlight_bg_color=highlight_bg_color,
            highlighted_word_index=highlight_idx if highlight_idx is not None else -1,
            background_padding=padding_tuple,
            corner_radius=corner_radius,
            image_size=(1080, 200)
        )
        
        # Check if text exceeds safe width and resize if needed
        if text_img.shape[1] > self.safe_width:
            scale_factor = self.safe_width / text_img.shape[1]
            # Add some padding to ensure text doesn't touch edges
            scale_factor *= 0.95  # Use 95% of available width for safety
            new_width = int(text_img.shape[1] * scale_factor)
            new_height = int(text_img.shape[0] * scale_factor)
            
            # Uncomment for debugging: print(f"Auto-scaling word highlight text: {text_img.shape[1]}px -> {new_width}px (factor: {scale_factor:.2f})")
            
            from PIL import Image
            img_pil = Image.fromarray(text_img)
            img_pil = img_pil.resize((new_width, new_height), Image.Resampling.LANCZOS)
            text_img = np.array(img_pil)
        
        return self._composite_center(canvas, text_img)
    
    def _render_text_shadow_style(self, canvas, window, highlight_idx, time):
        """Render text-shadow glow caption style with currentColor logic"""
        text = window['text']
        
        # Get styled text with text shadow effect
        if hasattr(self.style, 'create_styled_text'):
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                False,  # is_highlighted (not used for text shadow)
                highlight_idx  # word_index for highlighting
            )
        else:
            # Fallback to simple rendering
            text_img = self.style.create_styled_text(
                text,
                self.style.config['typography']['font_size'],
                time,
                False
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
    
    def _render_deep_diver_style(self, canvas, window, highlight_idx, time):
        """Render deep diver style with full background and word color changes"""
        from subtitle_styles.effects.word_highlight_effects import WordHighlightEffects
        
        # Get the words from window
        words = [w['word'] for w in window['words']]
        
        # Get style configuration
        typo = self.style.config['typography']
        effects = self.style.config.get('effect_parameters', {})
        
        # Transform text if needed
        if typo.get('text_transform') == 'uppercase':
            words = [word.upper() for word in words]
        elif typo.get('text_transform') == 'lowercase':
            words = [word.lower() for word in words]
        
        # Get colors for deep diver
        active_text_color = tuple(typo['colors'].get('active_text', [0, 0, 0]))
        inactive_text_color = tuple(typo['colors'].get('inactive_text', [128, 128, 128]))
        background_color = tuple(typo['colors'].get('background', [192, 192, 192]))
        
        # Get effect parameters
        bg_padding = effects.get('background_padding', {'x': 25, 'y': 10})
        if isinstance(bg_padding, dict):
            padding_tuple = (bg_padding.get('x', 25), bg_padding.get('y', 10))
        else:
            padding_tuple = (bg_padding, bg_padding // 2)
        
        corner_radius = effects.get('corner_radius', 20)
        
        # Create deep diver effect
        text_img = WordHighlightEffects.create_deep_diver_effect(
            words=words,
            font_path=typo['font_family'],
            font_size=int(typo['font_size']),
            active_text_color=active_text_color,
            inactive_text_color=inactive_text_color,
            background_color=background_color,
            highlighted_word_index=highlight_idx if highlight_idx is not None else -1,
            background_padding=padding_tuple,
            corner_radius=corner_radius,
            image_size=(1080, 200)
        )
        
        # Composite onto canvas
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
        x_end = min(x + text_w, canvas_w)
        y_end = min(y + text_h, canvas_h)
        
        # Adjust text image if it needs to be cropped
        text_w_actual = x_end - x
        text_h_actual = y_end - y
        if text_w_actual < text_w or text_h_actual < text_h:
            text_img = text_img[:text_h_actual, :text_w_actual]
        
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