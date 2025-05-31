# Deep Diver Style

## Overview
Deep thoughts style with grey background and contrasting text. Perfect for philosophical and contemplative content.

## Style Specifications
- **Font**: Publica Sans Round Bold, 70px
- **Colors**: Black active text, gray inactive text (#505050), light gray background (#8C8C8C)
- **Transform**: Lowercase
- **Effect Type**: `deep_diver`
- **Background**: Single gray background containing all text

## Features
- ✅ Contrasting active/inactive text colors
- ✅ Contemplative aesthetic
- ✅ Single background for all text
- ✅ Perfect text centering
- ✅ Multi-line support

## Color System
- **Active Text**: Black (#000000) for currently spoken word
- **Inactive Text**: Medium Gray (#505050) for other words
- **Background**: Light Gray (#8C8C8C) with 25px rounded corners

## Technical Notes
- **Manual Centering Fix**: Applied -40px horizontal offset to correct rendering alignment
- **Background Sizing**: Optimized padding (15px x, 8px y) for tight fit
- **Font Metrics**: Uses ascent/descent for perfect vertical alignment

## Files
- `DEEP_DIVER_FIX_README.md` - Details about centering fix
- `fixed_deep_diver_effect.py` - Implementation with manual offset
- `word_highlight_effects_manual_fix.py` - Corrected manual fix implementation
- `generate_deep_diver_video.py` - Video generation script

## Use Cases
- Philosophical content
- Educational videos
- Contemplative discussions
- Deep thought presentations

## Test Script
Run `python3 generate_deep_diver_video.py` to generate a test video with this style.

## Configuration
Located in `subtitle_styles_v3.json` under `"deep_diver"` key.