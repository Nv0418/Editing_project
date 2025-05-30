# Word-by-Word Effects Implementation Guide

## Overview
This document explains how word-by-word subtitle effects are implemented in the VinVideo project. There are currently two main types of word-by-word effects that highlight individual words as they are spoken.

## Effect Types

### 1. Karaoke Style (Word Color Change)
Changes the color of individual words as they are spoken.

#### Configuration
```json
"effect_type": "dual_glow"  // or "text_shadow"
```

#### Implementation Files
- **Main Effect File**: `subtitle_styles/effects/text_effects.py`
- **Key Methods**:
  - `create_two_tone_glow_effect()` - For karaoke style (white → yellow)
  - `create_text_shadow_glow_effect()` - For glow caption (white → green with shadows)

#### How It Works
1. Takes a list of words and `highlighted_word_index` parameter
2. Renders each word separately with different colors:
   - **Normal words**: White text (with optional white glow)
   - **Highlighted words**: Yellow/Green text (with matching glow)
3. Words are positioned correctly to form complete text
4. No background changes - only text color changes

#### Example Styles Using This Effect
- **karaoke_style**: Uses `dual_glow` with white-to-yellow color change
- **glow_caption**: Uses `text_shadow` with white-to-green color change

### 2. Highlight Caption Style (Word Background)
Adds a colored background box behind individual words as they are spoken.

#### Configuration
```json
"effect_type": "word_highlight"
```

#### Implementation Files
- **Main Effect File**: `subtitle_styles/effects/word_highlight_effects.py`
- **Key Method**: `create_word_background_highlight_effect()`

#### How It Works
1. Takes a list of words and `highlighted_word_index` parameter
2. Only the highlighted word gets a background:
   - **Normal words**: No background (transparent)
   - **Highlighted word**: Purple background box (customizable color)
3. Backgrounds are drawn first, then text on top
4. Text color remains consistent (white) for all words

#### Customizable Parameters
- `background_padding`: Controls padding around text (e.g., `{"x": 15, "y": 10}`)
- `corner_radius`: Rounded corners for background boxes (e.g., `20`)
- `highlight_bg_color`: RGB color for background (e.g., `[126, 87, 194]` for purple)

#### Example Style Using This Effect
- **highlight_caption**: Purple background on active words, mazzard font, lowercase text

### 3. Deep Diver Style (Full Background + Word Color)
Shows all text on a grey background with the active word in black and inactive words in grey.

#### Configuration
```json
"effect_type": "deep_diver"
```

#### Implementation Files
- **Main Effect File**: `subtitle_styles/effects/word_highlight_effects.py`
- **Key Method**: `create_deep_diver_effect()`

#### How It Works
1. Renders all words on a single grey background box
2. Colors each word based on its state:
   - **Active word**: Black text
   - **Inactive words**: Grey text
3. Background encompasses all text with padding
4. Maintains consistent positioning for all words

#### Customizable Parameters
- `background_padding`: Padding around entire text block
- `corner_radius`: Rounded corners for background
- `active_text_color`: Color for currently spoken word (default: black)
- `inactive_text_color`: Color for other words (default: grey)
- `background_color`: Color for the background box (default: light grey)

#### Example Style Using This Effect
- **deep_diver**: Grey background with black/grey text, Publica Sans Round font

## Rendering Pipeline

### 1. JSON Configuration (`subtitle_styles_v3.json`)
Defines style parameters including:
- `effect_type`: Determines which rendering method to use
- Typography settings (font, size, colors)
- Effect-specific parameters

### 2. Style Loader (`json_style_loader.py`)
Routes to appropriate rendering method based on `effect_type`:
```python
if effect_type == 'dual_glow':
    return self._create_dual_glow_text()
elif effect_type == 'text_shadow':
    return self._create_text_shadow_text()
elif effect_type == 'word_highlight':
    return self._create_word_highlight_text()
```

### 3. Effect Rendering
- **For color change effects** → `text_effects.py`
- **For background highlight effects** → `word_highlight_effects.py`

### 4. Timing Integration (`movis_layer.py`)
- Determines which word is currently active based on timestamps
- Passes `highlighted_word_index` to the effect renderer
- Handles word grouping (default: 3 words per window)

## Key Implementation Details

### Common Parameters
- `highlighted_word_index`: Integer indicating which word should be highlighted (-1 for none)
- `words`: List of words to render
- `font_path`, `font_size`: Typography settings
- `image_size`: Canvas dimensions (typically 1080x200 for subtitle area)

### Word Timing
Each word has:
- `start`: Timestamp when word begins
- `end`: Timestamp when word ends
- Words are highlighted when `current_time` is between `start` and `end`

### Auto-scaling
Both effect types include automatic font scaling to ensure text fits within safe zones:
- If text width exceeds 90% of canvas width
- Font size is automatically reduced
- Maintains readability while fitting constraints

## Adding New Word-by-Word Effects

To add a new word-by-word effect:

1. **Choose an effect type name** (e.g., `"word_outline"`)

2. **Create rendering method** in appropriate effects file:
   - For text-based effects → Add to `text_effects.py`
   - For background-based effects → Add to `word_highlight_effects.py`

3. **Add routing** in `json_style_loader.py`:
   ```python
   elif effect_type == 'your_new_effect':
       return self._create_your_effect_text()
   ```

4. **Define JSON configuration** in `subtitle_styles_v3.json`

## Current Implementations Summary

| Effect Type | What Changes | Implementation File | Example Style |
|-------------|--------------|-------------------|---------------|
| `dual_glow` | Word color (two-tone) | `text_effects.py` | karaoke_style |
| `text_shadow` | Word color + shadow | `text_effects.py` | glow_caption |
| `word_highlight` | Word background | `word_highlight_effects.py` | highlight_caption |
| `deep_diver` | Full background + word color | `word_highlight_effects.py` | deep_diver |

## Notes
- All word-by-word effects maintain the same text positioning
- Effects are frame-based and update in real-time based on audio timestamps
- The system supports customization through JSON configuration without code changes