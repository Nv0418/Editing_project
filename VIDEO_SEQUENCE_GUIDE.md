# Dynamic Video Editor - Video Sequence Guide

This guide explains how to use the `dynamic_video_editor.py` to create videos from multiple video sources with intelligent scaling, transitions, and effects.

## Key Features

### 1. Intelligent Auto-Scaling for Videos
Each video is automatically analyzed and scaled to properly fill the screen:
- **Same aspect ratio**: Videos matching the target aspect ratio (within 1% tolerance) are scaled to fit exactly
- **Different aspect ratio**: Videos are scaled to "cover" the entire screen, preventing black borders
- **Landscape videos**: Automatically scaled and cropped to fit vertical formats like Instagram
- **Manual override**: Use the `scale` parameter for additional scaling on top of auto-scaling

### 2. Multi-Video Composition
Create complex video sequences with:
- Multiple video layers with precise timing
- Individual control over start/end times
- Independent positioning, scaling, and effects per video
- Smooth transitions between video segments

### 3. Animation Support
Each video layer supports keyframe animations:
- **Opacity**: Fade in/out effects
- **Scale**: Zoom in/out animations
- **Position**: Pan and slide movements
- **Rotation**: Subtle rotation effects

### 4. Professional Transitions
Automatic or custom transitions between videos:
- **Fade**: Classic fade in/out
- **Scale**: Zoom transitions
- **Position**: Slide transitions
- **Combined**: Multiple animation properties

## JSON Configuration Format

```json
{
  "composition": {
    "resolution": [1080, 1920],
    "duration": 30.0,
    "fps": 30,
    "background_color": [0, 0, 0]
  },
  "layers": [
    {
      "type": "video",
      "source": "/path/to/video1.mp4",
      "name": "intro_video",
      "start_time": 0.0,
      "end_time": 5.0,
      "position": [540, 960],
      "scale": 1.0,
      "opacity": 1.0,
      "animations": {
        "opacity": {
          "keyframes": [0.0, 0.5, 4.5, 5.0],
          "values": [0.0, 1.0, 1.0, 0.0],
          "easings": ["ease_out", "linear", "ease_in"]
        }
      }
    },
    {
      "type": "video",
      "source": "/path/to/video2.mp4",
      "name": "main_content",
      "start_time": 5.0,
      "end_time": 15.0,
      "position": [540, 960],
      "scale": 1.0,
      "opacity": 1.0,
      "animations": {
        "scale": {
          "keyframes": [0.0, 0.5],
          "values": [1.2, 1.0],
          "easings": ["ease_out"]
        }
      }
    }
  ],
  "audio": {
    "narration": {
      "source": "narration.mp3",
      "offset": 0.0,
      "level": 0.0
    }
  },
  "subtitles": {
    "parakeet_data": "transcription.json",
    "style": "glow_caption"
  }
}
```

## Video Layer Parameters

### Required Parameters
- `type`: Must be "video"
- `source`: Path to the video file
- `start_time`: When to show the video (seconds)
- `end_time`: When to hide the video (seconds)

### Optional Parameters
- `name`: Unique identifier for the layer
- `position`: [x, y] position (default: [540, 960] for centered)
- `scale`: Scale factor (default: 1.0, applied after auto-scaling)
- `rotation`: Rotation in degrees (default: 0.0)
- `opacity`: Transparency 0.0-1.0 (default: 1.0)
- `trim_start`: Start time within the source video (default: 0.0)
- `trim_end`: End time within the source video (default: full video)
- `animations`: Keyframe animations (see below)

## Animation System

### Opacity Animation (Fade Effects)
```json
"animations": {
  "opacity": {
    "keyframes": [0.0, 0.5, 4.5, 5.0],
    "values": [0.0, 1.0, 1.0, 0.0],
    "easings": ["ease_out", "linear", "ease_in"]
  }
}
```

### Scale Animation (Zoom Effects)
```json
"animations": {
  "scale": {
    "keyframes": [0.0, 2.0],
    "values": [1.0, 1.2],
    "easings": ["ease_in_out"]
  }
}
```

### Position Animation (Pan/Slide Effects)
```json
"animations": {
  "position": {
    "keyframes": [0.0, 3.0],
    "values": [[540, 1020], [540, 960]],
    "easings": ["ease_out"]
  }
}
```

### Rotation Animation
```json
"animations": {
  "rotation": {
    "keyframes": [0.0, 5.0],
    "values": [0.0, 5.0],
    "easings": ["ease_in_out"]
  }
}
```

## Available Easing Functions

- `linear` - Constant speed
- `ease_in`, `ease_out`, `ease_in_out` - Basic easing
- `ease_in2` to `ease_in5` - Stronger ease in
- `ease_out2` to `ease_out5` - Stronger ease out
- `ease_in_out2` to `ease_in_out5` - Stronger ease in/out

## Usage Examples

### Basic Video Sequence
```bash
python3 dynamic_video_editor.py --config video_sequence.json --output video_compilation.mp4
```

### With Platform Optimization
```bash
python3 dynamic_video_editor.py --config video_sequence.json --platform instagram --quality high --output instagram_video.mp4
```

### Mixed Media (Videos + Images)
You can combine video layers with image sequences in the same composition:

```json
{
  "layers": [
    {
      "type": "video",
      "source": "intro.mp4",
      "start_time": 0.0,
      "end_time": 5.0
    }
  ],
  "image_sequence": [
    {
      "source": "image1.jpg",
      "start_time": 5.0,
      "end_time": 8.0
    }
  ]
}
```

## Aspect Ratio Handling

### Automatic Scaling Examples

**Landscape Video (16:9) → Instagram (9:16)**:
- Original: 1920x1080 (aspect: 1.778)
- Target: 1080x1920 (aspect: 0.562)
- Auto-scale: 1.778x (covers full height, crops sides)

**Square Video (1:1) → Instagram (9:16)**:
- Original: 1080x1080 (aspect: 1.000)
- Target: 1080x1920 (aspect: 0.562)
- Auto-scale: 1.778x (covers full width, crops top/bottom)

**Vertical Video (9:16) → Instagram (9:16)**:
- Original: 1080x1920 (aspect: 0.562)
- Target: 1080x1920 (aspect: 0.562)
- Auto-scale: 1.0x (perfect fit, no cropping)

## Best Practices

### 1. Video Preparation
- Use high-quality source videos
- Consider the target aspect ratio when filming
- Ensure important content is in the center for auto-cropping

### 2. Timing Considerations
- Allow smooth transitions between video segments
- Sync video changes with audio beats or narration
- Use fade effects for professional transitions

### 3. Performance Tips
- Use appropriate video resolutions for target platform
- Limit the number of simultaneous video layers
- Consider video compression before processing

### 4. Animation Guidelines
- Use subtle animations to avoid motion sickness
- Combine opacity and scale for smooth transitions
- Keep rotation effects minimal (under 5 degrees)

## Integration with VinVideo Agents

The editing agent can dynamically create video sequences by:

1. **Content Analysis**: Analyzing video content and duration
2. **Smart Timing**: Matching video segments to narration timing
3. **Transition Selection**: Choosing appropriate transitions between clips
4. **Effect Application**: Adding suitable animations based on content

Example agent workflow:
```python
# Agent determines video sequence based on script timing
video_sequence = [
    {
        "source": select_intro_video(),
        "start_time": 0.0,
        "end_time": get_sentence_end_time(0),
        "animation": "fade_in"
    },
    {
        "source": select_content_video(topic="main_point"),
        "start_time": get_sentence_end_time(0),
        "end_time": get_sentence_end_time(3),
        "animation": "zoom_in"
    }
]
```

## Troubleshooting

### Videos Not Displaying
- Verify video file paths are absolute and correct
- Check video format compatibility (MP4, MOV, AVI)
- Ensure start_time < end_time

### Scaling Issues
- Videos automatically scale to cover full screen
- Use `scale: 1.0` to rely on auto-scaling
- Manual scaling applies on top of auto-scaling

### Performance Issues
- Reduce video resolution and bitrate
- Limit simultaneous video layers
- Use shorter video segments for testing

### Animation Conflicts
- Only one animation per property per layer
- Later animations override earlier ones
- Use different properties for complex effects