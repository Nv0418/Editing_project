# VinVideo - AI Video Creation Platform
## Codex OpenAI Platform Deployment Guide

### Quick Start
```bash
# 1. Setup environment
python3 setup.py

# 2. Test subtitle styles
python3 Finalized_styles/test_v3_styles.py

# 3. Run React preview (optional)
cd react_style_showcase/subtitle_preview_app
npm start
```

### Project Structure
```
VinVideo/
├── subtitle_styles/          # Core subtitle system
│   ├── config/              # Style configurations
│   ├── core/                # Loading and rendering logic
│   └── effects/             # Text effects implementation
├── movis/                   # Video rendering library
├── editing_pipeline/        # Video editing agents
├── react_style_showcase/    # Web preview interface
├── project_fonts/           # Typography assets
└── other_root_files/        # Audio and media assets
```

### Dependencies
- **Python 3.8+** with movis, opencv-python, pillow
- **Node.js 16+** for React preview interface
- **FFmpeg** for video processing

### Environment Variables
Create `.env` file with:
```bash
# API Keys (if using external services)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Paths
PROJECT_ROOT=/path/to/project
FONT_PATH=/path/to/fonts
OUTPUT_PATH=/path/to/output
```

### Key Features
- ✅ 6 Professional subtitle styles (Instagram format)
- ✅ Word-by-word highlighting with audio sync
- ✅ JSON-based style configuration
- ✅ React preview interface
- ✅ Movis video rendering pipeline
- 🚧 LLM editing agents (in development)

### Testing
```bash
# Test all subtitle styles
python3 Finalized_styles/test_v3_styles.py

# Test specific style
python3 Finalized_styles/test_v3_styles.py --style simple_caption

# Generate React previews
python3 react_style_showcase/style_preview_generator.py
```

### Troubleshooting
1. **Missing fonts**: Fonts will be loaded from project_fonts/ directory
2. **Audio files**: Place test audio in other_root_files/
3. **Output issues**: Check output_test/ directory permissions
4. **React issues**: Run `npm install` in subtitle_preview_app/

### Production Notes
- All media files are gitignored for performance
- Environment files are excluded from repository
- Node modules will be installed fresh on platform
- Python dependencies listed in requirements.txt