#!/usr/bin/env python3
"""
React Style Preview Generator
Generates preview images for the React app matching Aicut's design
Shows actual rendered text with style name overlaid
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

from PIL import Image, ImageDraw, ImageFont
import json

# Preview configuration
PREVIEW_SIZE = (400, 220)  # Slightly larger for better fit
PREVIEW_TEXT = "hey hello"  # Sample text to show
BACKGROUND_COLOR = (0, 0, 0)  # Black background

# 9 finalized styles
FINALIZED_STYLES = [
    'simple_caption',
    'background_caption', 
    'glow_caption',
    'karaoke_style',
    'highlight_caption',
    'deep_diver',
    'popling_caption',
    'greengoblin',
    'sgone_caption'
]

def load_styles_config():
    """Load styles configuration from JSON"""
    config_path = Path(__file__).parent.parent / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def create_style_preview(style_id, output_path):
    """Create a preview image for a specific style"""
    try:
        # Create a black background
        preview = Image.new('RGB', PREVIEW_SIZE, BACKGROUND_COLOR)
        draw = ImageDraw.Draw(preview)
        
        # Load all styles
        all_styles = load_styles_config()
        
        if style_id not in all_styles:
            print(f"Style not found: {style_id}")
            return False
        
        # Get style configuration
        config = all_styles[style_id]
        typography = config.get('typography', {})
        effect_type = config.get('effect_type', '')
        effect_params = config.get('effect_parameters', {})
        
        # Apply text transform
        display_text = PREVIEW_TEXT
        if typography.get('text_transform') == 'uppercase':
            display_text = display_text.upper()
        elif typography.get('text_transform') == 'lowercase':
            display_text = display_text.lower()
        
        # For sgone_caption, limit to 2 words
        if style_id == 'sgone_caption':
            words = display_text.split()[:2]
            display_text = ' '.join(words)
        
        # Get font settings - scale down for preview
        font_path = typography.get('font_family', '')
        base_font_size = typography.get('font_size', 72)
        # Different scaling for different styles
        if style_id == 'background_caption':
            font_size = int(base_font_size * 0.4)  # Smaller for background caption
        else:
            font_size = int(base_font_size * 0.5)  # Scale to 50% for preview
        
        # Try to load the font
        try:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # Try project_fonts directory
                font_name = os.path.basename(font_path)
                project_font_path = f"/Users/naman/Desktop/movie_py/project_fonts/{font_name}"
                if os.path.exists(project_font_path):
                    font = ImageFont.truetype(project_font_path, font_size)
                else:
                    font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Center position
        text_x = PREVIEW_SIZE[0] // 2
        text_y = PREVIEW_SIZE[1] // 2
        
        # Render based on effect type
        if effect_type == 'outline':
            # Simple outline effect
            colors = typography.get('colors', {})
            text_color = tuple(colors.get('text', [255, 255, 255]))
            outline_color = tuple(colors.get('outline', [0, 0, 0]))
            outline_width = effect_params.get('outline_width', 4)
            
            # Draw outline
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((text_x + dx, text_y + dy), display_text, 
                                font=font, fill=outline_color, anchor="mm")
            
            # Draw text
            draw.text((text_x, text_y), display_text, 
                     font=font, fill=text_color, anchor="mm")
        
        elif effect_type == 'background':
            # Background box effect
            colors = typography.get('colors', {})
            text_color = tuple(colors.get('text', [255, 255, 255]))
            bg_color = tuple(colors.get('background', [0, 51, 102]))
            padding = effect_params.get('background_padding', {'x': 40, 'y': 20})
            
            # Scale padding
            pad_x = int(padding.get('x', 40) * 0.6)
            pad_y = int(padding.get('y', 20) * 0.6)
            
            # Get text bbox
            bbox = draw.textbbox((text_x, text_y), display_text, font=font, anchor="mm")
            
            # Draw background
            bg_bbox = [bbox[0] - pad_x, bbox[1] - pad_y, 
                      bbox[2] + pad_x, bbox[3] + pad_y]
            draw.rectangle(bg_bbox, fill=bg_color)
            
            # Draw text
            draw.text((text_x, text_y), display_text, 
                     font=font, fill=text_color, anchor="mm")
        
        elif effect_type == 'text_shadow' or effect_type == 'glow':
            # Glow effect - render words separately with different colors
            colors = typography.get('colors', {})
            text_normal = tuple(colors.get('text_normal', [255, 255, 255]))
            text_highlighted = tuple(colors.get('text_highlighted', [57, 255, 20]))
            
            words = display_text.split()
            # Calculate total width to center
            test_text = " ".join(words)
            bbox = draw.textbbox((0, 0), test_text, font=font)
            total_width = bbox[2] - bbox[0]
            current_x = text_x - total_width // 2
            
            for i, word in enumerate(words):
                # Second word gets highlighted color and glow
                if i == 1:
                    # Draw glow effect
                    for radius in range(15, 0, -1):
                        alpha = int(150 * (1 - radius/15))
                        for dx in range(-radius//3, radius//3 + 1):
                            for dy in range(-radius//3, radius//3 + 1):
                                if dx*dx + dy*dy <= radius*radius/9:
                                    draw.text((current_x + dx, text_y + dy), word,
                                            font=font, fill=text_highlighted, anchor="lm")
                    # Draw the word
                    draw.text((current_x, text_y), word,
                             font=font, fill=text_highlighted, anchor="lm")
                else:
                    # Normal word
                    draw.text((current_x, text_y), word,
                             font=font, fill=text_normal, anchor="lm")
                
                # Move to next word position
                word_width = draw.textlength(word, font=font)
                current_x += word_width
                if i < len(words) - 1:
                    current_x += draw.textlength(" ", font=font)
        
        elif effect_type == 'underline':
            # Underline effect (popling)
            colors = typography.get('colors', {})
            text_color = tuple(colors.get('text', [255, 255, 255]))
            outline_color = tuple(colors.get('outline', [0, 0, 0]))
            underline_color = tuple(colors.get('underline', [147, 51, 234]))
            
            # Draw text with outline
            outline_width = effect_params.get('outline_width', 5)
            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((text_x + dx, text_y + dy), display_text,
                                font=font, fill=outline_color, anchor="mm")
            
            draw.text((text_x, text_y), display_text,
                     font=font, fill=text_color, anchor="mm")
            
            # Draw underline on second word
            words = display_text.split()
            if len(words) >= 2:
                # Get text bbox to find exact bottom
                full_bbox = draw.textbbox((text_x, text_y), display_text, font=font, anchor="mm")
                text_bottom = full_bbox[3]
                
                # Measure first word + space
                first_word_width = draw.textlength(words[0] + " ", font=font)
                second_word_width = draw.textlength(words[1], font=font)
                
                # Calculate underline position - touching the text bottom
                underline_x = text_x - draw.textlength(display_text, font=font) / 2 + first_word_width
                underline_y = text_bottom - 3  # Slight overlap to ensure it touches
                underline_height = 8
                
                # Draw underline
                draw.rectangle([underline_x, underline_y, 
                              underline_x + second_word_width, underline_y + underline_height],
                              fill=underline_color)
        
        elif effect_type == 'word_highlight':
            # Word highlight (hormozi style)
            colors = typography.get('colors', {})
            text_color = tuple(colors.get('text', [255, 255, 255]))
            highlight_bg = tuple(colors.get('highlight_bg_color', [126, 87, 194]))
            
            words = display_text.split()
            current_x = text_x - draw.textlength(display_text, font=font) / 2
            
            for i, word in enumerate(words):
                if i == 1:  # Highlight second word
                    # Draw background
                    bbox = draw.textbbox((current_x, text_y), word, font=font, anchor="lm")
                    padding = 8
                    draw.rectangle([bbox[0] - padding, bbox[1] - padding,
                                  bbox[2] + padding, bbox[3] + padding],
                                  fill=highlight_bg)
                
                # Draw word
                draw.text((current_x, text_y), word, font=font, fill=text_color, anchor="lm")
                current_x += draw.textlength(word + " ", font=font)
        
        elif effect_type == 'deep_diver':
            # Deep diver effect
            colors = typography.get('colors', {})
            active_color = tuple(colors.get('active_text', [0, 0, 0]))
            inactive_color = tuple(colors.get('inactive_text', [80, 80, 80]))
            bg_color = tuple(colors.get('background', [140, 140, 140]))
            
            # Draw background for all text
            bbox = draw.textbbox((text_x, text_y), display_text, font=font, anchor="mm")
            padding = 10
            draw.rectangle([bbox[0] - padding, bbox[1] - padding,
                          bbox[2] + padding, bbox[3] + padding],
                          fill=bg_color)
            
            # Draw words with different colors
            words = display_text.split()
            current_x = text_x - draw.textlength(display_text, font=font) / 2
            
            for i, word in enumerate(words):
                color = active_color if i == 1 else inactive_color
                draw.text((current_x, text_y), word, font=font, fill=color, anchor="lm")
                current_x += draw.textlength(word + " ", font=font)
        
        elif effect_type == 'dual_glow':
            # Dual glow (karaoke/green goblin)
            colors = typography.get('colors', {})
            text_normal = tuple(colors.get('text_normal', [255, 255, 255]))
            text_highlighted = tuple(colors.get('text_highlighted', [255, 255, 0]))
            
            words = display_text.split()
            current_x = text_x - draw.textlength(display_text, font=font) / 2
            
            for i, word in enumerate(words):
                color = text_highlighted if i == 1 else text_normal
                
                # Add outline for green goblin
                if style_id == 'greengoblin':
                    outline_width = 3
                    for dx in range(-outline_width, outline_width + 1):
                        for dy in range(-outline_width, outline_width + 1):
                            if dx != 0 or dy != 0:
                                draw.text((current_x + dx, text_y + dy), word,
                                        font=font, fill=(0, 0, 0), anchor="lm")
                
                draw.text((current_x, text_y), word, font=font, fill=color, anchor="lm")
                current_x += draw.textlength(word + " ", font=font)
        
        else:
            # Default rendering
            colors = typography.get('colors', {})
            text_color = tuple(colors.get('text', [255, 255, 255]))
            draw.text((text_x, text_y), display_text,
                     font=font, fill=text_color, anchor="mm")
        
        # Add style name overlay at bottom
        style_name = config.get('name', style_id.upper())
        name_font_size = 16
        try:
            name_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", name_font_size)
        except:
            name_font = ImageFont.load_default()
        
        # Draw style name with background
        name_y = PREVIEW_SIZE[1] - 25
        name_bbox = draw.textbbox((text_x, name_y), style_name, font=name_font, anchor="mm")
        
        # Semi-transparent background for name
        overlay = Image.new('RGBA', PREVIEW_SIZE, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([0, name_bbox[1] - 5, PREVIEW_SIZE[0], PREVIEW_SIZE[1]], 
                              fill=(0, 0, 0, 180))
        preview = Image.alpha_composite(preview.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(preview)
        
        # Draw style name
        draw.text((text_x, name_y), style_name, font=name_font, fill=(255, 255, 255), anchor="mm")
        
        # Save preview
        preview.save(output_path, quality=95)
        print(f"Generated preview: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error generating preview for {style_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate all style previews"""
    # Create output directory in React app
    output_dir = Path(__file__).parent / "subtitle_preview_app" / "public" / "style_previews"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating previews for {len(FINALIZED_STYLES)} styles...")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    for style_id in FINALIZED_STYLES:
        output_path = output_dir / f"{style_id}.png"
        if create_style_preview(style_id, output_path):
            success_count += 1
    
    print(f"\nGenerated {success_count}/{len(FINALIZED_STYLES)} previews successfully!")
    print(f"Previews saved to: {output_dir}")

if __name__ == "__main__":
    main()