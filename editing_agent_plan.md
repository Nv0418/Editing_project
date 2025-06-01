# Editing Agent Pipeline Development Plan

## Executive Summary

This document outlines the comprehensive plan for building the Editing Agent pipeline for the VinVideo project. The Editing Agent will be the central intelligence that receives inputs from Director, DoP, Producer, and Prompt Engineer agents, and outputs structured JSON editing plans that can be executed by the existing Movis-based video rendering pipeline.

## Current Project State

### Completed Components
- **9 Professional Subtitle Styles**: Production-ready with word-by-word highlighting
- **Dynamic Video Editor**: Comprehensive Python script with multi-layer composition
- **Movis Integration**: Full pipeline from JSON to MP4 output
- **Platform Optimization**: Instagram, TikTok, YouTube Shorts support
- **Asset Management**: Registry system for tracking generated assets
- **Transition System**: Framework for custom transitions (ready for implementation)

### Existing Architecture
```
Input → AI Agents → JSON Edit Plan → DynamicVideoEditor → Movis Composition → MP4
         ↓     ↓          ↓                    ↓                   ↓
    Director  DoP    EditPlanParser    Layer Management    Platform Export
    Producer         Asset Registry    Animation System     Quality Control
```

## Editing Agent Requirements

### Input Sources
1. **Director Agent Output**
   - Scene breakdown with timing
   - Narrative structure and pacing
   - Emotional beats and story arc

2. **DoP Agent Output**
   - Visual style preferences
   - Color grading suggestions
   - Camera movement concepts

3. **Producer Agent Output**
   - Available assets (videos, images, audio)
   - Budget constraints (render time, quality)
   - Platform requirements

4. **Prompt Engineer Output**
   - Original user intent
   - Key messaging points
   - Style preferences

### Output Format
The Editing Agent must produce a JSON editing plan compatible with `dynamic_video_editor.py`:

```json
{
  "metadata": {
    "agent_version": "1.0",
    "creation_timestamp": "ISO 8601",
    "editing_style": "dynamic/calm/energetic",
    "target_platform": "instagram/tiktok/youtube_shorts"
  },
  "composition": {
    "resolution": [1080, 1920],
    "duration": 30,
    "fps": 30,
    "background_color": [0, 0, 0]
  },
  "layers": [...],
  "transitions": [...],
  "audio": {...},
  "subtitles": {...},
  "effects": {...}
}
```

## Development Plan

### Phase 1: Core Infrastructure (Days 1-3)

#### 1.1 Create Agent Base Classes
```python
# editing_agent/base.py
class BaseAgent:
    """Base class for all VinVideo agents"""
    def process(self, input_data):
        pass
    
class EditingAgent(BaseAgent):
    """Main editing agent that orchestrates the edit"""
    def __init__(self):
        self.director_parser = DirectorParser()
        self.dop_parser = DoPParser()
        self.producer_parser = ProducerParser()
        self.edit_composer = EditComposer()
```

#### 1.2 Input Parsers
Create parsers for each agent's output:
- `director_parser.py`: Extract scene timing, pacing
- `dop_parser.py`: Extract visual style, mood
- `producer_parser.py`: Extract asset inventory
- `prompt_parser.py`: Extract user intent

#### 1.3 Edit Decision Engine
Core logic for making editing decisions:
- Scene selection based on narrative importance
- Transition selection based on mood/pacing
- Effect application based on style
- Subtitle style selection based on content type

### Phase 2: Edit Composition Logic (Days 4-6)

#### 2.1 Timeline Management
```python
class TimelineManager:
    """Manages the temporal arrangement of clips"""
    def calculate_scene_durations(self, director_data, total_duration):
        # Distribute time based on scene importance
        pass
    
    def apply_pacing_curve(self, timeline, emotional_beats):
        # Adjust timing for dramatic effect
        pass
```

#### 2.2 Visual Style Application
```python
class StyleApplicator:
    """Applies DoP visual preferences to edit"""
    def select_transitions(self, style_preference):
        # Map style to transition types
        pass
    
    def apply_color_grading(self, clips, color_mood):
        # Add color adjustment layers
        pass
```

#### 2.3 Asset Optimization
```python
class AssetOptimizer:
    """Optimizes asset usage based on producer constraints"""
    def select_best_assets(self, available_assets, required_scenes):
        # Quality vs. file size optimization
        pass
    
    def calculate_render_budget(self, edit_plan):
        # Estimate render time/resources
        pass
```

### Phase 3: Advanced Features (Days 7-9)

#### 3.1 Music Synchronization
- Integrate beat detection for cut timing
- Implement audio ducking for narration
- Sync transitions to musical beats

#### 3.2 Motion Design
- Ken Burns effect automation
- Dynamic text animations
- Camera movement simulation

#### 3.3 Platform Adaptation
- Automatic reformatting for different platforms
- Safe zone compliance
- Platform-specific optimizations

### Phase 4: Integration & Testing (Days 10-12)

#### 4.1 Integration Points
- Connect to existing `dynamic_video_editor.py`
- Validate JSON output against schema
- Test with various input combinations

#### 4.2 Performance Optimization
- Parallel processing for decision making
- Caching for repeated edits
- Memory optimization for large projects

#### 4.3 Quality Assurance
- Unit tests for each component
- Integration tests for full pipeline
- Performance benchmarks

## Technical Implementation Details

### Directory Structure
```
editing_agent/
├── __init__.py
├── base.py                 # Base agent classes
├── core/
│   ├── __init__.py
│   ├── editing_agent.py    # Main agent
│   ├── timeline_manager.py # Timeline logic
│   ├── style_applicator.py # Visual styling
│   └── asset_optimizer.py  # Asset management
├── parsers/
│   ├── __init__.py
│   ├── director_parser.py
│   ├── dop_parser.py
│   ├── producer_parser.py
│   └── prompt_parser.py
├── composers/
│   ├── __init__.py
│   ├── edit_composer.py    # JSON generation
│   ├── transition_selector.py
│   └── effect_selector.py
├── utils/
│   ├── __init__.py
│   ├── validators.py       # Input/output validation
│   └── constants.py        # Configuration constants
└── tests/
    ├── __init__.py
    ├── test_editing_agent.py
    └── fixtures/           # Test data
```

### Key Algorithms

#### 1. Scene Duration Allocation
```python
def allocate_scene_durations(scenes, total_duration, importance_weights):
    """
    Allocate duration to scenes based on importance
    Uses golden ratio for aesthetically pleasing proportions
    """
    total_weight = sum(importance_weights)
    base_durations = [
        (weight / total_weight) * total_duration 
        for weight in importance_weights
    ]
    
    # Apply minimum/maximum constraints
    # Adjust for pacing curve
    # Return final durations
```

#### 2. Transition Selection
```python
def select_transition(prev_scene, next_scene, style_preference):
    """
    Select appropriate transition based on:
    - Scene emotional continuity
    - Visual style preference
    - Pacing requirements
    """
    emotional_delta = calculate_emotional_change(prev_scene, next_scene)
    
    if emotional_delta > THRESHOLD:
        return "hard_cut"  # Dramatic change
    elif style_preference == "smooth":
        return "cross_dissolve"
    else:
        return select_from_style_matrix(style_preference)
```

#### 3. Effect Intensity Mapping
```python
def map_effect_intensity(emotional_beat, style_preference):
    """
    Map emotional intensity to visual effect strength
    """
    base_intensity = emotional_beat.intensity * 0.7
    style_modifier = STYLE_INTENSITY_MAP[style_preference]
    
    return clamp(base_intensity * style_modifier, 0.0, 1.0)
```

### Integration with Existing Pipeline

#### 1. Input Interface
```python
# Example usage
editing_agent = EditingAgent()

# Gather inputs from other agents
director_output = director_agent.analyze(script)
dop_output = dop_agent.plan_visuals(script, style_brief)
producer_output = producer_agent.gather_assets(requirements)
prompt_output = prompt_engineer.parse_intent(user_input)

# Generate edit plan
edit_plan = editing_agent.create_edit_plan(
    director_data=director_output,
    dop_data=dop_output,
    producer_data=producer_output,
    prompt_data=prompt_output
)

# Execute with existing pipeline
video_editor = DynamicVideoEditor()
video_editor.from_json(edit_plan)
video_editor.export("output.mp4", platform="instagram")
```

#### 2. Validation Schema
```python
EDIT_PLAN_SCHEMA = {
    "type": "object",
    "required": ["metadata", "composition", "layers"],
    "properties": {
        "metadata": {
            "type": "object",
            "required": ["agent_version", "creation_timestamp"]
        },
        "composition": {
            "type": "object",
            "required": ["resolution", "duration", "fps"]
        },
        "layers": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "source"]
            }
        }
    }
}
```

## Testing Strategy

### Unit Tests
- Test each parser independently
- Validate timeline calculations
- Verify transition selection logic
- Check effect mapping accuracy

### Integration Tests
- Full pipeline from agent inputs to JSON
- Compatibility with `dynamic_video_editor.py`
- Platform-specific exports
- Performance under various loads

### Example Test Cases
1. **Simple Edit**: 3 scenes, basic transitions
2. **Complex Edit**: 10+ scenes, music sync, effects
3. **Platform Variants**: Same content for different platforms
4. **Edge Cases**: Missing assets, conflicting requirements

## Performance Considerations

### Optimization Strategies
1. **Parallel Processing**
   - Parse multiple agent inputs concurrently
   - Generate layer configurations in parallel
   - Pre-compute common transitions

2. **Caching**
   - Cache parsed agent outputs
   - Store computed timelines
   - Reuse effect calculations

3. **Memory Management**
   - Stream large asset metadata
   - Lazy load configuration data
   - Efficient JSON generation

### Benchmarks
- Target: Generate edit plan in < 2 seconds
- Support videos up to 5 minutes
- Handle 100+ individual clips
- Process 4K resolution metadata

## Future Enhancements

### Phase 5: Machine Learning Integration
- Learn editing patterns from successful videos
- Predict optimal cut points
- Style transfer from reference videos

### Phase 6: Real-time Preview
- Generate low-res previews instantly
- Interactive timeline adjustments
- Live effect parameter tuning

### Phase 7: Collaborative Editing
- Multi-agent negotiation for decisions
- Human-in-the-loop refinements
- Version control for edit plans

## Conclusion

The Editing Agent pipeline will serve as the intelligent core of the VinVideo system, transforming high-level creative decisions from multiple AI agents into executable video editing plans. By leveraging the existing Movis integration and building on the established JSON configuration format, we can create a powerful system that maintains both creative flexibility and technical precision.

The modular architecture ensures that each component can be developed, tested, and optimized independently while maintaining seamless integration with the overall pipeline. This approach allows for rapid iteration and continuous improvement as we refine the editing intelligence.

## Next Steps

1. **Immediate**: Set up the `editing_agent/` directory structure
2. **Day 1**: Implement base agent classes and core infrastructure
3. **Day 2-3**: Build input parsers for each agent type
4. **Day 4-6**: Develop edit composition logic
5. **Day 7-9**: Add advanced features (music sync, motion design)
6. **Day 10-12**: Integration testing and optimization
7. **Ongoing**: Iterate based on output quality and user feedback