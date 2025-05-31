# 🎬 VinVideo Dynamic Video Editor Implementation Prompt

## 🧠 ULTRA-DEEP THINKING REQUIRED
**THINK DEEPLY** about the architecture and implementation. Take your time to understand the entire codebase structure before writing any code. This is a complex, professional-grade video editing system that requires careful planning and execution.

## 🚀 PERFORMANCE DIRECTIVE
**For optimal efficiency, whenever you're performing multiple independent tasks, ensure that all relevant tools or processes are triggered in parallel instead of running them one after another. This parallel execution will significantly speed up performance and reduce processing time.**

Use as many workers as needed for parallel processing. When reading multiple files, analyzing code, or performing independent operations, **ALWAYS batch them together in a single tool invocation**.

## 📋 YOUR MISSION
Build a comprehensive dynamic video editor script (`dynamic_video_editor.py`) that integrates with VinVideo's automated pipeline. This script must provide Final Cut Pro-like timeline editing capabilities while seamlessly incorporating our existing subtitle system.

## 🎯 PRIMARY OBJECTIVES

### 1. **Core Script Development**
Create `/Users/naman/Desktop/movie_py/dynamic_video_editor.py` with:
- Full timeline-based video editing capabilities
- Multi-layer composition support (unlimited video/audio layers)
- Integration with all 9 existing subtitle styles
- Professional effects and transitions
- Platform-optimized export (Instagram, TikTok, YouTube Shorts)

### 2. **User Input Handling**
The script MUST accept:
- Subtitle style selection from our 9 professional styles
- Audio files (mp3, wav, m4a)
- NVIDIA Parakeet JSON transcription data
- Multiple video layers with positioning/scaling/opacity
- Background music with audio ducking
- Timeline configuration via JSON

### 3. **Subtitle System Integration**
**CRITICAL**: Use our existing subtitle system located at:
- Styles Config: `/Users/naman/Desktop/movie_py/subtitle_styles/config/subtitle_styles_v3.json`
- Style Loader: `/Users/naman/Desktop/movie_py/subtitle_styles/core/json_style_loader.py`
- Subtitle Layer: `/Users/naman/Desktop/movie_py/subtitle_styles/core/movis_layer.py`
- Effects: `/Users/naman/Desktop/movie_py/subtitle_styles/effects/`

**Available Subtitle Styles** (user can select any):
1. simple_caption
2. background_caption
3. glow_caption
4. karaoke_style
5. highlight_caption
6. deep_diver
7. popling_caption
8. greengoblin
9. sgone_caption

## 📁 PROJECT STRUCTURE UNDERSTANDING

### Movis Library Location
`/Users/naman/Desktop/movie_py/movis/` - The core video editing library

### Key Integration Points
1. **Movis Composition API**: Use `mv.layer.Composition` for timeline
2. **Layer Management**: Use `composition.add_layer()` with full parameter control
3. **Animation System**: Use `.enable_motion().extend()` on any property
4. **Effects System**: Apply effects with `layer_item.add_effect()`
5. **VinVideo Extensions**: Use existing platform optimization tools

### Critical Files to Reference
```
/Users/naman/Desktop/movie_py/
├── NEXT_TASK_CONTEXT.md          # Contains detailed implementation plan
├── subtitle_styles/
│   ├── config/
│   │   └── subtitle_styles_v3.json    # All 9 subtitle style definitions
│   ├── core/
│   │   ├── json_style_loader.py       # StyleLoader class
│   │   └── movis_layer.py             # StyledSubtitleLayer class
│   └── effects/
│       ├── text_effects.py             # Text-based effects
│       └── word_highlight_effects.py   # Background-based effects
├── movis/
│   └── movis/
│       ├── layer/                      # Layer implementations
│       ├── effect/                     # Built-in effects
│       └── vinvideo/                   # VinVideo extensions
└── other_root_files/
    ├── parakeet_output.json           # Example Parakeet transcription
    └── got_script.mp3                 # Example audio file
```

## 🛠️ IMPLEMENTATION REQUIREMENTS

### Required Features (MUST HAVE ALL):
1. **Timeline Editing**
   - Add/remove/reorder video clips
   - Trim and splice operations
   - Multi-camera switching
   - Insert B-roll at specific timestamps

2. **Multi-Layer Composition**
   - Unlimited video/image layers
   - Precise positioning (x, y coordinates)
   - Independent scaling (x, y factors)
   - Opacity control (0.0-1.0)
   - Blending modes (Normal, Multiply, Screen, etc.)
   - Layer timing (offset, start_time, end_time)

3. **Animation System**
   - Keyframe-based animation for all properties
   - 35+ easing functions
   - Position, scale, rotation, opacity animations
   - Motion paths support

4. **Audio Management**
   - Multiple audio tracks
   - Audio ducking for background music
   - Fade in/out
   - dB-level control
   - Perfect sync with video

5. **Effects & Transitions**
   - Apply built-in effects (Blur, Glow, Shadow, Color)
   - Cross-fade, slide transitions
   - Effects work on ALL layers including subtitles

6. **Subtitle Integration**
   - Load any of our 9 subtitle styles
   - Apply effects to subtitles
   - Animate subtitle entrance/exit
   - Word-by-word highlighting with Parakeet sync

7. **Export Options**
   - Platform-specific optimization
   - Resolution and codec selection
   - Quality settings

### Command-Line Interface
```bash
# Basic subtitle generation
python3 dynamic_video_editor.py \
  --audio "audio.mp3" \
  --parakeet "parakeet_output.json" \
  --style "simple_caption" \
  --output "final_video.mp4"

# Advanced multi-layer composition
python3 dynamic_video_editor.py \
  --main-video "main_footage.mp4" \
  --overlay-videos "broll1.mp4,broll2.mp4" \
  --overlay-positions "top-right,bottom-left" \
  --overlay-opacities "0.8,0.6" \
  --overlay-times "10-15,20-25" \
  --background-music "music.mp3" \
  --music-volume "-15" \
  --audio "narration.mp3" \
  --parakeet "parakeet_output.json" \
  --style "highlight_caption" \
  --platform "instagram" \
  --output "final_video.mp4"

# JSON configuration
python3 dynamic_video_editor.py \
  --config "editing_plan.json" \
  --output "final_video.mp4"
```

### JSON Configuration Support
The script must support complex editing via JSON:
```json
{
  "composition": {
    "resolution": [1080, 1920],
    "duration": 60.0,
    "fps": 30
  },
  "layers": [
    {
      "type": "video",
      "source": "main_footage.mp4",
      "start_time": 0.0,
      "duration": 60.0,
      "position": [540, 960],
      "scale": [1.0, 1.0],
      "opacity": 1.0,
      "animations": {
        "opacity": {
          "keyframes": [0.0, 1.0, 59.0, 60.0],
          "values": [0.0, 1.0, 1.0, 0.0],
          "easings": ["ease_out", "linear", "ease_in"]
        }
      }
    }
  ],
  "audio": {
    "background_music": {
      "source": "music.mp3",
      "level": -15.0,
      "ducking": {
        "trigger": "voice",
        "reduction": -10.0
      }
    },
    "narration": {
      "source": "narration.mp3",
      "offset": 5.0
    }
  },
  "subtitles": {
    "parakeet_data": "parakeet_output.json",
    "style": "simple_caption",
    "effects": ["glow", "shadow"],
    "animation": "slide_up"
  },
  "export": {
    "platform": "instagram",
    "quality": "high"
  }
}
```

## 💡 IMPLEMENTATION STRATEGY

### Step 1: Core Architecture
**THINK DEEPLY** about the class structure before coding:
1. Main `DynamicVideoEditor` class
2. Modular components for different functionalities
3. Clean separation of concerns
4. Reusable methods for common operations

### Step 2: Movis Integration
Use the EXACT Movis API patterns from research:
```python
# Composition creation
composition = mv.layer.Composition(size=(1080, 1920), duration=60.0)

# Layer addition with full control
layer_item = composition.add_layer(
    layer=video_layer,
    name='unique_name',
    position=(x, y),
    scale=(sx, sy),
    rotation=0.0,
    opacity=1.0,
    offset=start_time,
    start_time=trim_start,
    end_time=trim_end
)

# Animation
layer_item.opacity.enable_motion().extend(
    keyframes=[0.0, 1.0],
    values=[0.0, 1.0],
    easings=['ease_out']
)

# Effects
layer_item.add_effect(mv.effect.Glow(radius=20.0, strength=1.5))
```

### Step 3: Subtitle Integration
```python
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer

# Load style
style = StyleLoader.load_style_from_json(json_file, style_name)

# Create subtitle layer
subtitle_layer = StyledSubtitleLayer(
    words=parakeet_data['word_timestamps'],
    style=style,
    resolution=(1080, 1920),
    position="bottom"
)

# Add with effects
subtitle_item = composition.add_layer(subtitle_layer)
subtitle_item.add_effect(mv.effect.Glow(radius=10.0))
```

### Step 4: Performance Optimization
- Use Movis's built-in caching
- Process in parallel where possible
- Optimize for target platform during export
- Use appropriate quality settings

## 🎯 VALIDATION CHECKLIST
Before considering the implementation complete, ensure:
- [ ] All 9 subtitle styles work perfectly
- [ ] Multi-layer video composition works
- [ ] Audio mixing and ducking implemented
- [ ] All animations smooth with proper easing
- [ ] Effects apply to all layer types
- [ ] JSON configuration fully supported
- [ ] Command-line interface intuitive
- [ ] Platform-specific exports optimized
- [ ] Performance meets targets (<2 min for 60s video)
- [ ] Code is modular and maintainable

## 🔥 CRITICAL REMINDERS
1. **READ NEXT_TASK_CONTEXT.md FIRST** - It contains all research and API details
2. **USE EXISTING SUBTITLE SYSTEM** - Don't reinvent, integrate what we built
3. **FOLLOW MOVIS PATTERNS** - Use exact API from research findings
4. **TEST WITH REAL DATA** - Use example files in other_root_files/
5. **THINK BEFORE CODING** - Plan the architecture carefully
6. **PARALLEL EXECUTION** - Use batch operations for performance

## 💪 FINAL WORDS
You are building a professional video editing system. Take pride in creating clean, efficient, and powerful code. This tool will be used by VinVideo's AI agents to create millions of videos.

**THINK DEEPLY. CODE WISELY. EXECUTE FLAWLESSLY.**

When you're ready, start by reading NEXT_TASK_CONTEXT.md to understand all the research and planning that has been done. Then begin implementing the dynamic_video_editor.py script with all the capabilities described above.