# Popling Caption Style

## Overview
Playful, creative, artistic content with hand-drawn style purple underlines that appear under highlighted words.

## Style Specifications
- **Font**: Bicyclette Black, 100px
- **Colors**: White text, black outline (5px), purple underline (#9333EA)
- **Transform**: Lowercase
- **Effect Type**: `underline`
- **Underline**: Hand-drawn style with wave effect (16px thickness)

## Features
- ✅ Hand-drawn style underlines
- ✅ Wave animation effect
- ✅ Bold, artistic typography
- ✅ Playful aesthetic
- ✅ Dynamic underline highlighting

## Underline Configuration
- **Height**: 16px (doubled for boldness)
- **Offset**: 10px from text baseline
- **Style**: Hand-drawn with slight wave effect
- **Color**: Purple (#9333EA)
- **Animation**: Appears under highlighted word with wave pattern

## Technical Implementation
- **Wave Effect**: Uses sine wave function for natural hand-drawn appearance
- **Line Segments**: 20 points creating smooth curve
- **Dynamic Positioning**: Calculates exact word boundaries for precise placement

## Files
- `test_popling_caption.py` - Basic test script
- `generate_popling_video.py` - Full video generation script

## Use Cases
- Creative content
- Artistic videos
- Playful presentations
- Design-focused content

## Test Script
Run `python3 generate_popling_video.py` to generate a test video with this style.

## Configuration
Located in `subtitle_styles_v3.json` under `"popling_caption"` key.