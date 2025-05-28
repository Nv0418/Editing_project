# Movis Subtitle System

## Overview
A comprehensive subtitle system that integrates Nvidia Parakeet transcription data with movis for video production. Creates videos with synchronized subtitles using per-word timing data.

## Features
- 🎯 **Precise Timing**: Uses Nvidia Parakeet per-word timing for accurate subtitle placement
- 📝 **Smart Segmentation**: Automatically groups words into readable subtitle segments
- 🎨 **Flexible Styling**: Customizable fonts, colors, and positioning
- 📤 **Multiple Formats**: Export to SRT, ASS, and direct movis integration
- ⚡ **Fast Rendering**: Optimized for movis rendering pipeline
- 🎬 **Video Generation**: Create complete videos with audio and subtitles

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_subtitles.txt
```

### 2. Run Test
```bash
python test_subtitles.py
```

### 3. Basic Usage
```python
from movis_subtitle_generator import MovisSubtitleVideo

# Create video with subtitles
generator = MovisSubtitleVideo(
    audio_file="got_script.mp3",
    parakeet_file="parakeet_output.json"
)

# Generate video
generator.create_basic_subtitle_video("output.mp4")
```

## Files
- `subtitle_processor.py` - Core subtitle processing logic
- `movis_subtitle_generator.py` - Movis video generation with subtitles
- `test_subtitles.py` - Complete workflow test
- `parakeet_output.json` - Example Nvidia Parakeet transcription
- `got_script.mp3` - Example audio file

## Configuration Options

### Subtitle Segmentation
```python
processor.create_subtitle_segments(
    max_duration=3.0,  # Max subtitle duration in seconds
    max_words=8,       # Max words per subtitle
    min_gap=0.3        # Min gap between subtitles
)
```

### Video Styling
```python
subtitle_style = {
    'font_size': 48,
    'font_family': 'Helvetica', 
    'color': '#ffffff',
    'position': (960, 930)  # x, y coordinates
}
```

## Output
- **Video**: MP4 with black background, audio, and subtitles
- **SRT**: Standard subtitle format
- **ASS**: Advanced subtitle format with styling
