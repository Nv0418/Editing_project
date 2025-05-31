# Word-by-Word Effects Implementation Guide

## Overview
This document explains how word-by-word subtitle effects are implemented in the VinVideo project using the Movis library. The system supports 9 finalized subtitle styles, each with unique visual characteristics and word-by-word highlighting behaviors. All styles are optimized for 9:16 aspect ratio (1080x1920) and designed for Instagram, YouTube Shorts, and TikTok content.

## Architecture Overview

### Core Components
1. **Configuration System**: JSON-based style definitions (`subtitle_styles_v3.json`)
2. **Style Loader**: Routes effects to appropriate rendering methods (`json_style_loader.py`)
3. **Effect Engines**: Specialized rendering for different effect types
   - `text_effects.py` - Color-based effects (karaoke, glow)
   - `word_highlight_effects.py` - Background-based effects (highlight, deep_diver)
4. **Movis Integration**: Video layer integration (`movis_layer.py`)

### Rendering Pipeline
```
JSON Config → Style Loader → Effect Engine → Movis Layer → Final Video
```

## Finalized Subtitle Styles

### 1. Simple Caption
**Purpose**: Clean, educational text for tutorials and how-to content

#### Typography
- **Font**: Oswald Heavy (`/Users/naman/Library/Fonts/Oswald-Heavy.ttf`)
- **Size**: 72px (normal), 80px (highlighted)
- **Transform**: Uppercase
- **Alignment**: Center
- **Weight**: Heavy

#### Colors
- **Text**: White `[255, 255, 255]`
- **Outline**: Black `[0, 0, 0]`
- **Outline Width**: 4px

#### Highlighting Behavior
- **Effect Type**: `outline`
- **Highlight Method**: `size_pulse`
- **Animation**: Text size increases from 72px to 80px when highlighted
- **Transition Duration**: 0.2 seconds
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_outline_text()` method in `json_style_loader.py`
- Calls `TextEffects.create_outline_effect()` from `text_effects.py`
- Creates crisp white text with black stroke border
- Size-based highlighting draws attention to active words
- Auto-scales if text width exceeds safe zone (880px max width)

---

### 2. Background Caption
**Purpose**: Professional news-style text with dark background

#### Typography
- **Font**: Bicyclette Black (`/Users/naman/Library/Fonts/Bicyclette-Black.ttf`)
- **Size**: 140px (both normal and highlighted)
- **Transform**: Uppercase
- **Alignment**: Center
- **Weight**: Bold
- **Line Height**: 1.1

#### Colors
- **Text**: White `[255, 255, 255]`
- **Outline**: Black `[0, 0, 0]` (6px width)
- **Background**: Dark Blue `[0, 51, 102]`
- **Background Highlighted**: Same `[0, 51, 102]`

#### Background Parameters
- **Padding**: X: 120px, Y: 50px
- **Corner Radius**: 30px
- **Opacity**: 1.0 (fully opaque)
- **Brightness Boost**: 0 (no change on highlight)

#### Highlighting Behavior
- **Effect Type**: `background`
- **Highlight Method**: `none`
- **Animation**: No visual change on highlight (consistent professional look)
- **Multi-line Support**: Yes
- **Dynamic Width**: Yes
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_background_text()` method in `json_style_loader.py`
- Auto-scales font size when text exceeds safe zone (980px max width)
- Creates large rounded rectangle background containing all text
- Font scales down intelligently (e.g., 140px → 119px for long text)
- Maintains professional news broadcaster aesthetic

---

### 3. Glow Caption
**Purpose**: Gaming & tech content with neon glow effects

#### Typography
- **Font**: Impact (`/Users/naman/Library/Fonts/Impact.ttf`)
- **Size**: 72px (both normal and highlighted)
- **Transform**: Uppercase
- **Alignment**: Center
- **Weight**: Bold

#### Colors
- **Normal Text**: White `[255, 255, 255]`
- **Highlighted Text**: Bright Green `[57, 255, 20]`

#### Shadow Configuration
- **Primary Shadow**: 
  - Offset: X: 0, Y: 0
  - Blur: 18px
  - Color: `rgba(currentColor, 0.8)`
  - Normal Opacity: 0.8, Highlighted: 0.96
- **Secondary Shadow**:
  - Offset: X: 0, Y: 0
  - Blur: 27px
  - Color: `rgba(currentColor, 0.6)`
  - Normal Opacity: 0.6, Highlighted: 0.72

#### Highlighting Behavior
- **Effect Type**: `text_shadow`
- **Highlight Method**: `color_change_with_shadow`
- **Animation**: Text color changes from white to bright green with intensified glow
- **Transition Duration**: 0.2 seconds
- **Word-Level Styling**: Yes
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_text_shadow_text()` method in `json_style_loader.py`
- Calls `TextEffects.create_text_shadow_glow_effect()` from `text_effects.py`
- Renders layered shadows: shadow layer first, then text layer
- Dynamic color fill changes shadow color to match text color
- Creates intense neon glow effect perfect for gaming content

---

### 4. Karaoke Style
**Purpose**: Y2K nostalgic karaoke for music and entertainment

#### Typography
- **Font**: Alverata Bold Italic (`/Users/naman/Library/Fonts/alverata-bold-italic.ttf`)
- **Size**: 108px (both normal and highlighted)
- **Transform**: Uppercase
- **Alignment**: Center
- **Weight**: 800

#### Colors
- **Normal Text**: White `[255, 255, 255]`
- **Highlighted Text**: Yellow `[255, 255, 0]`
- **Normal Glow**: White `[255, 255, 255]`
- **Highlighted Glow**: Yellow `[255, 255, 0]`

#### Effect Parameters
- **Glow Radius**: 0 (disabled for crisp look)
- **Glow Intensity**: 0.0 (disabled)
- **Two-Tone Words**: Enabled
- **Text Crisp**: Yes
- **Layered Rendering**: No
- **Pulse**: Disabled

#### Highlighting Behavior
- **Effect Type**: `dual_glow`
- **Highlight Method**: `two_tone_no_glow`
- **Animation**: Individual word color changes from white to yellow
- **Transition Duration**: 0.2 seconds
- **Word-Level Styling**: Yes
- **Separate Word Colors**: Yes
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_dual_glow_text()` method in `json_style_loader.py`
- Calls `TextEffects.create_two_tone_glow_effect()` from `text_effects.py`
- Renders each word separately with individual color states
- No glow effects for clean, crisp appearance
- Classic karaoke-style word highlighting with elegant italic serif font

---

### 5. Highlight Caption (Hormozi Style)
**Purpose**: Alex Hormozi-style motivational content

#### Typography
- **Font**: Mazzard M Bold (`/Users/naman/Library/Fonts/mazzard-m-bold.otf`)
- **Size**: 80px (both normal and highlighted)
- **Transform**: None (preserves original case)
- **Alignment**: Center
- **Weight**: Bold

#### Colors
- **Text**: White `[255, 255, 255]`
- **Highlight Background**: Purple `[126, 87, 194]`
- **Normal Background**: None (transparent)

#### Background Parameters
- **Padding**: X: 15px, Y: 10px
- **Corner Radius**: 20px
- **Normal Background Color**: null (transparent)

#### Highlighting Behavior
- **Effect Type**: `word_highlight`
- **Highlight Method**: `background_per_word`
- **Animation**: Purple background appears behind individual words when highlighted
- **Transition Duration**: 0.2 seconds
- **Background-Per-Word**: Only highlighted word gets background
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_word_highlight_text()` method in `json_style_loader.py`
- Calls `WordHighlightEffects.create_word_background_highlight_effect()` from `word_highlight_effects.py`
- Renders backgrounds first, then text on top
- Only active word receives colored background
- Preserves text case for natural speech patterns
- Ideal for motivational and business content

---

### 6. Deep Diver
**Purpose**: Deep thoughts style with grey background and contrasting text

#### Typography
- **Font**: Publica Sans Round Bold (`/Users/naman/Library/Fonts/PublicaSansRound-Bd.otf`)
- **Size**: 70px (both normal and highlighted)
- **Transform**: Lowercase
- **Alignment**: Center
- **Weight**: Bold
- **Line Height**: 1.1

#### Colors
- **Active Text**: Black `[0, 0, 0]`
- **Inactive Text**: Medium Gray `[80, 80, 80]`
- **Background**: Light Gray `[140, 140, 140]`

#### Background Parameters
- **Padding**: X: 15px, Y: 8px (optimized for tight fit)
- **Corner Radius**: 25px
- **Full Background**: Contains all text words

#### Highlighting Behavior
- **Effect Type**: `deep_diver`
- **Highlight Method**: `deep_diver`
- **Animation**: Active word appears in black, inactive words in gray
- **Transition Duration**: 0.2 seconds
- **Multi-line Support**: Yes
- **Dynamic Width**: Yes
- **Words Per Window**: 3

#### Implementation Details
- Uses `_create_deep_diver_text()` method in `json_style_loader.py`
- Calls `WordHighlightEffects.create_deep_diver_effect()` from `word_highlight_effects_manual_fix.py`
- Renders single background encompassing all text
- Each word colored individually based on active state
- Perfect text centering using font metrics (ascent/descent)
- Optimized background sizing prevents oversized boxes
- **Manual Centering Fix**: Applied -40px horizontal offset to correct rendering alignment issue
- Ideal for philosophical, contemplative, or educational content

## Technical Implementation Details

### Word Timing System
Each word contains:
```json
{
  "word": "example",
  "start": 1.25,
  "end": 1.75
}
```

### Highlighting Logic
1. **Time-based Activation**: Words highlight when `current_time` falls between `start` and `end` timestamps
2. **Word Index Tracking**: `highlighted_word_index` parameter passed to rendering functions
3. **Window Management**: Text grouped into 3-word windows for better readability
4. **Auto-scaling**: Font sizes automatically reduced if text exceeds safe zone boundaries

### Safe Zone Management
- **Horizontal Margins**: 100px on each side
- **Top Margin**: 220px
- **Bottom Margin**: 450px
- **Max Width Limits**: Varies by style (800-980px)
- **Auto-scaling**: Prevents text overflow while maintaining readability

### Effect Type Routing
```python
# In json_style_loader.py
if effect_type == 'outline':          # Simple Caption
    return self._create_outline_text()
elif effect_type == 'background':     # Background Caption  
    return self._create_background_text()
elif effect_type == 'dual_glow':      # Karaoke Style
    return self._create_dual_glow_text()
elif effect_type == 'text_shadow':    # Glow Caption
    return self._create_text_shadow_text()
elif effect_type == 'word_highlight': # Highlight Caption
    return self._create_word_highlight_text()
elif effect_type == 'deep_diver':     # Deep Diver
    return self._create_deep_diver_text()
```

### Movis Integration
- **Layer Type**: `StyledSubtitleLayer` class in `movis_layer.py`
- **Rendering**: Returns RGBA numpy arrays compatible with Movis
- **Timing**: Integrates with Movis timeline for precise synchronization
- **Resolution**: Optimized for 1080x1920 (9:16 aspect ratio)

## Performance Considerations

### Font Loading
- Fonts loaded once and cached during style initialization
- Fallback to system defaults if custom fonts unavailable
- Auto-scaling calculations minimize rendering overhead

### Rendering Optimization
- Pre-calculated word windows reduce real-time processing
- Effect-specific optimizations (e.g., disabled glow for karaoke style)
- Safe zone calculations performed once during initialization

### Memory Management
- RGBA arrays used for transparency support
- Efficient canvas sizing based on content requirements
- Crop operations to minimize memory footprint

## Usage Examples

### Basic Implementation
```python
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

# Load style configuration
style = StyleLoader.load_style_from_json(json_path, "simple_caption")

# Create subtitle layer
subtitle_layer = StyledSubtitleLayer(
    words=word_timestamps,
    style=style,
    resolution=(1080, 1920),
    position="bottom",
    safe_zones=True
)

# Add to Movis composition
composition.add_layer(subtitle_layer, name="subtitles")
```

### Custom Color Modifications
```json
// In subtitle_styles_v3.json
"colors": {
  "active_text": [0, 0, 0],     // Black for active word
  "inactive_text": [80, 80, 80], // Gray for inactive words  
  "background": [140, 140, 140]   // Light gray background
}
```

### 8. Green Goblin
**Purpose**: Clean dynamic highlighting without glow effects for professional presentations

#### Typography
- **Font**: Manrope ExtraBold (`/Users/naman/Desktop/movie_py/subtitle_styles/fonts/Manrope-ExtraBold.ttf`)
- **Size**: 108px (both normal and highlighted)
- **Transform**: Uppercase
- **Alignment**: Center
- **Weight**: 800 (ExtraBold)

#### Colors
- **Text Normal**: White `[255, 255, 255]`
- **Text Highlighted**: Bright Green `[57, 255, 20]`
- **Outline**: Black `[0, 0, 0]`
- **Outline Width**: 3px

#### Highlighting Behavior
- **Effect Type**: `dual_glow`
- **Highlight Method**: `dual_glow_with_scale`
- **Animation**: Color change (white → green) + auto-scaling (1.1x)
- **Transition Duration**: 0.2 seconds
- **Words Per Window**: 3
- **Glow**: Disabled (radius=0, intensity=0.0)

#### Implementation Details
- Uses `_render_dual_glow_style()` method in `movis_layer.py`
- Calls `TextEffects.create_dual_glow_text()` from `text_effects.py`
- Combines karaoke-style effects with clean outline rendering
- Auto-scaling provides emphasis without glow effects
- Same font and sizing as karaoke style but different color scheme

---

### 9. Sgone Caption
**Purpose**: Center-positioned style with The Sgone font displaying maximum 2 words at a time

#### Typography
- **Font**: The Sgone (`/Users/naman/Desktop/movie_py/subtitle_styles/fonts/The Sgone.otf`)
- **Size**: 65px (normal), 75px (highlighted)
- **Transform**: Lowercase
- **Alignment**: Center
- **Weight**: Regular

#### Colors
- **Text**: White `[255, 255, 255]`
- **Outline**: Black `[0, 0, 0]`
- **Outline Width**: 4px

#### Positioning
- **Layout**: Center screen positioning
- **Safe Margins**: Top: 200px, Bottom: 200px, Horizontal: 100px
- **Max Width**: 600px (prevents text overflow)

#### Highlighting Behavior
- **Effect Type**: `outline`
- **Highlight Method**: `size_pulse`
- **Animation**: Text size increases from 65px to 75px when highlighted
- **Transition Duration**: 0.2 seconds
- **Words Per Window**: 2 (strictly enforced)

#### Implementation Details
- Uses `_create_outline_text()` method in `json_style_loader.py`
- Calls `TextEffects.create_outline_effect()` from `text_effects.py`
- **Auto-scaling enabled**: Font reduces if text exceeds 600px width
- **Fixed word windowing**: Only 2 words displayed at once, cycling through pairs
- Custom font integration with The Sgone typeface
- Center positioning optimized for social media formats
- Ideal for artistic, unique content with distinctive typography

## Troubleshooting

### Deep Diver Centering Issue (Fixed)
**Problem**: In 9:16 format, the Deep Diver caption appeared shifted to the right.

**Solution**: Manual horizontal offset adjustment in `word_highlight_effects_manual_fix.py`
- Edit `MANUAL_OFFSET = -40` to adjust centering
- Negative values shift left, positive values shift right
- Test with increments of 5-10 pixels for fine-tuning

**Files Modified**:
- `subtitle_styles/effects/word_highlight_effects_manual_fix.py` (fix implementation)
- `subtitle_styles/core/movis_layer.py` (import update)
- `subtitle_styles/core/json_style_loader.py` (import update)

## Future Development

### Adding New Styles
1. Define style configuration in `subtitle_styles_v3.json`
2. Create new effect type if needed
3. Add routing in `json_style_loader.py`
4. Implement rendering method in appropriate effects file
5. Test with various text lengths and timing scenarios

### Supported Platforms
All styles optimized for:
- **Instagram Stories/Reels**: 1080x1920
- **YouTube Shorts**: 1080x1920  
- **TikTok**: 1080x1920
- **Safe zones**: Ensures visibility across all platforms

This comprehensive system provides professional-quality, synchronized subtitle effects that enhance video content across social media platforms while maintaining excellent performance and flexibility.