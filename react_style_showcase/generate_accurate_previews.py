#!/usr/bin/env python3
"""
Accurate Preview Generator
Uses the actual subtitle rendering system to create EXACT previews
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

import json
from PIL import Image
import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import SubtitleLayer

# Preview configuration
PREVIEW_WIDTH = 400
PREVIEW_HEIGHT = 220
PREVIEW_FPS = 30
PREVIEW_DURATION = 0.1  # Single frame

# Sample text with timing
PREVIEW_TEXT = "hey hello"
PREVIEW_WORDS = [
    {"word": "hey", "start": 0.0, "end": 0.5},
    {"word": "hello", "start": 0.5, "end": 1.0}
]

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

def create_accurate_preview(style_id, output_path):
    """Create preview using the actual video rendering pipeline"""
    try:
        print(f"Creating preview for {style_id}...")
        
        # Create a mini video composition
        scene = mv.Scene(size=(PREVIEW_WIDTH, PREVIEW_HEIGHT), duration=PREVIEW_DURATION)
        
        # Add black background
        bg = mv.layer.Solid(size=(PREVIEW_WIDTH, PREVIEW_HEIGHT), color=(0, 0, 0))
        scene.add_layer(bg)
        
        # Load the style
        loader = StyleLoader()
        style_instance = loader.load_style(style_id)
        
        if not style_instance:
            print(f"Failed to load style: {style_id}")
            return False
        
        # Create subtitle layer with our preview text
        # Adjust timing so second word is highlighted
        subtitle_layer = SubtitleLayer(
            style=style_instance,
            size=(PREVIEW_WIDTH, PREVIEW_HEIGHT),
            words=PREVIEW_WORDS,
            duration=PREVIEW_DURATION
        )
        
        # Position at center for sgone_caption, bottom for others
        if style_id == 'sgone_caption':
            subtitle_layer.position = (PREVIEW_WIDTH // 2, PREVIEW_HEIGHT // 2)
        else:
            subtitle_layer.position = (PREVIEW_WIDTH // 2, int(PREVIEW_HEIGHT * 0.8))
        
        scene.add_layer(subtitle_layer)
        
        # Render a single frame at 0.05 seconds (when "hello" should be highlighted)
        frame = scene[0.05]
        
        # Convert to PIL Image and save
        pil_image = Image.fromarray(frame)
        
        # Add style name overlay
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(pil_image)
        
        # Get style name from config
        style_config = style_instance.config
        style_name = style_config.get('name', style_id.upper())
        
        # Load font for style name
        try:
            name_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        except:
            name_font = ImageFont.load_default()
        
        # Add semi-transparent background for name
        overlay = Image.new('RGBA', (PREVIEW_WIDTH, PREVIEW_HEIGHT), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        name_y = PREVIEW_HEIGHT - 25
        overlay_draw.rectangle([0, PREVIEW_HEIGHT - 40, PREVIEW_WIDTH, PREVIEW_HEIGHT], 
                              fill=(0, 0, 0, 180))
        
        # Composite overlay
        pil_image = Image.alpha_composite(pil_image.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(pil_image)
        
        # Draw style name
        draw.text((PREVIEW_WIDTH // 2, name_y), style_name, 
                 font=name_font, fill=(255, 255, 255), anchor="mm")
        
        # Save
        pil_image.save(output_path, quality=95)
        print(f"✓ Saved: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error creating preview for {style_id}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Generate all previews using actual rendering pipeline"""
    output_dir = Path(__file__).parent / "subtitle_preview_app" / "public" / "style_previews"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating ACCURATE previews using video rendering pipeline...")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    for style_id in FINALIZED_STYLES:
        output_path = output_dir / f"{style_id}.png"
        if create_accurate_preview(style_id, output_path):
            success_count += 1
    
    print(f"\nGenerated {success_count}/{len(FINALIZED_STYLES)} previews successfully!")

if __name__ == "__main__":
    main()