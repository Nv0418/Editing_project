# VinVideo LLM-Based Editing Pipeline Usage Guide

## Overview

The VinVideo editing pipeline uses an LLM-based Editing Agent (Qwen-3 32B) to transform AI agent outputs into professional videos through intelligent JSON generation and Movis integration.

## Pipeline Components

### 1. **LLM Editing Agent** (Deployed on RunPod)
- **Input**: JSON files from Director, Producer, and Prompt Engineer agents
- **Process**: Advanced AI reasoning for creative editing decisions based on content analysis
- **Output**: Professional JSON editing plan compatible with Movis pipeline

### 2. **Editing Agent to Movis Converter** (`editing_agent_to_movis.py`)
- **Input**: JSON editing plan from LLM Editing Agent
- **Process**: Converts JSON to Movis composition, handles assets, applies effects
- **Output**: Final MP4 video file

### 3. **Full Pipeline Script** (`full_editing_pipeline.py`)
- **Input**: Agent output JSON files
- **Process**: Coordinates LLM agent calls and Movis conversion
- **Output**: Final video with validation and error handling

## Usage Examples

### Production Usage (with real agent outputs)

```bash
# Run complete pipeline with agent JSON files
python3 full_editing_pipeline.py \
  --producer producer_output.json \
  --director director_output.json \
  --prompt-engineer prompt_engineer_output.json \
  --output final_video.mp4
```

### Two-Step Process (for development/debugging)

```bash
# Step 1: Generate editing plan using LLM agent
python3 llm_editing_agent.py \
  --producer producer_output.json \
  --director director_output.json \
  --prompt-engineer prompt_engineer_output.json \
  --output editing_plan.json

# Step 2: Convert to video using Movis
python3 editing_agent_to_movis.py editing_plan.json output_video.mp4
```

### Testing and Validation

```bash
# Validate JSON output format
python3 editing_agent_to_movis.py \
  --validate-only editing_plan.json

# Test with verbose logging
python3 editing_agent_to_movis.py \
  editing_plan.json output.mp4 --verbose

# Test without asset validation (for development)
python3 editing_agent_to_movis.py \
  editing_plan.json output.mp4 --no-validate-assets
```

## Agent Input Format

### Producer Agent Output
```json
{
  "shot_count": 4,
  "total_duration": 20.0,
  "beat_durations": {
    "beat_01": 5.0,
    "beat_02": 5.0,
    "beat_03": 5.0,
    "beat_04": 5.0
  },
  "asset_paths": {
    "beat_01": "/path/to/beat_01.mp4",
    "beat_02": "/path/to/beat_02.mp4",
    "beat_03": "/path/to/beat_03.mp4",
    "beat_04": "/path/to/beat_04.mp4"
  },
  "audio_path": "/path/to/narration.mp3",
  "subtitle_data": "/path/to/parakeet_output.json"
}
```

### Director Agent Output
```json
{
  "genre": "storytelling",
  "tone": "dramatic",
  "pacing": "medium",
  "story_arc": {
    "act1": "setup",
    "act2": "conflict",
    "act3": "climax",
    "act4": "resolution"
  },
  "emotional_beats": {
    "beat_01": "introduction",
    "beat_02": "rising_tension",
    "beat_03": "climax",
    "beat_04": "resolution"
  }
}
```

### Prompt Engineer Agent Output
```json
{
  "beat_contexts": {
    "beat_01": {
      "image_prompt": "A vast medieval castle on a hilltop",
      "video_prompt": "Slow aerial approach to the castle",
      "scene_type": "establishing"
    },
    "beat_02": {
      "image_prompt": "Two characters arguing in chamber",
      "video_prompt": "Quick cuts between characters arguing",
      "scene_type": "dialogue"
    }
  }
}
```

## Generated JSON Output

The Editing Agent generates JSON plans with this structure:

```json
{
  "metadata": {
    "agent_version": "1.0",
    "creation_timestamp": "2025-06-01T21:37:54.779736",
    "editing_style": "cinematic",
    "target_platform": "instagram"
  },
  "composition": {
    "resolution": [1080, 1920],
    "duration": 15.0,
    "fps": 30,
    "background_color": [0, 0, 0]
  },
  "layers": [
    {
      "type": "video",
      "source": "/path/to/beat_01.mp4",
      "name": "layer_beat_01",
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
      },
      "effects": ["glow"]
    }
  ],
  "audio": {
    "narration": {
      "source": "/path/to/audio.mp3",
      "offset": 0.0,
      "level": 0.0
    }
  },
  "subtitles": {
    "parakeet_data": "/path/to/parakeet.json",
    "style": "deep_diver",
    "position": "bottom"
  },
  "export": {
    "platform": "instagram",
    "quality": "high"
  }
}
```

## Creative Intelligence Features

### Editing Style Profiles
- **Energetic**: Fast cuts, dynamic transitions, high effects
- **Calm**: Longer shots, gentle transitions, subtle effects
- **Cinematic**: Balanced pacing, sophisticated transitions
- **Social Media**: Hook-driven, retention-focused editing

### Content Analysis
- **Action Detection**: Analyzes video prompts for movement keywords
- **Dialogue Detection**: Identifies conversation-based scenes
- **Emotional Mapping**: Maps story beats to editing intensity
- **Transition Selection**: Chooses transitions based on content flow

### Beat Alignment System
- **Consistent Numbering**: beat_01, beat_02, etc. across all agents
- **Semantic Understanding**: Links beat number to content meaning
- **Context Preservation**: Maintains scene intent throughout pipeline

## Troubleshooting

### Common Issues

1. **Missing Movis**: The converter requires Movis to be installed
   ```bash
   pip install movis
   ```

2. **Asset Path Issues**: Ensure all video/audio paths in agent outputs are absolute and exist

3. **JSON Validation**: Use the built-in validation to check editing plans
   ```bash
   python3 editing_agent_to_movis.py --no-validate-assets plan.json test.mp4
   ```

### Testing Without Movis

You can test the creative intelligence without Movis:

```bash
# Generate editing plans for analysis
python3 editing_agent.py

# Inspect the generated JSON
cat generated_editing_plan.json | python3 -m json.tool
```

## Integration with Existing Pipeline

The generated JSON is fully compatible with your existing `dynamic_video_editor.py`:

```bash
# Once Movis is available
python3 dynamic_video_editor.py --config generated_editing_plan.json --output final.mp4
```

## Next Steps

1. **Install Movis**: Set up the Movis environment for video generation
2. **Test with Real Assets**: Replace mock paths with actual video files
3. **Agent Integration**: Connect with your actual Director, Producer, and Prompt Engineer agents
4. **Style Customization**: Extend editing profiles for specific content types
5. **Effect Expansion**: Add more visual effects and transitions to the system