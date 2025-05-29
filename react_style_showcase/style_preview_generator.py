#!/usr/bin/env python3
"""
Style Preview Generator
Generates accurate preview images using the actual subtitle rendering system
"""

import os
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from subtitle_styles.effects.text_effects import TextEffects

class StylePreviewGenerator:
    def __init__(self):
        script_dir = Path(__file__).resolve().parent
        self.config_path = script_dir / "subtitle_styles/config/subtitle_styles_v3.json"
        self.text_effects = TextEffects()
        self.canvas_size = (400, 150)  # Preview canvas size
        self.background_color = (0, 0, 0, 255)  # Black background
        
    def load_styles_config(self):
        """Load the styles configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading styles config: {e}")
            return {}
    
    def generate_preview(self, style_id, text="SAMPLE TEXT"):
        """Generate a preview image for a specific style using actual rendering logic"""
        print(f"[Generator Script] generate_preview called with style_id='{style_id}', text='{text}'") # Log text in generate_preview
        try:
            styles = self.load_styles_config()
            if style_id not in styles:
                print(f"Style '{style_id}' not found")
                return None
                
            style_config = styles[style_id]
            
            # Create canvas
            canvas = Image.new('RGBA', self.canvas_size, self.background_color)
            
            # Get style settings
            typography = style_config.get('typography', {})
            effect_type = style_config.get('effect_type', 'outline')
            effect_params = style_config.get('effect_parameters', {})
            
            # Apply text transform
            if typography.get('text_transform') == 'uppercase':
                text = text.upper()
            elif typography.get('text_transform') == 'lowercase':
                text = text.lower()
            
            # Get font settings
            font_family = typography.get('font_family', 'Arial')
            font_size = int(typography.get('font_size', 48) * 0.4)  # Scale down for preview
            
            # Use the actual text effects from the subtitle system
            if effect_type == 'outline':
                text_image = self._create_outline_preview(text, font_family, font_size, typography, effect_params)
            elif effect_type == 'background':
                text_image = self._create_background_preview(text, font_family, font_size, typography, effect_params)
            elif effect_type == 'glow':
                text_image = self._create_glow_preview(text, font_family, font_size, typography, effect_params)
            else:
                text_image = self._create_simple_preview(text, font_family, font_size, typography)
                
            if text_image is not None:
                # Convert numpy array to PIL Image if needed
                if isinstance(text_image, np.ndarray):
                    text_image = Image.fromarray(text_image)
                
                # Resize to fit canvas while maintaining aspect ratio
                text_image.thumbnail(self.canvas_size, Image.Resampling.LANCZOS)
                
                # Center on canvas
                x = (self.canvas_size[0] - text_image.width) // 2
                y = (self.canvas_size[1] - text_image.height) // 2
                
                canvas.paste(text_image, (x, y), text_image)
                
            return canvas
            
        except Exception as e:
            print(f"Error generating preview for {style_id}: {e}")
            return None
    
    def _create_outline_preview(self, text, font_family, font_size, typography, effect_params):
        """Create outline effect preview using TextEffects"""
        try:
            text_color = tuple(typography.get('colors', {}).get('text', [255, 255, 255]))
            outline_color = tuple(effect_params.get('outline_color', [0, 0, 0]))
            outline_width = effect_params.get('outline_width', 2)
            
            return TextEffects.create_outline_effect(
                text=text,
                font_path=font_family,
                font_size=font_size,
                text_color=text_color,
                outline_color=outline_color,
                outline_width=outline_width,
                image_size=self.canvas_size
            )
        except Exception as e:
            print(f"Error creating outline preview: {e}")
            return self._create_fallback_preview(text, font_family, font_size, typography)
    
    def _create_background_preview(self, text, font_family, font_size, typography, effect_params):
        """Create background effect preview (manual implementation)"""
        try:
            # Create image
            img = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Load font
            font_loaded = False
            font_extensions = ['.ttf', '.otf']
            script_dir = Path(__file__).resolve().parent
            font_base_path = script_dir / "subtitle_styles/fonts/"
            
            font_to_try = None
            # Attempt to load from local fonts folder first
            for ext in font_extensions:
                potential_font_path = font_base_path / (font_family + ext)
                if potential_font_path.exists():
                    font_to_try = str(potential_font_path)
                    break
            
            if font_to_try:
                try:
                    font = ImageFont.truetype(font_to_try, font_size)
                    font_loaded = True
                except Exception: 
                    pass # Will try system font next

            # If not loaded, try system font by name
            if not font_loaded: 
                try:
                    font = ImageFont.truetype(font_family, font_size)
                    font_loaded = True
                except Exception: 
                    pass # Will use default font next
            
            # If still not loaded, use default font
            if not font_loaded: 
                try:
                    font = ImageFont.load_default()
                    print(f"Warning: Font '{font_family}' not found locally or in system. Using default font for style preview.")
                except Exception as e_default:
                    print(f"CRITICAL: Default font failed to load: {e_default}")
                    # Create an error image if default font also fails
                    error_img = Image.new('RGBA', self.canvas_size, (50, 0, 0, 255)) # Dark red background
                    draw_error = ImageDraw.Draw(error_img)
                    try: 
                        # Attempt to draw error message with a truly basic default if possible
                        error_font_fallback = ImageFont.load_default() 
                        draw_error.text((10,10), "Font Load Error", font=error_font_fallback, fill=(255,255,255))
                    except: 
                        # If even this fails, the image will just be dark red
                        pass
                    return np.array(error_img)

            # Colors
            text_color = tuple(typography.get('colors', {}).get('text', [255, 255, 255]))
            
            # Get background color from different possible locations
            bg_color = None
            if 'background_color' in effect_params:
                bg_color = tuple(effect_params['background_color'])
            elif 'background' in typography.get('colors', {}):
                bg_color = tuple(typography['colors']['background'])
            else:
                bg_color = (0, 255, 255, 255)  # Default cyan
            
            # Get padding
            padding = effect_params.get('padding', effect_params.get('background_padding', {'horizontal': 20, 'vertical': 10}))
            if isinstance(padding, dict):
                pad_x = padding.get('horizontal', padding.get('x', 10))
                pad_y = padding.get('vertical', padding.get('y', 5))
            else:
                pad_x = pad_y = padding
            
            # Scale padding for preview
            pad_x = int(pad_x * 0.5)
            pad_y = int(pad_y * 0.5)
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate background dimensions
            bg_width = text_width + (pad_x * 2)
            bg_height = text_height + (pad_y * 2)
            
            # Center everything
            bg_x = (self.canvas_size[0] - bg_width) // 2
            bg_y = (self.canvas_size[1] - bg_height) // 2
            
            text_x = bg_x + pad_x
            text_y = bg_y + pad_y
            
            # Draw background
            draw.rectangle([bg_x, bg_y, bg_x + bg_width, bg_y + bg_height], fill=bg_color)
            
            # Draw text
            draw.text((text_x, text_y), text, font=font, fill=text_color)
            
            return np.array(img)
            
        except Exception as e:
            print(f"Error creating background preview: {e}")
            return self._create_fallback_preview(text, font_family, font_size, typography)
    
    def _create_glow_preview(self, text, font_family, font_size, typography, effect_params):
        """Create glow effect preview using TextEffects"""
        try:
            text_color = tuple(typography.get('colors', {}).get('text', [255, 255, 255]))
            glow_color = tuple(typography.get('colors', {}).get('glow', [255, 20, 147]))
            glow_radius = effect_params.get('glow_radius', 15)
            glow_intensity = effect_params.get('glow_intensity', 0.8)
            
            return TextEffects.create_glow_effect(
                text=text,
                font_path=font_family,
                font_size=font_size,
                text_color=text_color,
                glow_color=glow_color,
                glow_radius=int(glow_radius * 0.5),  # Scale down for preview
                glow_intensity=glow_intensity,
                image_size=self.canvas_size
            )
        except Exception as e:
            print(f"Error creating glow preview: {e}")
            return self._create_fallback_preview(text, font_family, font_size, typography)
    
    def _create_simple_preview(self, text, font_family, font_size, typography):
        """Create simple text preview"""
        return self._create_fallback_preview(text, font_family, font_size, typography)
    
    def _create_fallback_preview(self, text, font_family, font_size, typography):
        """Create a simple fallback preview using PIL"""
        try:
            img = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Try to load font
            font_loaded = False
            font_extensions = ['.ttf', '.otf']
            script_dir = Path(__file__).resolve().parent
            font_base_path = script_dir / "subtitle_styles/fonts/"
            
            font_to_try = None
            # Attempt to load from local fonts folder first
            for ext in font_extensions:
                potential_font_path = font_base_path / (font_family + ext)
                if potential_font_path.exists():
                    font_to_try = str(potential_font_path)
                    break
            
            if font_to_try:
                try:
                    font = ImageFont.truetype(font_to_try, font_size)
                    font_loaded = True
                except Exception: 
                    pass # Will try system font next

            # If not loaded, try system font by name
            if not font_loaded: 
                try:
                    font = ImageFont.truetype(font_family, font_size)
                    font_loaded = True
                except Exception: 
                    pass # Will use default font next
            
            # If still not loaded, use default font
            if not font_loaded: 
                try:
                    font = ImageFont.load_default()
                    print(f"Warning: Font '{font_family}' not found locally or in system. Using default font for style preview.")
                except Exception as e_default:
                    print(f"CRITICAL: Default font failed to load: {e_default}")
                    # Create an error image if default font also fails
                    error_img = Image.new('RGBA', self.canvas_size, (50, 0, 0, 255)) # Dark red background
                    draw_error = ImageDraw.Draw(error_img)
                    try: 
                        # Attempt to draw error message with a truly basic default if possible
                        error_font_fallback = ImageFont.load_default() 
                        draw_error.text((10,10), "Font Load Error", font=error_font_fallback, fill=(255,255,255))
                    except: 
                        # If even this fails, the image will just be dark red
                        pass
                    return np.array(error_img)

            # Get text color
            text_color = tuple(typography.get('colors', {}).get('text', [255, 255, 255]))
            
            # Get text bounds and center
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.canvas_size[0] - text_width) // 2
            y = (self.canvas_size[1] - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, font=font, fill=text_color)
            
            return np.array(img)
            
        except Exception as e:
            print(f"Error creating fallback preview: {e}")
            return None
    
    def generate_all_previews(self, text="SAMPLE TEXT", output_dir="style_previews"):
        """Generate previews for all available styles"""
        print(f"[Generator Script] generate_all_previews called with text='{text}'") # Log text in generate_all_previews
        os.makedirs(output_dir, exist_ok=True)
        
        styles = self.load_styles_config()
        results = {}
        
        print(f"Generating previews for {len(styles)} styles...")
        
        for style_id in styles:
            print(f"  Generating preview for {style_id}...")
            preview = self.generate_preview(style_id, text)
            
            if preview:
                output_path = os.path.join(output_dir, f"{style_id}_preview.png")
                preview.save(output_path)
                results[style_id] = output_path
                print(f"    Saved: {output_path}")
            else:
                print(f"    Failed to generate preview for {style_id}")
                
        return results

def main():
    parser = argparse.ArgumentParser(description='Generate accurate style previews')
    parser.add_argument('--text', default='SAMPLE TEXT', help='Text to render')
    parser.add_argument('--style', help='Specific style to preview')
    parser.add_argument('--output', default='style_previews', help='Output directory')
    
    args = parser.parse_args()
    
    print(f"[Generator Script] main received args: style='{args.style}', text='{args.text}', output='{args.output}'") # Log args.text in main
    
    generator = StylePreviewGenerator()
    
    if args.style:
        # Generate single style preview
        preview = generator.generate_preview(args.style, args.text)
        if preview:
            output_path = f"{args.output}/{args.style}_preview.png"
            os.makedirs(args.output, exist_ok=True)
            preview.save(output_path)
            print(f"Preview saved: {output_path}")
        else:
            print(f"Failed to generate preview for {args.style}")
    else:
        # Generate all style previews
        results = generator.generate_all_previews(args.text, args.output)
        print(f"\nGenerated {len(results)} previews in {args.output}/")

if __name__ == "__main__":
    main()
