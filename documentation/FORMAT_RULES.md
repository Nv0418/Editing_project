# Movis Format Rules & Available Features Guide

## 📋 Overview
This document defines the exact format and capabilities that Movis accepts for video editing operations. Use this as the authoritative reference for generating edit plans that the AI editor agent can execute.

## 🎯 Target Output Specifications
- **Duration**: 10.0 seconds (fixed)
- **Resolution**: 1080x1920 (TikTok vertical format)
- **Frame Rate**: 30 FPS
- **Video Codec**: H.264 (libx264)
- **Audio Codec**: AAC
- **Container**: MP4

## 📝 JSON Edit Plan Schema

### Root Structure
```json
{
  "scene_id": "string",
  "target_format": "tiktok",
  "resolution": [1080, 1920],
  "duration": 10.0,
  "instructions": [...],
  "metadata": {...}
}
```

### Video Instruction Format
```json
{
  "type": "video",
  "asset_id": "VIDEO-XXX",
  "start_time": 0.0,
  "duration": 3.33,
  "position": [540, 960],
  "scale": [1.0, 1.0],
  "opacity": 1.0,
  "properties": {
    "source_file": "/path/to/video.mp4",
    "source_start": 0.0,
    "source_end_trim": 1.0
  },
  "animations": [...]
}
```

### Audio Instruction Format
```json
{
  "type": "audio",
  "asset_id": "AUDIO-XXX", 
  "start_time": 0.0,
  "duration": 10.0,
  "properties": {
    "source_file": "/path/to/audio.mp3",
    "volume_db": -6
  },
  "animations": []
}
```

## 🎭 Available Transition Types

### 1. Hard Cuts
- **Description**: Instant transitions with no effects
- **Implementation**: No animations array
- **Use Case**: High energy, dramatic, action sequences
```json
"animations": []
```

### 2. Cross-Fade with Black
- **Description**: Fade to black, then fade from black
- **Implementation**: Single opacity animation per segment
- **Use Case**: Professional, clean transitions
```json
"animations": [
  {
    "attribute": "opacity",
    "keyframes": [0.0, 0.3, 2.7, 3.0],
    "values": [0.0, 1.0, 1.0, 0.0],
    "easings": ["ease_in", "linear", "ease_out"]
  }
]
```

### 3. True Cross-Fade (Recommended)
- **Description**: Direct video-to-video blending without black screens
- **Implementation**: Overlapping segments with different opacity patterns
- **Use Case**: Cinematic, smooth, premium feel

**First Video (Fade Out)**:
```json
"animations": [
  {
    "attribute": "opacity",
    "keyframes": [0.0, 3.0, 3.5],
    "values": [1.0, 1.0, 0.0],
    "easings": ["linear", "ease_out"]
  }
]
```

**Middle Video (Fade In/Out)**:
```json
"animations": [
  {
    "attribute": "opacity", 
    "keyframes": [0.0, 0.5, 3.5, 4.0],
    "values": [0.0, 1.0, 1.0, 0.0],
    "easings": ["ease_in", "linear", "ease_out"]
  }
]
```

**Last Video (Fade In)**:
```json
"animations": [
  {
    "attribute": "opacity",
    "keyframes": [0.0, 0.5, 3.5],
    "values": [0.0, 1.0, 1.0],
    "easings": ["ease_in", "linear"]
  }
]
```

## ⏱️ Timing Patterns

### Equal Segments (Simple)
- **3 Videos**: 3.33 seconds each
- **Segments**: [0-3.33], [3.33-6.67], [6.67-10.0]
- **Use Case**: Balanced, predictable pacing

### Overlapping Segments (True Cross-Fade)
- **Base Duration**: 3.0 seconds each
- **Overlap**: 0.5 seconds between transitions
- **Segments**: [0-3.5], [3.0-7.0], [6.5-10.0]
- **Use Case**: Seamless, cinematic flow

### Asset-Optimized Segments
- **Logic**: Distribute segments based on available asset count
- **Max Segments**: 2 × number_of_assets
- **Min Duration**: 1.0 second per segment
- **Use Case**: When you have many videos but want meaningful screen time

## 🎨 Available Effects & Properties

### Video Properties
- **position**: [x, y] coordinates (center: [540, 960])
- **scale**: [width_scale, height_scale] (normal: [1.0, 1.0])
- **opacity**: 0.0 to 1.0 (transparent to opaque)
- **source_start**: Start time in source video (seconds)
- **source_end_trim**: Seconds to trim from end of source

### Audio Properties
- **volume_db**: Volume in decibels (recommended: -6)
- **sync_strategy**: "beat_heavy" | "ambient" | "dialogue_focused"

### Animation Easings
- **"linear"**: Constant rate of change
- **"ease_in"**: Slow start, fast finish
- **"ease_out"**: Fast start, slow finish
- **"ease_in_out"**: Slow start and finish

## 🎵 Music Sync Capabilities

### Beat Detection Results
- **Current Song**: "Sad Emotional Piano Music - Background Music (HD).mp3"
- **BPM**: 69.8
- **Beat Count**: 11 beats in 10 seconds
- **Beat Times**: [0.998, 1.881, 2.740, 3.599, 4.481, 5.341, 6.200, 7.082, 7.964, 8.824, 9.706]

### Sync Strategies
1. **Beat-Heavy**: Align cuts with beat times
2. **Ambient**: Ignore beats, focus on musical flow
3. **Custom**: User-defined timing based on musical elements

## 📏 Asset Constraints

### Video Assets
- **Required Count**: 3 videos minimum
- **Supported Formats**: .mp4, .mov, .avi
- **Auto-Trimming**: 1 second removed from end of each video
- **Positioning**: All videos centered at [540, 960]

### Audio Assets  
- **Required Count**: 1 background music file
- **Supported Formats**: .mp3, .wav, .m4a
- **Volume**: Automatically set to -6dB
- **Duration**: Must cover full 10-second timeline

## 🚀 Performance Guidelines

### Segment Duration Rules
- **Minimum Duration**: 1.0 seconds (for readability)
- **Maximum Segments**: 6 (to avoid rapid-fire cuts)
- **Recommended Range**: 2-4 seconds per segment
- **Overlap Range**: 0.3-0.5 seconds for cross-fades

### File Size Optimization
- **Target Size**: 3-4MB for 10-second videos
- **Bitrate**: 3000k video, standard AAC audio
- **Compression**: H.264 with medium preset
- **Platform**: Optimized for TikTok specifications

## 🎬 Style Presets

### Dramatic/Action
```json
{
  "pacing": "fast",
  "segment_duration": [1.0, 2.0],
  "transitions": ["hard_cut"],
  "effects": ["high_contrast"],
  "music_sync": "beat_heavy"
}
```

### Cinematic/Professional
```json
{
  "pacing": "medium",
  "segment_duration": [2.0, 4.0], 
  "transitions": ["true_crossfade"],
  "effects": ["smooth_blending"],
  "music_sync": "ambient"
}
```

### Chill/Relaxed
```json
{
  "pacing": "slow",
  "segment_duration": [3.0, 5.0],
  "transitions": ["crossfade_with_black"],
  "effects": ["soft_transitions"],
  "music_sync": "ambient"
}
```

## ⚠️ Critical Constraints

### Mandatory Requirements
1. **Total Duration**: Must be exactly 10.0 seconds
2. **Resolution**: Must be 1080x1920 (TikTok format)
3. **Asset Count**: Exactly 3 videos + 1 audio file
4. **File Trimming**: Always trim 1 second from end of source videos
5. **Audio Volume**: Always set to -6dB

### Technical Limitations
- **No external assets**: All files must be in local project directory
- **No real-time effects**: Only opacity animations supported
- **Fixed positioning**: All videos centered, no dynamic movement
- **Single audio track**: Only one background music file
- **Linear timeline**: No complex layering or branching

## 🔧 Movis API Integration

### Asset Registration Pattern
```python
registry = mv.vinvideo.AssetRegistry(Path("beat_sync_assets.json"))
asset_id = registry.register_asset(
    file_path=source_file,
    asset_type="video",
    original_prompt="Description",
    generator_model="user_provided"
)
```

### Composition Creation Pattern
```python
composition = mv.vinvideo.VinVideoComposition(
    size=(1080, 1920),
    duration=10.0,
    scene_id="beat_sync_test",
    target_format="tiktok"
)
```

### Layer Addition Pattern
```python
video_layer = mv.layer.Video(asset_path, audio=False)
item = composition.add_layer(
    video_layer,
    offset=start_time,
    position=(540, 960)
)
```

## 📊 Success Metrics

### Quality Indicators
- **File Size**: 3-4MB (optimal)
- **Visual Quality**: No pixelation or artifacts
- **Audio Quality**: Clear, balanced at -6dB
- **Transition Smoothness**: No jarring cuts or black flashes
- **Timeline Coverage**: 100% coverage of 10-second duration

### User Experience Goals
- **First 3 seconds**: Hook the viewer immediately
- **Pacing**: Match the energy of background music
- **Flow**: Seamless progression between videos
- **Platform Readiness**: TikTok-optimized output

---
*This document serves as the complete specification for AI editor agents*
*Last Updated: 2025-05-23 23:05 PST*