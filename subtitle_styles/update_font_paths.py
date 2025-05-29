
#!/usr/bin/env python3
"""
VinVideo Font Path Updater
Updates font paths in subtitle_styles_v2.json after new fonts are installed
"""

import json
import os
import sys

# Font mapping - which fonts to update for each style
FONT_UPDATES = {
    "simple_caption": None,  # Keep current Oswald-Heavy
    "background_caption": "RobotoCondensed-Bold.ttf",  # Already installed
    "karaoke_style": "Shrikhand-Regular.ttf",
    "glow_caption": "Impact.ttf",
    "highlight_caption": "Montserrat-Black.ttf",  # HORMOZI STYLE
    "dashing_caption": "Quicksand-Bold.ttf",
    "newscore": None,  # Keep current Oswald-Bold
    "popling_caption": "Fredoka-Bold.ttf",
    "whistle_caption": "Nunito-Regular.ttf",
    "karaoke_caption": "BebasNeue-Regular.ttf",
    "tilted_caption": "LobsterTwo-Italic.ttf"
}

def update_font_paths():
    """Update font paths in the configuration file"""
    config_path = "/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v2.json"
    
    # Load current configuration
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # Update font paths
    updated_count = 0
    for style_name, new_font in FONT_UPDATES.items():
        if new_font and style_name in config:
            old_font = config[style_name]['typography']['font_family']
            new_path = f"/Users/naman/Library/Fonts/{new_font}"
            
            # Check if font exists
            if os.path.exists(new_path):
                config[style_name]['typography']['font_family'] = new_path
                print(f"✅ Updated {style_name}: {new_font}")
                updated_count += 1
            else:
                print(f"❌ Font not found: {new_font} (for {style_name})")
    
    # Save updated configuration
    if updated_count > 0:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"\n✨ Updated {updated_count} font paths successfully!")
    else:
        print("\n⚠️  No fonts were updated. Please install the fonts first.")

if __name__ == "__main__":
    print("🎨 VinVideo Font Path Updater")
    print("=" * 40)
    update_font_paths()
