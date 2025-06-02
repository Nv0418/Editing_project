# CLAUDE.md - VinVideo Project Context

## Project Overview
VinVideo is an AI-powered video creation platform that automates the entire short-form content production process (like YouTube Shorts, Reels, TikToks). Users can input a script or concept, and VinVideo uses multiple AI agents—like a Director, Producer, and DoP—to generate, edit, and stylize videos with minimal manual effort. The system integrates AI models for script understanding, image and video generation, scene planning, and smart editing decisions.

The project uses Movis (Python video editing library) as the core rendering engine for video composition and effects.

## Current Module: Subtitle Style Selection
We are currently developing the subtitle style selection interface - one component of the larger VinVideo platform. This module allows users to choose from professional subtitle styles for their generated videos, presented in an Aicut-like interface.

## Current Development Focus
🚧 **IN PROGRESS**: Comprehensive subtitle style system (6/11 professional styles completed)
🎯 **CURRENT FOCUS**: Finalizing remaining 5 subtitle styles before UI development

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

### Subtitle Style System 🚧 IN PROGRESS (6/11 Complete)
- **6 professional subtitle styles** finalized and production-ready
- **5 additional styles** pending finalization to complete full Aicut-inspired set
- **JSON-based configuration system** (`subtitle_styles/config/subtitle_styles_v3.json`)
- **Advanced effect types**: outline, background, text_shadow, dual_glow, word_highlight, deep_diver
- **Word-by-word highlighting** with NVIDIA Parakeet integration and audio sync
- **Instagram format optimization** (1080x1920) with safe zone compliance
- **Professional typography** with custom fonts and auto-scaling

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
│   └── subtitle_styles_v3.json           # Main style definitions
├── core/
│   ├── json_style_loader.py              # Style loading logic
│   └── movis_layer.py                     # Movis integration
└── effects/
    ├── text_effects.py                    # Color-based effects
    └── word_highlight_effects.py          # Background-based effects

react_style_showcase/                      # Preview system
├── style_preview_generator.py             # Static preview generation
└── subtitle_preview_app/                  # React interface
```

## Subtitle Styles Progress (6/11 Complete)

### ✅ FINALIZED STYLES (Production Ready)
1. **Simple Caption** - Educational content (Oswald Heavy, size-pulse effect)
2. **Background Caption** - News style (Bicyclette Black, dark blue background)
3. **Glow Caption** - Gaming/tech (Impact, green glow effects) 
4. **Karaoke Style** - Music content (Alverata Bold Italic, yellow highlights)
5. **Highlight Caption** - Motivational (Mazzard M Bold, purple word backgrounds)
6. **Deep Diver** - Contemplative (Publica Sans Round, contrasting text)

### 🚧 PENDING FINALIZATION (5 Remaining)
7. **Dashing Caption** - Orange glow effects
8. **Newscore** - Yellow text, black outline
9. **Popling Caption** - Pink text with effects
10. **Whistle Caption** - Teal gradient background
11. **Tilted Caption** - Orange text, rotated

## Key Commands
```bash
# Test all 6 styles with comprehensive validation
python3 test_v3_styles.py

# Test specific style with custom parameters  
python3 test_json_styled_video.py --style simple_caption --text "Test"

# Generate style previews for React interface
python3 react_style_showcase/style_preview_generator.py

# Quick development preview
python3 quick_preview.py

# Test Deep Diver style with centering fix
python3 30may_test/generate_deep_diver_video.py
```

## Known Issues and Fixes

### Deep Diver Centering Fix (May 30, 2025)
The Deep Diver caption style had a horizontal centering issue in 9:16 Instagram format where the gray background appeared shifted to the right. This has been fixed with a manual offset adjustment.

**Fix Location**: `subtitle_styles/effects/word_highlight_effects_manual_fix.py`
- Adjust `MANUAL_OFFSET = -40` value to fine-tune horizontal positioning
- Negative values shift left, positive values shift right
- Current setting shifts 40 pixels left to compensate for the rendering offset

## CURRENT PRIORITY TASK
**LLM-Based Editing Agent Development** (Phase 3 Implementation)
- **Current Status**: Hardcoded approach replaced with LLM-based intelligent agent
- **Goal**: Deploy Qwen-3 32B Editing Agent on RunPod for sophisticated video editing decisions
- **Immediate Tasks**:
  - Create comprehensive system message for Editing Agent
  - Define JSON schema specification with Movis capabilities
  - Build input format for Director/Producer/Prompt Engineer JSON files
  - Deploy and test LLM agent with real data validation
- **Success Criteria**: Generate accurate JSON editing plans compatible with existing Movis pipeline

## Development Priorities
1. **IMMEDIATE**: Deploy LLM-based Editing Agent on RunPod with Qwen-3 32B
2. **NEXT**: Complete system message and JSON schema specification
3. **CURRENT**: Test with real Director/Producer/Prompt Engineer data
4. **FUTURE**: Build Aicut-inspired user interface for style selection
5. **ADVANCED**: Real-time preview and API integration

## Essential Documentation
For complete understanding of the subtitle system, read these files in order:
1. **CLAUDE.md** (this file) - Project overview and status
2. **WORD_BY_WORD_EFFECTS_GUIDE.md** - Technical implementation details
3. **VIDEO_GENERATION_GUIDE.md** - How to generate test videos
4. **SUBTITLE_README.md** - Basic subtitle system overview
5. **subtitle_styles/config/subtitle_styles_v3.json** - Style configurations

## Notes
- All subtitle styles should be clearly visible and distinguishable
- Preview interfaces must accurately represent final video output
- Maintain backwards compatibility with existing JSON configurations
- Focus on user experience matching professional tools like Aicut
- Use VIDEO_GENERATION_GUIDE.md for consistent video testing