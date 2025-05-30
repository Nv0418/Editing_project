#!/usr/bin/env python3
"""Test all 5 finalized caption styles with Game of Thrones audio"""

import os
import json
import movis as mv
from pathlib import Path
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

# Define the 5 finalized styles
FINALIZED_STYLES = [
    'simple_caption',
    'background_caption', 
    'glow_caption',
    'karaoke_style',
    'highlight_caption'
]

# Load transcription data
with open('other_root_files/parakeet_output.json', 'r') as f:
    transcript_data = json.load(f)

# Extract word timestamps
word_timestamps = transcript_data['word_timestamps']

# Video settings
resolution = (1080, 1920)
duration = 22.0  # Duration based on audio
fps = 30

# Output directory
output_dir = "output_test/temp_test"
os.makedirs(output_dir, exist_ok=True)

# Process each style
for style_name in FINALIZED_STYLES:
    print(f"\n{'='*60}")
    print(f"Processing style: {style_name}")
    print(f"{'='*60}")
    
    # Output file name
    output_file = f"{output_dir}/{style_name}.mp4"
    
    try:
        # Create composition
        composition = mv.layer.Composition(size=resolution, duration=duration)
        
        # Add black background
        background = mv.layer.Rectangle(
            size=resolution,
            color=(0, 0, 0),
            duration=duration
        )
        composition.add_layer(background)
        
        # Load audio
        audio_layer = mv.layer.Audio("other_root_files/got_script.mp3")
        composition.add_layer(audio_layer)
        
        # Load style
        style = StyleLoader.load_style_from_json(
            Path('subtitle_styles/config/subtitle_styles_v3.json'), 
            style_name
        )
        if not style:
            print(f"ERROR: Failed to load style {style_name}")
            continue
            
        # Add subtitle layer
        subtitle_layer = StyledSubtitleLayer(
            words=word_timestamps,
            style=style,
            resolution=resolution
        )
        composition.add_layer(subtitle_layer)
        
        # Render video
        print(f"Rendering {style_name} to {output_file}...")
        composition.write_video(output_file, codec='libx264', fps=fps, audio_codec='aac')
        print(f"✓ Successfully created {output_file}")
        
    except Exception as e:
        print(f"✗ ERROR processing {style_name}: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*60}")
print("All styles processed!")
print(f"Videos saved to: {output_dir}/")
print(f"{'='*60}")