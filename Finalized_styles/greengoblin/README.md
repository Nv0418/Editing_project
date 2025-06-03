# Green Goblin Caption Style

## Overview
Clean text style without glow effects using Manrope ExtraBold font with green highlighting and auto-scaling.

## Features
- **Font**: Manrope ExtraBold (800 weight)
- **Size**: 108px (both normal and highlighted)
- **Colors**: White → Bright Green transition
- **Effect**: Dual glow without actual glow (clean appearance)
- **Auto-scaling**: 1.1x scale on highlight
- **Outline**: 3px black outline

## Target Use Cases
- Professional presentations
- Clean karaoke-style content
- Business and educational videos
- Content requiring clear, readable text

## Style Configuration
```json
{
  "effect_type": "dual_glow",
  "font_family": "Manrope-ExtraBold.ttf",
  "font_size": 108,
  "text_transform": "uppercase",
  "colors": {
    "text_normal": [255, 255, 255],
    "text_highlighted": [57, 255, 20]
  },
  "highlight_method": "dual_glow_with_scale"
}
```

## Testing
Run the test script to generate a sample video with this style:
```bash
python3 test_greengoblin.py
```