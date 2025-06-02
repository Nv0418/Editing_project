# LLM Editing Agent System Message - Comprehensive Development Plan

## Executive Summary

This document outlines the strategic plan for creating the optimal system message for VinVideo's LLM-based Editing Agent, which will run on Qwen-3 32B FP8. The agent will transform outputs from Director, Producer, and Prompt Engineer agents into intelligent JSON editing plans compatible with the existing Movis-based video generation pipeline.

---

## 🎯 **Deep Context Analysis**

### **VinVideo User Experience Flow**
1. **User Preferences Selection**:
   - Music selection (background music or none)
   - Subtitle preference (enabled/disabled)
   - Subtitle style selection (9 professional options)
   - Video format choice (9:16 short-form vs 16:9 regular)

2. **Content Creation Process**:
   - User provides script or concept idea
   - LLM converts idea to structured script
   - AI agent pipeline executes: Producer → Director → DoP → Image Prompt Engineer → Image Generation → QA → Video Prompt Engineer → Image-to-Video → **Editing Agent**

3. **Final Output**:
   - Platform-optimized video (Instagram/TikTok/YouTube Shorts)
   - Professional subtitle integration with audio sync
   - Intelligent editing decisions based on content analysis

### **AI Agent Pipeline Analysis**

#### **Producer Agent (Input 1)**
- **Function**: Determines precise cut points based on audio timing and script structure
- **Output Format**: JSON array with cut_number, cut_time, and reason
- **Key Data**: 
  ```json
  [
    {"cut_number": 1, "cut_time": 2.48, "reason": "End of opening question"},
    {"cut_number": 2, "cut_time": 6.84, "reason": "End of first factual beat"}
  ]
  ```

#### **Director Agent (Input 2)**
- **Function**: Creative vision, story arc, emotional tone, narrative beats
- **Output Format**: Comprehensive JSON with project metadata and narrative beats
- **Key Data**:
  ```json
  {
    "project_metadata": {
      "target_platform": "instagram",
      "content_type": "educational",
      "primary_concept": "sustainable living tips"
    },
    "narrative_beats": [
      {
        "beat_no": 1,
        "timecode_start": "00:00:00.000",
        "est_duration_s": 4,
        "script_phrase": "Want to live more sustainably?",
        "narrative_function": "hook",
        "emotional_tone": "curiosity",
        "creative_vision": "Close-up of person with questioning expression",
        "audience_retention_strategy": "direct_question",
        "turning_point": false
      }
    ]
  }
  ```

#### **Prompt Engineer Agent (Input 3)**
- **Function**: Provides detailed scene context, image/video prompts for each beat
- **Output Format**: Indexed array of detailed prompts
- **Key Data**:
  ```json
  [
    "1: Jordan, 20s with tousled hair wearing white cotton tee, questioning expression, reaching for reusable water bottle, modern kitchen with natural light, medium shot 50mm, warm morning light, sustainable living aesthetic, 16:9 4K"
  ]
  ```

### **Beat Alignment System**
- **Critical Concept**: All agents use consistent beat numbering (beat_01, beat_02, etc.)
- **Video Assets**: Generated videos saved as `beat_01.mp4`, `beat_02.mp4`, etc.
- **Semantic Mapping**: Beat number → content meaning → editing decisions
- **Duration Control**: Each beat has predetermined duration from Producer Agent

---

## 🎨 **VinVideo Technical Capabilities Analysis**

### **Professional Subtitle System (9 Styles)**

#### **Style Categories & Use Cases**:
1. **simple_caption** - Educational content (Oswald Heavy, size-pulse effect)
2. **background_caption** - News style (Bicyclette Black, dark blue background)
3. **glow_caption** - Gaming/tech (Impact, green glow effects)
4. **karaoke_style** - Music content (Alverata Bold Italic, yellow highlights)
5. **highlight_caption** - Motivational (Mazzard M Bold, purple word backgrounds)
6. **deep_diver** - Contemplative (Publica Sans Round, contrasting text)
7. **popling_caption** - Elegant (underline effects)
8. **greengoblin** - Clean dynamic (no glow effects)
9. **sgone_caption** - Artistic (2-word display, center positioning)

#### **Technical Specifications**:
- **Word-by-Word Sync**: NVIDIA Parakeet integration for precise timing
- **Safe Zone Compliance**: Instagram/TikTok/YouTube Shorts optimization
- **Multi-line Support**: Intelligent text wrapping and positioning
- **Effect Types**: outline, background, text_shadow, dual_glow, word_highlight, deep_diver
- **Animation Types**: size_pulse, color_change, background_highlight, underline

### **Movis Library Capabilities**

#### **Core Architecture**:
- **Compositions**: Primary containers for video scenes (nestable)
- **Layers**: Visual/audio elements (images, videos, audio, text, procedural graphics)
- **Attributes**: Animatable properties (position, scale, opacity, color)
- **Motion & Animation**: 35+ easing functions for keyframe animation
- **Effects**: Visual effects (blur, glow, shadow, color adjustments)

#### **Layer Types Available**:
- **Media Layers**: Image, Video, Audio, ImageSequence, AudioSequence
- **Drawing Layers**: Rectangle, Ellipse, Line, Text
- **Texture Layers**: Gradient, Stripe
- **Special Layers**: AlphaMatte, LuminanceMatte
- **Custom Layers**: Professional subtitle integration

#### **Animation System**:
- **Properties**: position, scale, rotation, opacity, color
- **Easing Functions**: linear, ease_in/out/in_out (variants 1-35)
- **Keyframe System**: Precise time-based control
- **Blending Modes**: Normal, Multiply, Screen, Overlay, etc.

### **Dynamic Video Editor JSON Format**

#### **Complete Structure**:
```json
{
  "metadata": {
    "agent_version": "1.0",
    "creation_timestamp": "ISO 8601",
    "editing_style": "energetic/calm/cinematic",
    "target_platform": "instagram/tiktok/youtube_shorts"
  },
  "composition": {
    "resolution": [1080, 1920],
    "duration": 30.0,
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
  "image_sequence": [
    {
      "source": "/path/to/image.jpg",
      "start_time": 0.0,
      "end_time": 3.0,
      "ken_burns": {
        "type": "zoom_in",
        "start_scale": 1.0,
        "end_scale": 1.15
      }
    }
  ],
  "audio": {
    "background_music": {
      "source": "/path/to/music.mp3",
      "level": -20.0,
      "fade_in": 3.0,
      "fade_out": 3.0,
      "ducking": {
        "trigger": "voice",
        "reduction": -10.0
      }
    },
    "narration": {
      "source": "/path/to/narration.mp3",
      "offset": 0.0,
      "level": 0.0
    }
  },
  "subtitles": {
    "parakeet_data": "/path/to/parakeet_output.json",
    "style": "highlight_caption",
    "position": "bottom"
  },
  "export": {
    "platform": "instagram",
    "quality": "high"
  }
}
```

### **Platform Optimization Specifications**

#### **Instagram/TikTok**:
- Resolution: 1080x1920 (9:16)
- FPS: 30, Codec: H.264, CRF: 23
- Safe zones: Horizontal 100px, Top 220px, Bottom 450px

#### **YouTube Shorts**:
- Resolution: 1080x1920 (9:16)
- FPS: 30, Codec: H.264, CRF: 18
- Higher quality encoding

#### **YouTube Regular**:
- Resolution: 1920x1080 (16:9)
- FPS: 30, Codec: H.264, CRF: 18

---

## 🧠 **Editing Intelligence Requirements**

### **Content Analysis Capabilities**

#### **Scene Type Detection**:
- **Action Scenes**: Fast movements, dynamic camera work
  - Indicators: "running", "fighting", "jumping", "chase", "explosion"
  - Editing Style: Fast cuts, dynamic transitions, high energy
  
- **Dialogue Scenes**: Conversation-focused content
  - Indicators: "talking", "speaking", "conversation", "interview"
  - Editing Style: Longer holds, smoother transitions, focus on speakers

- **Establishing Scenes**: Setting/context introduction
  - Indicators: Wide shots, landscapes, building exteriors
  - Editing Style: Ken Burns effects, slow zooms, extended duration

- **Transition Scenes**: Bridge between main content
  - Indicators: Movement between locations, time passage
  - Editing Style: Quick cuts, slide transitions, medium duration

#### **Emotional Tone Mapping**:
- **High Energy** (wonder, excitement, triumph): Fast cuts, zoom effects, vibrant colors
- **Contemplative** (reflection, learning): Slower pacing, fade transitions, stable shots
- **Dramatic** (tension, conflict, climax): Dynamic movements, quick cuts, strong effects
- **Calm** (peaceful, resolution): Gentle transitions, longer holds, subtle movements

### **Professional Editing Principles**

#### **Pacing Strategies**:
- **Hook Creation** (0-3 seconds): Fast cuts, dynamic openings, immediate engagement
- **Retention Tactics**: Vary shot lengths, strategic reveals, pattern interrupts
- **Emotional Flow**: Build tension → release, question → answer, setup → payoff
- **Platform Optimization**: Instagram/TikTok favor faster pacing than YouTube

#### **Transition Selection Logic**:
```
Emotional Continuity → Same Mood = Smooth Transition (fade, dissolve)
Emotional Shift → Different Mood = Dynamic Transition (cut, zoom, slide)
Action Level Change → High to Low = Dramatic Cut, Low to High = Build-up Transition
Narrative Function → Setup to Conflict = Intensifying, Climax to Resolution = Releasing
```

#### **Effect Application Rules**:
- **Glow Effects**: Gaming, tech, high-energy content
- **Shadow Effects**: Dramatic, serious, professional content
- **Ken Burns**: Static images, establishing shots, contemplative moments
- **Scale Animations**: Emphasis, reveals, dynamic content
- **Position Animations**: Movement simulation, pan effects

---

## 📋 **System Message Architecture Plan**

### **Section 1: Core Identity & Mission**
- Define role as Expert Video Editor AI
- Establish creative intelligence capabilities
- Set professional editing standards
- Emphasize platform optimization expertise

### **Section 2: Input Processing Framework**
- **Producer Agent Data**: Cut timing and structure analysis
- **Director Agent Data**: Creative vision and narrative extraction
- **Prompt Engineer Data**: Scene context and visual content understanding
- **Beat Alignment System**: Semantic mapping and content correlation

### **Section 3: Content Analysis Engine**
- **Scene Type Classification**: Action, dialogue, establishing, transition
- **Emotional Tone Detection**: Energy level, mood, narrative function
- **Visual Content Analysis**: From image/video prompts
- **Audio Synchronization**: Narration timing and music integration

### **Section 4: Editing Decision Matrix**
- **Genre-Based Rules**: Documentary, storytelling, educational, entertainment
- **Platform Considerations**: Instagram vs TikTok vs YouTube Shorts optimization
- **User Preferences**: Music integration, subtitle styling
- **Technical Constraints**: Duration limits, safe zones, aspect ratios

### **Section 5: Movis Capabilities Reference**
- **Complete Layer System**: All available layer types and properties
- **Animation Framework**: 35+ easing functions and keyframe system
- **Effect Catalog**: Blur, glow, shadow, color effects with parameters
- **Audio Management**: Multi-track mixing, ducking, fade controls

### **Section 6: Subtitle System Integration**
- **Style Selection Logic**: Content type → appropriate subtitle style
- **Technical Specifications**: Safe zones, positioning, word sync
- **Effect Parameters**: Font sizes, colors, backgrounds, animations
- **Platform Compliance**: Instagram/TikTok safe area requirements

### **Section 7: JSON Output Schema**
- **Complete Structure Definition**: All required and optional fields
- **Validation Rules**: Data types, ranges, dependencies
- **Example Templates**: Different content types and platforms
- **Error Handling**: Fallback options and graceful degradation

### **Section 8: Quality Assurance Framework**
- **Technical Validation**: JSON syntax, file paths, timing logic
- **Creative Standards**: Professional editing principles
- **Platform Compliance**: Export settings and optimization
- **User Experience**: Smooth playback, engaging pacing

---

## 🎯 **Prompt Engineering Strategy**

### **Temperature & Sampling Settings**
- **Temperature**: 0.7-0.8 (balance creativity with consistency)
- **Top-p**: 0.9 (maintain coherent decision-making)
- **Max Tokens**: 2000-3000 (accommodate complex JSON outputs)

### **Few-Shot Examples Strategy**
- **Example 1**: Educational content with simple_caption style
- **Example 2**: Action sequence with glow_caption and dynamic effects
- **Example 3**: Contemplative content with deep_diver and Ken Burns
- **Example 4**: Music content with karaoke_style and beat sync

### **Chain-of-Thought Integration**
- **Step 1**: Content Analysis ("I see this is educational content about...")
- **Step 2**: Style Selection ("This requires clean, readable subtitles...")
- **Step 3**: Timing Strategy ("Based on the beats, I'll pace this...")
- **Step 4**: Effect Application ("Adding Ken Burns to static moments...")
- **Step 5**: Validation Check ("Ensuring platform compliance...")

### **Error Prevention Strategies**
- **Path Validation**: Consistent beat_XX.mp4 naming convention
- **Timing Logic**: Ensure start_time < end_time, no gaps/overlaps
- **Effect Compatibility**: Valid combinations of effects and animations
- **Platform Constraints**: Resolution, duration, safe zone compliance

---

## 🔧 **Implementation Roadmap**

### **Phase 1: Core System Message Development (Days 1-3)**
1. **Day 1**: Draft core identity, mission, and input processing sections
2. **Day 2**: Complete Movis capabilities reference and JSON schema
3. **Day 3**: Add editing decision matrix and quality assurance framework

### **Phase 2: Testing & Refinement (Days 4-6)**
1. **Day 4**: Test with simple educational content examples
2. **Day 5**: Test with complex multi-beat scenarios
3. **Day 6**: Refine based on output quality and JSON validation

### **Phase 3: Advanced Features (Days 7-9)**
1. **Day 7**: Add sophisticated transition logic and effect selection
2. **Day 8**: Integrate platform-specific optimization rules
3. **Day 9**: Implement user preference handling (music, subtitles)

### **Phase 4: Production Deployment (Days 10-12)**
1. **Day 10**: Deploy on RunPod with Qwen-3 32B FP8
2. **Day 11**: Integration testing with real agent outputs
3. **Day 12**: Performance optimization and error handling

---

## 📊 **Success Metrics**

### **Technical Accuracy**
- **JSON Validation**: 100% syntactically correct outputs
- **Path Consistency**: Proper beat_XX.mp4 asset referencing
- **Timing Logic**: No gaps, overlaps, or impossible durations
- **Effect Compatibility**: Valid Movis effect combinations

### **Creative Quality**
- **Style Appropriateness**: Subtitle style matches content type
- **Pacing Excellence**: Engaging rhythm for target platform
- **Transition Smoothness**: Professional flow between beats
- **Effect Enhancement**: Visual effects improve rather than distract

### **Platform Optimization**
- **Safe Zone Compliance**: Text/graphics within platform boundaries
- **Aspect Ratio Accuracy**: Perfect 9:16 or 16:9 formatting
- **Export Settings**: Optimal quality/compression for each platform
- **Performance**: Reasonable rendering times

### **User Experience**
- **Engagement**: High retention rates and completion percentages
- **Accessibility**: Clear subtitles and readable text
- **Professional Polish**: Broadcast-quality output
- **Brand Consistency**: Maintains VinVideo aesthetic standards

---

## 🚀 **Next Steps**

1. **Immediate Priority**: Begin drafting the comprehensive system message using this plan
2. **Technical Setup**: Prepare RunPod deployment environment for Qwen-3 32B FP8
3. **Test Data**: Gather sample outputs from Director, Producer, and Prompt Engineer agents
4. **Validation Framework**: Create JSON schema validators and quality checkers
5. **Integration Testing**: Connect with existing dynamic_video_editor.py pipeline

This plan provides the foundation for creating an LLM-based Editing Agent that combines creative intelligence with technical precision, delivering professional-quality video editing decisions that leverage the full capabilities of the VinVideo platform.

---

**Document Status**: Comprehensive analysis complete - Ready for system message development
**Last Updated**: June 2025
**Author**: AI Analysis of VinVideo Architecture