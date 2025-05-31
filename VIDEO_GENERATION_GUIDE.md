# Video Generation Guide for Subtitle Styles

## Overview
This guide explains how to generate test videos with different subtitle styles using the VinVideo subtitle system.

## Required Files
To generate a video with subtitles, you need:
1. **Audio file** (e.g., `got_script.mp3`)
2. **Parakeet transcription JSON** with word timestamps
3. **Style configuration** (`subtitle_styles_v3.json`)

## Standard Test Files Location
- **Audio**: `/Users/naman/Desktop/movie_py/other_root_files/got_script.mp3`
- **Transcription**: `/Users/naman/Desktop/movie_py/other_root_files/parakeet_output.json`
- **Styles Config**: `/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json`

## Video Generation Methods

### Method 1: Using test_v3_styles.py (All Styles)
```bash
# Test all 9 finalized styles
python3 test_v3_styles.py

# Test specific style
python3 test_v3_styles.py --style deep_diver
```

### Method 2: Using test_json_styled_video.py (Single Style)
```bash
# Test with default text
python3 test_json_styled_video.py --style simple_caption

# Test with custom text
python3 test_json_styled_video.py --style simple_caption --text "Custom text here"
```

### Method 3: Custom Script (Recommended for Testing)
Create a script like `30may_test/generate_deep_diver_video.py`:

```python
#!/usr/bin/env python3
import os
import sys
import json

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import movis as mv
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

def load_parakeet_data(file_path):
    """Load word timestamps from Parakeet JSON output."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['word_timestamps']

def create_styled_video(style_name="deep_diver", output_name=None):
    """Create a video with specified subtitle style."""
    
    # Configuration
    resolution = (1080, 1920)  # Instagram 9:16 format
    fps = 30
    
    # File paths
    project_root = os.path.dirname(os.path.dirname(__file__))
    parakeet_file = os.path.join(project_root, 'other_root_files', 'parakeet_output.json')
    audio_file = os.path.join(project_root, 'other_root_files', 'got_script.mp3')
    json_style_file = os.path.join(project_root, 'subtitle_styles', 'config', 'subtitle_styles_v3.json')
    
    # Output file
    if output_name is None:
        output_name = f"{style_name}_test.mp4"
    output_file = os.path.join(project_root, '30may_test', output_name)
    
    # Load data
    word_timestamps = load_parakeet_data(parakeet_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    duration = audio_layer.duration
    
    # Load style
    style = StyleLoader.load_style_from_json(json_style_file, style_name)
    
    # Create composition
    scene = mv.layer.Composition(size=resolution, duration=duration)
    
    # Add black background
    background = mv.layer.Rectangle(
        size=resolution,
        duration=duration,
        color=(0, 0, 0)
    )
    scene.add_layer(background, name='background')
    
    # Create subtitle layer
    subtitle_layer = StyledSubtitleLayer(
        words=word_timestamps,
        style=style,
        resolution=resolution,
        position="bottom",  # or "center", "top"
        safe_zones=True
    )
    
    # Add layers
    scene.add_layer(subtitle_layer, name='subtitles', offset=0.0)
    scene.add_layer(audio_layer, name='audio')
    
    # Export video
    print(f"Generating {style_name} style video...")
    print(f"Output: {output_file}")
    
    scene.write_video(
        output_file,
        fps=fps,
        audio_codec='aac'
    )
    
    print(f"Video successfully generated at: {output_file}")

if __name__ == "__main__":
    # Example: Generate Deep Diver style video
    create_styled_video("deep_diver", "deep_diver_got_test.mp4")
```

## Available Subtitle Styles (All 9 Finalized)
1. **simple_caption** - Educational content with size-pulse effect
2. **background_caption** - News style with dark blue background
3. **glow_caption** - Gaming/tech with green glow effects
4. **karaoke_style** - Music content with yellow word highlights
5. **highlight_caption** - Motivational with purple word backgrounds
6. **deep_diver** - Contemplative with gray background
7. **popling_caption** - Elegant with pink text and underline effect
8. **greengoblin** - Clean karaoke without glow effects
9. **sgone_caption** - Unique 2-word display with stylized font

## Key Parameters

### Position Options
- `"bottom"` - Bottom of screen (default for most styles)
- `"center"` - Center of screen
- `"top"` - Top of screen

### Safe Zones
- `True` - Respects Instagram/TikTok safe areas (recommended)
- `False` - Uses full screen

### Resolution
- `(1080, 1920)` - Standard 9:16 format for Instagram/TikTok/YouTube Shorts
- `(1920, 1080)` - Standard 16:9 format (not commonly used for shorts)

## Common Issues and Solutions

### Issue: Font not found
**Solution**: Check font paths in `subtitle_styles_v3.json` and ensure fonts are installed

### Issue: Audio file not found
**Solution**: Verify path to `got_script.mp3` in `other_root_files/`

### Issue: Deep Diver appears off-center
**Solution**: Adjust `MANUAL_OFFSET` in `word_highlight_effects_manual_fix.py`

## Testing Workflow
1. Choose a style from the 9 finalized options
2. Create a test script using the template above
3. Run the script to generate video
4. Review output in the specified directory
5. Adjust parameters if needed and regenerate

## Output Locations
- **test_v3_styles.py**: Creates timestamped folder in `output_test/`
- **Custom scripts**: Output to specified location (e.g., `30may_test/`)
- **Default naming**: `{style_name}.mp4` or custom name