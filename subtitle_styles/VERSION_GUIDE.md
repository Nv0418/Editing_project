# VinVideo Subtitle Styles - Version Guide

## 📁 Configuration Files Overview

### Current Active Versions

**📋 subtitle_styles_v2.json** - Original Research-Based Configuration
- **Purpose**: Backup of our original font diversity approach
- **Fonts**: Oswald, Bicyclette, RobotoCondensed variations
- **Status**: ✅ Working backup
- **Use Case**: Fallback or A/B testing

**📋 subtitle_styles_v3.json** - Advanced Research-Based Configuration  
- **Purpose**: Current production configuration with specialized fonts
- **Fonts**: Purpose-driven fonts (Montserrat, Impact, Shrikhand, etc.)
- **Status**: ✅ Active (default)
- **Use Case**: Primary production system

## 🔄 Version Differences

### v2 (Original)
```json
"simple_caption": {
  "font_family": "Arial Black",
  "description": "Clean, bold text with black outline for maximum readability"
}
"glow_caption": {
  "font_family": "Arial Black",  
  "colors": {
    "text_highlighted": [255, 80, 80]
  }
}
```

### v3 (Current) 
```json
"simple_caption": {
  "font_family": "/Users/naman/Library/Fonts/Oswald-Heavy.ttf",
  "description": "Clean, educational text for tutorials and how-to content"
}
"glow_caption": {
  "font_family": "/System/Library/Fonts/Supplemental/Impact.ttf",
  "colors": {
    "text_highlighted": [57, 255, 20]
  }
}
```

## 🎯 Default System Behavior

**Current Default**: v3 (subtitle_styles_v3.json)
- Video generation: Uses v3 automatically
- Preview generation: Uses v3 automatically
- React app: Configured for v3 fonts

**To Use v2**: Specify explicitly
```bash
# Video generation with v2
python3 test_json_styled_video.py --json subtitle_styles/config/subtitle_styles_v2.json --style simple_caption

# Preview generation with v2
python3 style_preview_generator.py --config v2 --style simple_caption
```

## 📊 Font Comparison

| Style | v2 Font | v3 Font | Purpose (v3) |
|-------|---------|---------|--------------|
| SIMPLE CAPTION | Arial Black | Oswald-Heavy | Educational content |
| BACKGROUND CAPTION | Arial Black | Roboto Condensed | Professional news |
| KARAOKE STYLE | Tide Sans 900 | Shrikhand | Music/Entertainment |
| GLOW CAPTION | Arial Black | Impact | Gaming/Tech |
| HIGHLIGHT CAPTION | Arial Black | Montserrat-Black | Motivational (Hormozi) |
| DASHING CAPTION | Arial Black | Quicksand-Bold | Fashion/Lifestyle |
| NEWSCORE | Arial Black | Oswald-Bold | Breaking news |
| POPLING CAPTION | Arial Black | Fredoka-Bold | Kids content |
| WHISTLE CAPTION | Arial Black | Nunito-Regular | Wellness/ASMR |
| KARAOKE CAPTION | Arial Black | BebasNeue-Regular | Live streaming |
| TILTED CAPTION | Arial Black | LobsterTwo-Italic | Comedy/Memes |

## 🔄 Switching Between Versions

### To Switch to v2 (Original)
```bash
# Temporarily use v2 for testing
python3 test_json_styled_video.py --json subtitle_styles/config/subtitle_styles_v2.json --style [style_name]
```

### To Switch Back to v3 (Current)  
```bash
# Default behavior (no flags needed)
python3 test_json_styled_video.py --style [style_name]
```

### To Make v2 Default Again
```python
# Edit test_json_styled_video.py line 44
json_file = project_root / "subtitle_styles" / "config" / "subtitle_styles_v2.json"

# Edit style_preview_generator.py line 18  
self.config_path = script_dir / "subtitle_styles/config/subtitle_styles_v2.json"
```

## ✅ Backup Safety

**Both versions are preserved:**
- ✅ v2: Original configuration safely backed up
- ✅ v3: New research-based configuration active
- ✅ Font files: All fonts from both versions installed
- ✅ Rollback: Can easily switch between versions
- ✅ Testing: Both versions tested and working

## 🚀 Recommendations

**For Production**: Use v3 (current default)
- Purpose-driven fonts for specific video types
- Research-backed color optimizations
- Better visual hierarchy and branding

**For Comparison**: Test with v2
- A/B testing between font approaches
- Fallback if specific fonts cause issues
- Client preference testing

---
*Version management implemented for VinVideo subtitle system*