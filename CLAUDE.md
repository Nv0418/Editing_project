# CLAUDE.md - VinVideo Project Context

## Project Overview
VinVideo is an AI-powered video editing platform with a focus on subtitle styling and automated video generation. The project uses Movis (Python video editing library) as the core rendering engine.

## Current Development Focus
Building a comprehensive subtitle style system with an Aicut-inspired user interface for style selection and preview.

## Current Interface Status
**Active Interface**: `/Users/naman/Desktop/movie_py/accurate_react_preview.html`
- **Working perfectly** - React-based 60/40 split layout
- **User-approved design** - Font display and style selection functionality confirmed good
- **Accurate preview system** - Uses actual subtitle rendering pipeline for pixel-perfect previews
- **Integration ready** - Connected to `style_preview_generator.py` for real rendering

## Key Requirements

### UI/UX Design Direction
**IMPORTANT**: We are looking to always get a similar interface like the Aicut screenshot located at:
`/Users/naman/Desktop/movie_py/other_root_files/aicut_ss.png`

The target interface should have:
- Left panel: Grid of caption style buttons (colorful, branded for each style)
- Right panel: Large preview screen showing selected style with live text
- Bottom controls: Text input and generation controls
- Clean, modern design matching Aicut's professional appearance

### Subtitle Style System
- 10 unique Aicut-inspired subtitle styles implemented
- JSON-based configuration system (`subtitle_styles/config/subtitle_styles_v2.json`)
- Support for outline, background, and glow effects
- Word-by-word karaoke-style highlighting with NVIDIA Parakeet integration
- Instagram format optimization (1080x1920) with safe zones

### Technical Stack
- **Backend**: Python with Movis library for video rendering
- **Frontend**: HTML/CSS/JavaScript for preview interfaces
- **Data Format**: JSON for style configurations
- **Audio Processing**: NVIDIA Parakeet for word-level timestamps
- **Export**: MP4 video generation with FFmpeg

## File Structure
```
subtitle_styles/
├── config/
│   └── subtitle_styles_v2.json    # Main style definitions
├── core/
│   ├── json_style_loader.py       # Style loading logic
│   └── movis_layer.py             # Movis integration
└── effects/
    └── text_effects.py            # PIL-based text effects

interfaces/
├── aicut_style_interface.html     # Main Aicut-style interface
└── accurate_style_preview.html    # Development/testing interface
```

## Available Subtitle Styles
1. Simple Caption (white text, black outline)
2. Glow Caption (pink glow effect)
3. Background Caption (cyan background)
4. Highlight Caption (purple gradient background)
5. Dashing Caption (orange glow)
6. Newscore (yellow text, black outline)
7. Popling Caption (pink text, pink outline)
8. Whistle Caption (teal gradient background)
9. Karaoke Caption (white text, green outline/glow)
10. Tilted Caption (orange text, tilted)

## Key Commands
```bash
# Generate style previews
python3 style_preview_generator.py --text "Custom Text"

# Test specific style
python3 test_json_styled_video.py --style simple_caption --text "Test"

# Quick preview workflow
python3 quick_preview.py
```

## Current Issues to Address
- Text visibility in preview interfaces (black text on black background)
- Ensuring live preview matches actual video output exactly
- Maintaining Aicut-style interface consistency across all tools

## NEXT PRIORITY TASK
**Perfect Individual Subtitle Styles** (Phase 2)
- **Current Status**: 10 styles replicated from Aicut screenshots but not pixel-perfect
- **Goal**: Hand-craft each style to perfection with proper design language
- **Tasks**:
  - Analyze each of the 10 styles individually  
  - Adjust fonts, colors, outlines, highlights for each style
  - Perfect typography, effects, and visual appearance
  - Test each style in React interface for accuracy
  - Ensure each style has distinct, professional appearance

## Development Priorities
1. **IMMEDIATE**: Perfect all 10 individual subtitle styles
2. Integrate with main VinVideo editing pipeline
3. Add transition effects between subtitle styles
4. Implement real-time preview generation

## Notes
- All subtitle styles should be clearly visible and distinguishable
- Preview interfaces must accurately represent final video output
- Maintain backwards compatibility with existing JSON configurations
- Focus on user experience matching professional tools like Aicut