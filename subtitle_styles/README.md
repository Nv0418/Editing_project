# Subtitle Style System

A dynamic subtitle styling system for VinVideo that provides Aicut-inspired styles with JSON configuration.

## Overview

This system allows you to create professional-looking subtitles with various visual effects, all configured through JSON files. It integrates seamlessly with Movis for video generation and supports Nvidia Parakeet word-level timing.

## Features

- **JSON Configuration**: Define styles in JSON without touching code
- **Multiple Effect Types**: Outline, background, glow effects
- **Instagram Safe Zones**: Automatic text positioning within safe areas
- **Word-by-Word Timing**: Precise synchronization with Parakeet transcriptions
- **Backward Compatible**: Works with existing subtitles_style.json formats

## Available Styles

### 1. Simple Caption
- Clean white text with black outline
- Maximum readability
- Effect type: `outline`

### 2. Background Caption  
- White text on cyan background box
- High contrast for emphasis
- Effect type: `background`

### 3. Glow Caption
- White text with animated pink/red glow
- Eye-catching neon effect
- Effect type: `glow`

## Usage

### Basic Usage

```python
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

# Load style from JSON
style = StyleLoader.load_style_from_json(
    'subtitle_styles/config/subtitle_styles_v2.json',
    'simple_caption'
)

# Create subtitle layer
subtitle_layer = StyledSubtitleLayer(
    words=words,  # Parakeet word timings
    style=style,
    resolution=(1080, 1920),
    position='bottom',
    safe_zones=True
)

# Add to composition
composition.add_layer(subtitle_layer)
```

### Command Line

```bash
# Generate video with specific style
python test_json_styled_video.py --style simple_caption

# List available styles
python test_json_styled_video.py --list

# Test all styles
python test_json_styled_video.py --all
```

## JSON Style Configuration

### Style Structure

```json
{
  "style_id": {
    "name": "Display Name",
    "description": "Style description",
    "effect_type": "outline|background|glow",
    "format": {
      "resolution": [1080, 1920],
      "aspect_ratio": "9:16"
    },
    "layout": {
      "text_positioning": "bottom",
      "safe_zones": true,
      "safe_margins": {
        "horizontal": 100,
        "top": 220,
        "bottom": 450
      }
    },
    "typography": {
      "font_family": "Arial Black",
      "font_size": 72,
      "colors": {
        "text": [255, 255, 255],
        "outline": [0, 0, 0]
      }
    },
    "effect_parameters": {
      // Effect-specific parameters
    }
  }
}
```

### Effect Parameters

#### Outline Effect
```json
"effect_parameters": {
  "outline_width": 4
}
```

#### Background Effect
```json
"effect_parameters": {
  "background_padding": {"x": 40, "y": 20},
  "background_opacity": 1.0,
  "rounded_corners": 0,
  "highlight_brightness_boost": 30
}
```

#### Glow Effect
```json
"effect_parameters": {
  "glow_radius": 20,
  "glow_intensity": 0.9,
  "pulse": {
    "enabled": true,
    "frequency": 0.5,
    "min_intensity": 0.6,
    "max_intensity": 1.0
  }
}
```

## Creating Custom Styles

1. Copy an existing style in `subtitle_styles_v2.json`
2. Modify the parameters:
   - Change `effect_type` to choose base effect
   - Adjust `typography` for fonts and colors
   - Tune `effect_parameters` for visual appearance
3. Test with: `python test_json_styled_video.py --style your_style_id`

## Instagram Safe Zones

The system automatically respects Instagram UI elements:
- **Top margin**: 220px (for status bar)
- **Bottom margin**: 450px (for UI controls)
- **Side margins**: 100px (for better visibility)

Text that exceeds safe width is automatically scaled down to fit.

## File Structure

```
subtitle_styles/
├── config/
│   └── subtitle_styles_v2.json    # Style definitions
├── core/
│   ├── base_style.py             # Base style class
│   ├── json_style_loader.py      # JSON configuration loader
│   └── movis_layer.py            # Movis integration layer
├── effects/
│   └── text_effects.py           # Visual effect implementations
└── styles/                       # Legacy Python-based styles
```

## Backward Compatibility

The system supports both new and old JSON formats:
- New format uses `colors.text` and `colors.outline`
- Old format uses `colors.normal` and `colors.highlighted`
- Both formats work seamlessly

## Performance

- Renders at 30fps by default
- ~60-70 frames per second processing speed
- Automatic text scaling prevents render slowdowns
- Parallel processing ready for future optimizations