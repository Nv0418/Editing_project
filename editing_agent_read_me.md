# VinVideo Editing Agent

## Overview

The Editing Agent is the creative intelligence core of the VinVideo pipeline. It receives structured outputs from the Director, Producer, and Prompt Engineer agents, then generates professional JSON editing plans that leverage the existing Movis-based video rendering system.

## Architecture

### Core Components

```
Agent Inputs → Input Parsers → Creative Decision Engine → Timeline Composer → JSON Generator → dynamic_video_editor.py
     ↓              ↓                    ↓                     ↓              ↓
  Producer      Beat Alignment      Style Profiles       Timing Logic    Compatible
  Director      Scene Context       Genre Rules          Transitions     Editing Plans
  PromptEng     Content Analysis    Creative Logic       Effects
```

### Input Data Flow

1. **Producer Agent Output**: Timeline structure, shot count, clip durations per beat
2. **Director Agent Output**: Overall vision, tone, storytelling approach
3. **Prompt Engineer Output**: Scene context, image/video prompt details for each beat

### Beat Alignment System

- Video clips labeled as `beat_01.mp4`, `beat_02.mp4`, etc.
- Consistent beat numbering across all agent outputs
- Semantic mapping of beat number → content understanding

### Creative Decision Engine

- **Genre-aware editing**: Different rules for documentary, storytelling, action, etc.
- **Contextual decisions**: Action vs. dialogue scene handling
- **Style profiles**: Energetic, calm, cinematic editing personalities
- **Human-like intelligence**: Contextual rather than mechanical editing

## Implementation Plan

### Phase 1: Core Infrastructure
- Base agent classes and input validation
- Agent output parsers for structured data ingestion
- Beat alignment and content mapping system

### Phase 2: Creative Intelligence
- Genre-specific editing rule systems
- Style profile implementations
- Scene type detection and handling logic

### Phase 3: Timeline Generation
- Beat-to-timeline conversion algorithms
- Transition selection and effect application
- JSON editing plan generation

### Phase 4: Integration & Testing
- Compatibility validation with dynamic_video_editor.py
- Mock agent output testing framework
- Performance optimization and error handling