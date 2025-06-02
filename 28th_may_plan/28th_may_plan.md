# VinVideo MVP Editing Pipeline Development Plan
**Updated: May 28, 2025 (15-Day Sprint)**

## Executive Summary
This plan outlines the development strategy for VinVideo's MVP editing pipeline using the Movis library. The MVP will provide essential editing capabilities while maintaining constraints that prioritize simplicity and rapid development.

## Current State Analysis
Based on the codebase review:
- **Movis Integration**: Core library is integrated with initial VinVideo-specific modules
- **Subtitle System**: Dynamic karaoke system exists with JSON-based style definitions
- **Asset Management**: Basic registry system for tracking generated assets
- **Transition Framework**: Registry-based transition system (needs population)
- **Social Format Support**: Platform-specific export settings implemented
- **Audio Processing**: Parakeet integration for word-level timestamps

## Architecture Overview

### 1. Frontend Architecture
```
┌─────────────────────────────────────────────┐
│               VinVideo Frontend              │
├─────────────────────────────────────────────┤
│  ┌────────────┐  ┌─────────────────────┐   │
│  │ Edit Page  │  │ Preview Component   │   │
│  │            │  │                     │   │
│  │ - Clip     │  │ - Low-res preview  │   │
│  │   List     │  │ - Watermarked      │   │
│  │ - Subtitle │  │ - Real-time       │   │
│  │   Toggle   │  │                     │   │
│  │ - Music    │  └─────────────────────┘   │
│  │   Control  │                             │
│  └────────────┘                             │
└─────────────────────────────────────────────┘
                    ↓ API
┌─────────────────────────────────────────────┐
│            Backend Services                  │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐    │
│  │ Edit API    │  │ Render Engine    │    │
│  │             │  │                  │    │
│  │ - Project   │  │ - Movis Graph    │    │
│  │   State     │  │   Builder        │    │
│  │ - Asset     │  │ - FFmpeg Export  │    │
│  │   Manager   │  │ - Preview Gen    │    │
│  └─────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────┘
```

```plaintext
┌─────────────────────────────────────────────┐
│               VinVideo Frontend              │
├─────────────────────────────────────────────┤
│  ┌────────────┐  ┌─────────────────────┐   │
│  │ Edit Page  │  │ Preview Component   │   │
│  │            │  │                     │   │
│  │ - Clip     │  │ - Low-res preview  │   │
│  │   List     │  │ - Watermarked      │   │
│  │ - Subtitle │  │ - Real-time       │   │
│  │   Toggle   │  │                     │   │
│  │ - Music    │  └─────────────────────┘   │
│  │   Control  │                             │
│  └────────────┘                             │
└─────────────────────────────────────────────┘
                    ↓ API
┌─────────────────────────────────────────────┐
│            Backend Services                  │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐    │
│  │ Edit API    │  │ Render Engine    │    │
│  │             │  │                  │    │
│  │ - Project   │  │ - Movis Graph    │    │
│  │   State     │  │   Builder        │    │
│  │ - Asset     │  │ - FFmpeg Export  │    │
│  │   Manager   │  │ - Preview Gen    │    │
│  └─────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────┘
```

### 2. Data Flow
1. **Input Phase**: AI clips + Parakeet timestamps + Audio → Project State
2. **Edit Phase**: User edits → State updates → Preview generation
3. **Export Phase**: Final render request → Movis graph → FFmpeg → Output URL

## 15-Day Sprint Plan

We will deliver a lean MVP in 15 days by focusing on core features, running frontend and backend work in parallel, and cutting non‑essential scope.

| Days   | Backend                             | Frontend                          |
|--------|-------------------------------------|-----------------------------------|
| 1–3    | ProjectState, AssetRegistry, APIs   | Scaffold Edit Page, API client    |
| 4–6    | GraphBuilder core (clips, subtitles)| Clip list, subtitle toggle UI     |
| 7–9    | Audio layering, FFmpeg export       | Music controls, Regenerate button |
| 10–12  | Preview stub endpoint               | Preview display, download link    |
| 13–14  | Regenerate & smoke-test flows       | UX polish, error handling         |
| 15     | End-to-end tests & deployment       | Final QA & handoff                |

**Key Scope for MVP**  
- Clip sequencing with hard cuts & crossfades  
- Subtitle overlay using NVIDIA Parakeet timestamps  
- Single music layer with change/remove controls  
- Per-clip "Regenerate" prompt integration  
- "Generate Final Video" and replace preview on regen  
- Pseudo real-time preview via API-triggered refresh  
- No drag-and-drop timeline, advanced grading or multi‑track mixing

## Technical Implementation Details

### 1. Movis Graph Construction
```python
def build_edit_graph(project_state):
    composition = mv.Composition(size=(1080, 1920), duration=total_duration)
    
    # Add background
    bg_layer = mv.layer.SolidColor(size=(1080, 1920), color=(0, 0, 0))
    composition.add_layer(bg_layer)
    
    # Add clips with transitions
    for i, clip in enumerate(project_state.clips):
        clip_layer = mv.layer.Video(clip.file_path)
        
        # Apply transition if not first clip
        if i > 0:
            transition = SmartTransition.create(
                type=project_state.transition_type,
                duration=1.0
            )
            transition.apply(prev_layer, clip_layer, composition, offset)
        
        composition.add_layer(clip_layer, offset=clip.start_time)
        prev_layer = clip_layer
    
    # Add subtitles
    subtitle_renderer = SubtitleRenderer(project_state.subtitle_config)
    subtitle_layers = subtitle_renderer.create_layers(
        project_state.word_timestamps
    )
    for layer in subtitle_layers:
        composition.add_layer(layer)
    
    # Add audio
    audio_layer = mv.layer.Audio(project_state.audio_track.file_path)
    composition.add_layer(audio_layer)
    
    if project_state.music_track:
        music_layer = mv.layer.Audio(
            project_state.music_track.file_path,
            volume=0.3  # Background music volume
        )
        composition.add_layer(music_layer)
    
    return composition
```

### 2. Frontend State Management
```javascript
// EditPageState.js
const EditPageState = {
  project: {
    id: string,
    clips: Clip[],
    audioTrack: AudioTrack,
    subtitleConfig: SubtitleConfig,
    musicTrack: MusicTrack | null,
  },
  ui: {
    selectedClipIndex: number | null,
    previewLoading: boolean,
    renderProgress: number,
  },
  actions: {
    reorderClips: (fromIndex, toIndex) => {},
    regenerateClip: (clipIndex, newPrompt) => {},
    toggleSubtitles: () => {},
    changeMusic: (musicId) => {},
    removeMusic: () => {},
  }
}
```

### 3. API Endpoints Implementation
```python
# vinvideo/api/editing.py
@app.post("/api/v1/preview")
async def generate_preview(project_id: str, settings: PreviewSettings):
    # Build low-res composition
    composition = build_edit_graph(get_project_state(project_id))
    
    # Apply preview settings
    preview_comp = composition.resize((480, 854))
    preview_comp.add_layer(WatermarkLayer())
    
    # Render to temp file
    output_path = f"/tmp/preview_{project_id}_{timestamp()}.mp4"
    preview_comp.export(output_path, fps=24, codec='libx264')
    
    # Upload to CDN
    preview_url = await upload_to_cdn(output_path)
    
    return {"preview_url": preview_url}
```

## Key Considerations

### 1. Performance Optimizations
- **Lazy Loading**: Load clips on-demand during render
- **Caching**: Cache rendered preview segments
- **Parallel Processing**: Use multiprocessing for render jobs
- **CDN Integration**: Direct upload to CDN for preview/final videos

### 2. Error Handling
- Graceful degradation for missing assets
- Retry mechanism for failed renders
- User-friendly error messages
- Fallback options for corrupted clips

### 3. Scalability Preparations
- Queue-based rendering system
- Horizontal scaling for render workers
- Database optimization for project states
- Asset storage optimization

## Testing Strategy

### 1. Unit Tests
- Graph builder logic
- Transition calculations
- Subtitle timing accuracy
- Asset registry operations

### 2. Integration Tests
- End-to-end render pipeline
- API endpoint responses
- Frontend-backend communication
- Platform-specific exports

### 3. Performance Tests
- Render time benchmarks
- Memory usage profiling
- Concurrent render handling
- Large project handling

## Next Steps
1. **Immediate (Today)**: Set up project structure and database schema
2. **Next Days**: Begin GraphBuilder implementation and frontend scaffolding as per the 15-day sprint plan above
3. **Sprint Duration**: Complete MVP features and testing within the 15-day timeline
4. **Post-Sprint**: Deployment and handoff for initial user testing and feedback

## Success Metrics
- Preview generation < 5 seconds for 30-second video
- Final render < 30 seconds for 30-second video
- Zero failed renders due to system errors
- Support for all major social platforms
- Intuitive UI requiring < 5 clicks for common tasks

## Infrastructure & Technical Implementation

### 6. Movis Graph Construction (Detailed)
```python
def build_edit_graph(project_state):
    composition = mv.Composition(size=(1080, 1920), duration=total_duration)
    # Add background
    bg_layer = mv.layer.SolidColor(size=(1080, 1920), color=(0, 0, 0))
    composition.add_layer(bg_layer)
    # Add clips with transitions
    for i, clip in enumerate(project_state.clips):
        clip_layer = mv.layer.Video(clip.file_path)
        if i > 0:
            transition = SmartTransition.create(
                type=project_state.transition_type,
                duration=1.0
            )
            transition.apply(prev_layer, clip_layer, composition, offset)
        composition.add_layer(clip_layer, offset=clip.start_time)
        prev_layer = clip_layer
    # Add subtitles
    subtitle_renderer = SubtitleRenderer(project_state.subtitle_config)
    subtitle_layers = subtitle_renderer.create_layers(
        project_state.word_timestamps
    )
    for layer in subtitle_layers:
        composition.add_layer(layer)
    # Add audio
    audio_layer = mv.layer.Audio(project_state.audio_track.file_path)
    composition.add_layer(audio_layer)
    if project_state.music_track:
        music_layer = mv.layer.Audio(
            project_state.music_track.file_path,
            volume=0.3  # Background music volume
        )
        composition.add_layer(music_layer)
    return composition
```
### 7. Frontend State Management (Detailed)
```javascript
// EditPageState.js
const EditPageState = {
  project: {
    id: string,
    clips: Clip[],
    audioTrack: AudioTrack,
    subtitleConfig: SubtitleConfig,
    musicTrack: MusicTrack | null,
  },
  ui: {
    selectedClipIndex: number | null,
    previewLoading: boolean,
    renderProgress: number,
  },
  actions: {
    reorderClips: (fromIndex, toIndex) => {},
    regenerateClip: (clipIndex, newPrompt) => {},
    toggleSubtitles: () => {},
    changeMusic: (musicId) => {},
    removeMusic: () => {},
  }
}
```
### 8. API Endpoints Implementation (Detailed)
```python
# vinvideo/api/editing.py
@app.post("/api/v1/render")
async def start_render(project_id: str, settings: RenderSettings):
    job = enqueue_render_job(project_id, settings)
    return {"job_id": job.id}

@app.get("/api/v1/render/{job_id}")
async def render_status(job_id: str):
    status = get_job_status(job_id)
    return {"status": status, "video_url": status.completed and get_output_url(job_id)}
```