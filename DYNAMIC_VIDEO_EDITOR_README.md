# VinVideo Dynamic Video Editor

A comprehensive video editing script with Final Cut Pro-like timeline capabilities, integrated with VinVideo's professional subtitle system. This tool provides multi-layer composition, keyframe animations, platform-optimized export, and seamless integration with all 9 subtitle styles.

## Features

### 🎬 Core Capabilities
- **Multi-layer video composition** - Unlimited video/audio layers with precise control
- **Professional subtitle integration** - All 9 VinVideo subtitle styles with word-by-word sync
- **Timeline-based editing** - Trim, splice, concatenate, and arrange clips
- **Keyframe animations** - Animate position, scale, rotation, opacity with 35+ easing functions
- **Platform optimization** - Export presets for Instagram, TikTok, YouTube Shorts
- **Audio mixing** - Multi-track audio with ducking and fade effects
- **Effects system** - Apply blur, glow, shadow effects to any layer
- **JSON configuration** - Complex projects via JSON files

### 🎯 Subtitle Styles Available
1. **simple_caption** - Clean educational style
2. **background_caption** - News-style with background
3. **glow_caption** - Gaming/tech with glow effects
4. **karaoke_style** - Music content with word highlighting
5. **highlight_caption** - Motivational (Hormozi style)
6. **deep_diver** - Contemplative with contrasting text
7. **popling_caption** - Elegant underline effect
8. **greengoblin** - Clean karaoke without glow
9. **sgone_caption** - 2-word artistic display

## Installation

The script is already integrated into the VinVideo project. No additional installation required.

## Usage

### Basic Subtitle Generation

```bash
python3 dynamic_video_editor.py \
  --audio audio.mp3 \
  --parakeet parakeet_output.json \
  --style simple_caption \
  --output final_video.mp4
```

### Add Video Background

```bash
python3 dynamic_video_editor.py \
  --main-video background.mp4 \
  --audio narration.mp3 \
  --parakeet parakeet_output.json \
  --style highlight_caption \
  --output final_video.mp4
```

### Multi-Layer Composition

```bash
python3 dynamic_video_editor.py \
  --main-video main.mp4 \
  --overlay-videos "broll1.mp4,broll2.mp4" \
  --overlay-positions "top-right,bottom-left" \
  --overlay-opacities "0.8,0.6" \
  --overlay-times "10-15,20-25" \
  --background-music music.mp3 \
  --music-volume -15 \
  --music-ducking -10 \
  --audio narration.mp3 \
  --parakeet parakeet_output.json \
  --style karaoke_style \
  --platform instagram \
  --output final_video.mp4
```

### JSON Configuration

```bash
python3 dynamic_video_editor.py \
  --config editing_plan.json \
  --output final_video.mp4
```

## Command Line Options

### Input Options
- `--audio` - Path to audio file (narration/main audio)
- `--parakeet` - Path to NVIDIA Parakeet JSON transcription
- `--style` - Subtitle style to use (default: simple_caption)

### Video Options
- `--main-video` - Path to main video file
- `--overlay-videos` - Comma-separated overlay video paths
- `--overlay-positions` - Positions: top-right, bottom-left, or x:y coordinates
- `--overlay-opacities` - Opacity values 0.0-1.0 for each overlay
- `--overlay-times` - Time ranges (start-end) for each overlay

### Audio Options
- `--background-music` - Background music file path
- `--music-volume` - Background music level in dB (default: -15)
- `--music-ducking` - Ducking reduction when voice active

### Configuration
- `--config` - JSON configuration file path
- `--resolution` - Output resolution WIDTHxHEIGHT (default: 1080x1920)
- `--fps` - Frame rate (default: 30)
- `--background-color` - RGB values "R,G,B" (default: black)

### Export Options
- `--platform` - Platform optimization: instagram, tiktok, youtube_shorts, youtube
- `--quality` - Export quality: low, medium, high (default: medium)
- `--output` / `-o` - Output file path (default: output.mp4)

## JSON Configuration Format

Create complex editing projects with JSON configuration:

```json
{
  "composition": {
    "resolution": [1080, 1920],
    "duration": 60.0,
    "fps": 30,
    "background_color": [0, 0, 0]
  },
  "layers": [
    {
      "type": "video",
      "source": "main_footage.mp4",
      "name": "main",
      "position": [540, 960],
      "scale": 1.0,
      "opacity": 1.0,
      "start_time": 0.0,
      "duration": 60.0,
      "animations": {
        "opacity": {
          "keyframes": [0.0, 2.0, 58.0, 60.0],
          "values": [0.0, 1.0, 1.0, 0.0],
          "easings": ["ease_out", "linear", "ease_in"]
        }
      }
    },
    {
      "type": "video",
      "source": "overlay.mp4",
      "name": "pip",
      "position": [900, 200],
      "scale": 0.3,
      "opacity": 0.8,
      "start_time": 10.0,
      "duration": 15.0,
      "blending_mode": "overlay",
      "effects": ["glow", "shadow"]
    }
  ],
  "audio": {
    "background_music": {
      "source": "music.mp3",
      "level": -20.0,
      "fade_in": 3.0,
      "fade_out": 3.0,
      "ducking": {
        "trigger": "voice",
        "reduction": -10.0
      }
    },
    "narration": {
      "source": "voice.mp3",
      "offset": 5.0,
      "level": 0.0
    }
  },
  "subtitles": {
    "parakeet_data": "transcription.json",
    "style": "highlight_caption",
    "position": "bottom"
  },
  "export": {
    "platform": "instagram",
    "quality": "high"
  }
}
```

## Animation System

### Available Properties
- `position` - Animate X/Y position
- `scale` - Animate scale (uniform or X/Y separately)
- `rotation` - Animate rotation in degrees
- `opacity` - Animate transparency 0.0-1.0

### Easing Functions
- `linear` - Constant speed
- `ease_in`, `ease_out`, `ease_in_out` - Basic easing
- `ease_in2` to `ease_in5` - Progressively stronger ease in
- `ease_out2` to `ease_out5` - Progressively stronger ease out
- `ease_in_out2` to `ease_in_out5` - Progressively stronger ease in/out

### Example Animation
```json
"animations": {
  "position": {
    "keyframes": [0.0, 5.0, 10.0],
    "values": [[100, 100], [500, 300], [900, 100]],
    "easings": ["ease_out3", "ease_in3"]
  },
  "scale": {
    "keyframes": [0.0, 2.0],
    "values": [0.5, 1.0],
    "easings": ["ease_out"]
  }
}
```

## Platform Export Presets

### Instagram/TikTok
- Resolution: 1080x1920 (9:16)
- FPS: 30
- Codec: H.264
- Quality: CRF 23 (medium)

### YouTube Shorts
- Resolution: 1080x1920 (9:16)
- FPS: 30
- Codec: H.264
- Quality: CRF 18 (high)

### YouTube (Regular)
- Resolution: 1920x1080 (16:9)
- FPS: 30
- Codec: H.264
- Quality: CRF 18 (high)

## Advanced Features

### Multi-Layer Blending Modes
- `normal` - Standard compositing
- `multiply` - Darken blend
- `screen` - Lighten blend
- `overlay` - Contrast blend
- Additional Movis blending modes supported

### Audio Ducking
Automatically lower background music when voice is active:
```bash
--background-music music.mp3 --music-volume -15 --music-ducking -10
```

### Picture-in-Picture
Add overlay videos with custom positioning:
```bash
--overlay-videos "reaction.mp4" --overlay-positions "top-right" --overlay-opacities "0.9"
```

### Timeline Operations
- **Concatenate clips** - Join multiple videos sequentially
- **Split screen** - Multiple videos in grid layout
- **Transitions** - Fade, slide, cross-fade between clips
- **Trimming** - Cut specific portions of clips

## Integration with VinVideo

This script is designed to be called by VinVideo's AI agents (Director, Producer, DoP) as part of the automated video creation pipeline. It accepts standardized inputs and produces platform-optimized outputs ready for distribution.

## Performance

- Processes 60-second videos in under 2 minutes
- Automatic frame caching for repeated renders
- Parallel processing where applicable
- Memory-efficient handling of large videos

## Troubleshooting

### Common Issues

1. **ImportError**: Ensure you're in the correct directory with access to movis and subtitle_styles
2. **File not found**: Use absolute paths or verify relative paths from script location
3. **Memory issues**: Reduce preview_level or process shorter segments

### Debug Mode
Add verbose output by modifying the script to include print statements in key methods.

## Examples

### Create Instagram Reel with Subtitles
```bash
python3 dynamic_video_editor.py \
  --audio podcast.mp3 \
  --parakeet podcast_transcript.json \
  --style highlight_caption \
  --platform instagram \
  --quality high \
  --output instagram_reel.mp4
```

### Multi-Camera Edit
```bash
python3 dynamic_video_editor.py \
  --config multi_camera_edit.json \
  --output final_cut.mp4
```

### Music Video with Karaoke
```bash
python3 dynamic_video_editor.py \
  --main-video performance.mp4 \
  --audio song.mp3 \
  --parakeet lyrics.json \
  --style karaoke_style \
  --output music_video.mp4
```

## Future Enhancements

- Real-time preview server
- GPU acceleration
- More transition effects
- Advanced color grading
- Motion tracking
- Green screen support

## Credits

Built as part of the VinVideo AI-powered video creation platform using the Movis video editing library.