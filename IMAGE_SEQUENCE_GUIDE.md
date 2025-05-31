# Dynamic Video Editor - Image Sequence Guide

This guide explains how to use the enhanced `dynamic_video_editor.py` to create videos from image sequences with precise timing control, transitions, and effects.

## Key Features

### 1. Intelligent Auto-Scaling
Each image is automatically scaled to properly fill the screen without black borders:
- **Same aspect ratio**: Images with the same aspect ratio as the target (within 1% tolerance) are scaled to fit exactly
- **Different aspect ratio**: Images are scaled to "cover" the entire screen, preventing black borders
- **Manual override**: Use the `scale` parameter to apply additional scaling on top of auto-scaling

### 2. Flexible Image Timing
Each image in the sequence can specify:
- `start_time`: When the image appears in the timeline
- `end_time`: When the image disappears
- Duration is automatically calculated from these values

### 3. Automatic Zoom Transitions
Starting from the second image, a zoom transition is automatically applied to create smooth visual flow. This can be disabled by specifying custom transitions or Ken Burns effects.

### 4. Ken Burns Effects
Add motion to static images with:
- `zoom_in`: Start wide, zoom into the image
- `zoom_out`: Start close, zoom out to reveal more
- `pan`: Move across the image horizontally

### 5. Custom Transitions
Override automatic transitions with:
- `fade`: Classic fade in/out
- `crossfade`: Overlap with previous image
- `zoom_fade`: Zoom while fading (default for 2nd+ images)

## JSON Configuration Format

```json
{
  "composition": {
    "resolution": [1080, 1920],
    "duration": 30.0,
    "fps": 30,
    "background_color": [0, 0, 0]
  },
  "image_sequence": [
    {
      "source": "/path/to/image1.jpg",
      "start_time": 0.0,
      "end_time": 5.0,
      "name": "opening_shot",
      "scale": 1.1,
      "position": [540, 960],
      "ken_burns": {
        "type": "zoom_in",
        "start_scale": 1.0,
        "end_scale": 1.2
      }
    },
    {
      "source": "/path/to/image2.jpg",
      "start_time": 5.0,
      "end_time": 10.0,
      "name": "second_shot"
    },
    {
      "source": "/path/to/image3.jpg",
      "start_time": 10.0,
      "end_time": 15.0,
      "transition": {
        "type": "fade",
        "duration": 1.0
      },
      "ken_burns": {
        "type": "pan",
        "start_position": [480, 960],
        "end_position": [600, 960]
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
    "style": "highlight_caption",
    "position": "bottom"
  }
}
```

## Image Sequence Parameters

### Required Parameters
- `source`: Path to the image file
- `start_time`: When to show the image (seconds)
- `end_time`: When to hide the image (seconds)

### Optional Parameters
- `name`: Unique identifier for the layer
- `scale`: Scale factor (default: 1.0)
- `position`: [x, y] position (default: [540, 960] for centered)
- `opacity`: Transparency 0.0-1.0 (default: 1.0)
- `transition`: Custom transition settings
- `ken_burns`: Motion effect settings
- `animations`: Additional keyframe animations

## Transition Types

### 1. Fade (default for first image)
```json
"transition": {
  "type": "fade",
  "duration": 0.5
}
```

### 2. Zoom Fade (automatic for 2nd+ images)
```json
"transition": {
  "type": "zoom_fade",
  "duration": 0.5,
  "zoom_start": 1.2,
  "zoom_end": 1.0
}
```

### 3. Crossfade
```json
"transition": {
  "type": "crossfade",
  "duration": 0.5
}
```

## Ken Burns Effects

### Zoom In
Gradually zoom into the image for dramatic effect:
```json
"ken_burns": {
  "type": "zoom_in",
  "start_scale": 1.0,
  "end_scale": 1.3
}
```

### Zoom Out
Start close and reveal more of the image:
```json
"ken_burns": {
  "type": "zoom_out",
  "start_scale": 1.4,
  "end_scale": 1.0
}
```

### Pan
Move across the image horizontally:
```json
"ken_burns": {
  "type": "pan",
  "start_position": [400, 960],
  "end_position": [680, 960]
}
```

## Usage Examples

### Basic Image Sequence
```bash
python3 dynamic_video_editor.py --config image_sequence.json --output slideshow.mp4
```

### With Platform Optimization
```bash
python3 dynamic_video_editor.py --config image_sequence.json --platform instagram --quality high --output instagram_slideshow.mp4
```

## Best Practices

### 1. Image Preparation
- Use high-resolution images (at least 1080x1920 for Instagram)
- Pre-crop images to desired aspect ratio
- Optimize file sizes for faster processing

### 2. Timing Considerations
- Allow at least 2-3 seconds per image for viewer comprehension
- Overlap transitions slightly for smooth flow
- Sync image changes with audio beats or narration pauses

### 3. Ken Burns Usage
- Use subtle movements (10-20% scale change)
- Pan slowly to avoid motion sickness
- Alternate between static and moving images

### 4. Performance Tips
- Process images in batches
- Use consistent image dimensions
- Limit total number of images for longer videos

## Integration with VinVideo Agents

The editing agent can dynamically generate image sequences by:
1. Analyzing script content
2. Selecting appropriate images from asset library
3. Timing images to match narration
4. Adding appropriate transitions and effects

Example agent-generated configuration:
```json
{
  "image_sequence": [
    {
      "source": "{{asset_path}}/establishing_shot.jpg",
      "start_time": 0.0,
      "end_time": "{{first_sentence_end}}",
      "ken_burns": {
        "type": "zoom_in",
        "start_scale": 1.0,
        "end_scale": 1.1
      }
    }
  ]
}
```

## Troubleshooting

### Images Not Displaying
- Verify file paths are absolute
- Check image format compatibility (JPEG, PNG)
- Ensure start_time < end_time

### Transition Conflicts
- Ken Burns effects override zoom transitions
- Only one scale animation per image
- Use fade transitions with Ken Burns

### Performance Issues
- Reduce image resolution
- Decrease number of simultaneous layers
- Use lower quality preview for testing