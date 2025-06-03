# Editing Pipeline Core Components

This folder contains the essential files for the VinVideo AI-powered video editing pipeline.

## Core Files

### 1. **QWEN_EDITING_AGENT_SYSTEM_MESSAGE.md**
- The system message for the Qwen-3 32B LLM Editing Agent
- Defines how the AI understands and processes video editing tasks
- Contains input/output specifications and creative guidelines

### 2. **editing_agent_to_movis.py**
- Converts Editing Agent JSON output to Movis video compositions
- Validates JSON structure and asset paths
- Handles the bridge between AI decisions and video rendering
- **NEW**: Supports format override from command line

**Usage:**
```bash
# Basic usage
python3 editing_agent_to_movis.py editing_plan.json output.mp4

# Override format from JSON
python3 editing_agent_to_movis.py editing_plan.json output.mp4 --format 16:9

# Multiple overrides
python3 editing_agent_to_movis.py editing_plan.json output.mp4 --format 1:1 --platform instagram --quality high
```

### 3. **dynamic_video_editor.py**
- Main video composition engine using Movis
- Handles multi-layer video/audio/subtitle composition
- Supports animations, effects, and platform optimization
- Integrates all 9 professional subtitle styles
- **NEW**: Format-based resolution selection (9:16, 16:9, etc.)

**Usage:**
```bash
# Using format ratio
python3 dynamic_video_editor.py --format 9:16 --config editing_plan.json --output final.mp4

# Using explicit resolution
python3 dynamic_video_editor.py --resolution 1920x1080 --config editing_plan.json --output final.mp4

# Format in JSON config
{
  "composition": {
    "format": "16:9",  // or "resolution": [1920, 1080]
    "duration": 30.0
  }
}
```

### 4. **dynamic_image_sequence_editor.py** (formerly dynamic_assets_video_generator.py)
- Creates videos from asset folders (images, audio, cuts)
- Automatically discovers and sequences assets
- Applies Ken Burns effects and transitions
- Used for generating videos from image sequences
- **NEW**: Supports multiple video formats

**Usage:**
```bash
# Vertical video (default)
python3 dynamic_image_sequence_editor.py --assets-dir assets_2 --output video.mp4

# Horizontal video
python3 dynamic_image_sequence_editor.py --assets-dir assets_2 --format 16:9 --output video.mp4

# Square video
python3 dynamic_image_sequence_editor.py --assets-dir assets_2 --format 1:1 --output square.mp4
```

## Pipeline Flow

```
1. AI Agents (Producer, Director, Prompt Engineer)
   ↓
2. LLM Editing Agent (uses QWEN_EDITING_AGENT_SYSTEM_MESSAGE.md)
   ↓
3. JSON Editing Plan
   ↓
4. editing_agent_to_movis.py (conversion)
   ↓
5. dynamic_video_editor.py (composition)
   ↓
6. Final MP4 Video
```

## Key Features

- **AI-Driven Editing**: LLM makes creative decisions based on prompts
- **Multi-Layer Composition**: Videos, images, audio, subtitles
- **Professional Subtitles**: 9 styles with word-by-word sync
- **Platform Optimization**: Instagram, TikTok, YouTube Shorts
- **Animation System**: Keyframes with 35+ easing functions
- **Effect Library**: Blur, glow, shadow, Ken Burns
- **Format Support**: Multiple aspect ratios (9:16, 16:9, 4:5, 1:1, etc.)

## Supported Video Formats

The pipeline now supports automatic resolution selection based on format ratios:

| Format | Resolution | Use Case |
|--------|------------|----------|
| 9:16   | 1080×1920  | Instagram Stories, TikTok, YouTube Shorts |
| 16:9   | 1920×1080  | YouTube, TV, Standard Video |
| 4:5    | 1080×1350  | Instagram Feed Posts |
| 1:1    | 1080×1080  | Instagram/Facebook Square Posts |
| 21:9   | 2560×1080  | Ultrawide Cinematic |
| 4:3    | 1440×1080  | Classic TV Format |
| Custom | Calculated | Any ratio (e.g., "3:2", "5:4")

## Requirements

- Python 3.8+
- Movis library
- Subtitle styles system (../subtitle_styles/)
- NVIDIA Parakeet transcriptions for subtitles

## Quick Start

1. Generate editing plan with LLM agent
2. Convert to video: `python3 editing_agent_to_movis.py plan.json output.mp4`
3. Or use direct editing: `python3 dynamic_video_editor.py --config plan.json`
4. For custom formats: Add `--format 16:9` to any command

All scripts include comprehensive help: `python3 [script].py --help`