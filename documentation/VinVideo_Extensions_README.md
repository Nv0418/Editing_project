# VinVideo Extensions for Movis

This document describes the VinVideo-specific extensions added to the Movis library for automated video editing driven by AI agents.

## Overview

The VinVideo extensions enable seamless integration between AI agents (Director, DoP, QA) and the Movis video editing library. Key features include:

- **AI Agent Connector**: Translates JSON edit plans from AI agents into executable Movis code
- **Asset Registry**: Tracks all generated assets with regeneration capabilities
- **Quality Control Integration**: Multi-tier QC pipeline with <0.25s latency target
- **Social Media Optimization**: Platform-specific export settings for TikTok, Instagram, etc.
- **Smart Transitions**: AI-selectable transitions based on content analysis

## Quick Start

```python
import movis as mv
from movis.vinvideo import EditPlanParser, AssetRegistry, QCPipeline

# Initialize components
asset_registry = AssetRegistry()
qc_pipeline = QCPipeline()
parser = EditPlanParser(asset_registry)

# Register assets (normally done by generation pipeline)
video_id = asset_registry.register_asset(
    file_path="generated_video.mp4",
    asset_type="video",
    original_prompt="Mountain landscape with flowing water",
    generator_model="wan_ltx",
    generation_params={"seed": 42}
)

# Parse AI agent edit plan
edit_plan = parser.parse_json_plan("edit_plan.json")

# Create composition
composition = parser.execute_plan(edit_plan)

# Export for platform
result = composition.export_for_platform("output.mp4")
```

## Edit Plan JSON Schema

AI agents should generate edit plans in this format:

```json
{
  "scene_id": "scene_001",
  "target_format": "tiktok",
  "resolution": [1080, 1920],
  "duration": 15.0,
  "instructions": [
    {
      "type": "video",
      "asset_id": "VID-abc123",
      "start_time": 0.0,
      "duration": 10.0,
      "position": [540, 960],
      "scale": [1.0, 1.0],
      "opacity": 1.0,
      "properties": {},
      "animations": [
        {
          "attribute": "scale",
          "keyframes": [0.0, 10.0],
          "values": [[1.0, 1.0], [1.1, 1.1]],
          "easings": ["ease_in_out"]
        }
      ]
    }
  ]
}
```

## Supported Instruction Types

- **video**: Video clips from WAN LTx, etc.
- **image**: Still images from Flux, etc.
- **text**: Overlay text with full typography control
- **shape**: Geometric shapes (rectangles, ellipses)
- **audio**: Audio tracks and narration

## Quality Control Integration

The QC pipeline implements the multi-tier approach from your research:

### Tier 1 (Fast, <50ms)
- BRISQUE-style image quality analysis
- Basic temporal consistency checks
- Frame sampling with MGSampler concept

### Tier 2 (Detailed, <200ms)
- GHVQ metric for human-centric content
- CLIP-based temporal coherence analysis
- Optical flow motion artifact detection

```python
# QC example
qc_result = qc_pipeline.analyze_video_segment(
    video_path="segment.mp4",
    original_prompt="Person walking in park",
    fast_mode=True
)

if not qc_result.passed:
    # Trigger regeneration
    asset_registry.flag_asset_for_regeneration(
        asset_id, reason=qc_result.recommendation
    )
```

## Platform Optimization

Built-in support for social media platforms:

```python
# TikTok optimization
composition.target_format = "tiktok"
result = composition.export_for_platform("tiktok_video.mp4")

# Instagram Reels
composition.target_format = "instagram_reel"
result = composition.export_for_platform("insta_reel.mp4")
```

### Supported Platforms
- TikTok (1080x1920, 60s max)
- Instagram Reels (1080x1920, 90s max)
- YouTube Shorts (1080x1920, 60s max)
- Instagram Stories (1080x1920, 15s max)

## Asset Registry

Tracks all generated assets for regeneration:

```python
# Register new asset
asset_id = registry.register_asset(
    file_path="video.mp4",
    asset_type="video",
    original_prompt="Sunset over ocean",
    generator_model="wan_ltx",
    generation_params={"seed": 42, "steps": 20}
)

# Flag for regeneration
registry.flag_asset_for_regeneration(asset_id, "quality_issue")

# Get regeneration candidates
flagged_assets = registry.get_flagged_assets()
```

## Integration with VinVideo Pipeline

The extensions integrate seamlessly with your existing VinVideo architecture:

1. **Director Agent** → Generates edit plan JSON
2. **EditPlanParser** → Converts to Movis composition
3. **QC Pipeline** → Validates video segments
4. **Asset Registry** → Manages regeneration loops
5. **Platform Optimizer** → Exports for social media

## Performance Targets

Based on your research requirements:

- **Tier 1 QC**: <50ms per 60-second video
- **Tier 2 QC**: <200ms per 60-second video
- **Total Pipeline**: <0.25s latency target
- **Hardware**: Optimized for NVIDIA H100 GPUs

## Next Steps

1. Replace mock QC implementations with actual methods from your research
2. Integrate with your WAN LTx and Flux generation pipeline
3. Connect to your agent orchestration system
4. Add more sophisticated transition selection algorithms
5. Implement GPU-accelerated optical flow analysis

## File Structure

```
movis/movis/vinvideo/
├── __init__.py              # Module exports
├── agent_connector.py       # AI agent → Movis translation
├── asset_registry.py        # Asset tracking and regeneration
├── social_formats.py        # Platform-specific optimization
├── qc_integration.py        # Quality control pipeline
└── transitions.py           # Smart transition selection
```

This framework provides the foundation for fully automated video editing driven by your AI agents while maintaining the quality standards needed for social media content.
