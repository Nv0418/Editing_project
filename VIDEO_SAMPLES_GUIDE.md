# VinVideo - Video Samples Guide

## 📹 **Preserved Video Samples**

After Phase 2 cleanup, we've kept one representative video for each major subtitle style:

### 🎯 **V3 Style Samples** (Latest Research-Based Fonts)
**Location**: `./output_test/v3_samples/`

| Video File | Style | Purpose | Font Used |
|------------|-------|---------|-----------|
| `json_styled_simple_caption.mp4` | SIMPLE CAPTION | Educational content | Oswald-Heavy |
| `json_styled_background_caption.mp4` | BACKGROUND CAPTION | Professional news | Roboto Condensed |
| `json_styled_karaoke_style.mp4` | KARAOKE STYLE | Music/Entertainment | Shrikhand |
| `json_styled_glow_caption.mp4` | GLOW CAPTION | Gaming/Tech | Impact |
| `json_styled_highlight_caption.mp4` | HORMOZI CAPTION | Motivational content | Montserrat-Black |
| `json_styled_dashing_caption.mp4` | DASHING CAPTION | Fashion/Lifestyle | Quicksand-Bold |
| `json_styled_newscore.mp4` | NEWSCORE | Breaking news | Oswald-Bold |
| `json_styled_tilted_caption.mp4` | TILTED CAPTION | Comedy/Memes | LobsterTwo-Italic |
| `json_styled_whistle_caption.mp4` | WHISTLE CAPTION | Wellness/ASMR | Nunito-Regular |

### 📊 **Coverage Status**

**✅ Covered Styles (9/11)**:
- Simple Caption ✅
- Background Caption ✅  
- Karaoke Style ✅
- Glow Caption ✅
- Hormozi Caption ✅
- Dashing Caption ✅
- Newscore ✅
- Tilted Caption ✅
- Whistle Caption ✅

**📝 Missing Samples** (can be generated on demand):
- `popling_caption` (POPLING CAPTION - Kids content)
- `karaoke_caption` (LIVE CAPTION - Sports/Streaming)

### 🎬 **Video Details**
- **Audio**: Game of Thrones script (~21 seconds)
- **Resolution**: 1080x1920 (Instagram Stories format)
- **Quality**: High (original generation settings)
- **Total Size**: ~4.2MB (compact, efficient)

### 🔄 **Regenerating Samples**

To generate missing or updated samples:

```bash
# Generate specific style
python3 test_json_styled_video.py --style popling_caption

# Generate with v2 configuration (backup)
python3 test_json_styled_video.py --json subtitle_styles/config/subtitle_styles_v2_updated.json --style simple_caption

# Generate all styles (time-consuming)
python3 test_json_styled_video.py --all
```

### 💾 **Space Efficiency**

**Before Cleanup**: ~500MB+ (25+ videos)  
**After Cleanup**: ~4.2MB (9 videos)  
**Space Saved**: ~99% reduction while preserving functionality

### 🎯 **Usage**

These samples serve as:
- **Quality Reference**: Visual verification of each style
- **Client Demos**: Show different subtitle options
- **Testing Baseline**: Compare future updates
- **Development Reference**: Visual guide for further improvements

---
*Phase 2 cleanup: Maximum space savings with complete style coverage*