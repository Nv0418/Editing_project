# Sgone Caption Style

## Overview
Center-positioned artistic style using The Sgone font with maximum 2 words displayed at a time.

## Features
- **Font**: The Sgone (unique artistic typeface)
- **Size**: 65px normal, 75px highlighted
- **Position**: Center screen (not bottom)
- **Transform**: Lowercase
- **Effect**: Size pulse on highlight
- **Words Per Window**: 2 (strictly enforced)
- **Outline**: 4px black outline

## Target Use Cases
- Artistic content
- Poetry and short phrases
- Creative storytelling
- Unique brand content
- Social media posts requiring distinctive typography

## Style Configuration
```json
{
  "effect_type": "outline",
  "font_family": "The Sgone.otf",
  "font_size": 65,
  "font_size_highlighted": 75,
  "text_positioning": "center",
  "text_transform": "lowercase",
  "words_per_window": 2,
  "highlight_method": "size_pulse"
}
```

## Special Features
- **Center positioning**: Unlike other styles that are bottom-positioned
- **2-word maximum**: Text cycles through pairs of words
- **Auto-scaling**: Font reduces if text exceeds 600px width
- **Artistic font**: The Sgone provides unique character

## Testing
Run the test script to generate a sample video with this style:
```bash
python3 test_sgone_caption.py
```