# Prompt for New Chat: VinVideo Editing Agent System Message Development

## **ULTRATHINK MODE: Create Comprehensive System Message for VinVideo LLM Editing Agent**

You are tasked with creating the definitive system message for VinVideo's LLM-based Editing Agent that will run on Qwen-3 32B FP8. This is a critical component that transforms AI agent outputs into intelligent JSON editing plans.

## **CONTEXT & MISSION**

VinVideo is an AI-powered short-form video creation platform. The Editing Agent receives outputs from Director, Producer, and Prompt Engineer agents, then generates JSON editing plans compatible with the existing Movis-based video pipeline. The agent must make professional, human-like editing decisions while ensuring technical precision.

## **CRITICAL FILES TO READ AND ANALYZE**

### **Project Architecture & Planning**
- `/Users/naman/Downloads/Editing_project/EDITING_AGENT_SYSTEM_MESSAGE_PLAN.md` - **MASTER PLAN** (just created - contains complete analysis)
- `/Users/naman/Downloads/Editing_project/CLAUDE.md` - Project overview and current priorities
- `/Users/naman/Downloads/Editing_project/editing_agent_read_me.md` - LLM approach architecture

### **AI Agent System Messages (Critical for Understanding Input Format)**
- `/Users/naman/Downloads/Editing_project/agents/director.tsx` - Director agent output format
- `/Users/naman/Downloads/Editing_project/agents/producer.tsx` - Producer agent output format  
- `/Users/naman/Downloads/Editing_project/agents/promptEngineer.tsx` - Prompt Engineer output format
- `/Users/naman/Downloads/Editing_project/agents/dop.tsx` - DoP agent output format (for context)

### **Technical Capabilities Documentation**
- `/Users/naman/Downloads/Editing_project/movis_overview/movis_technical_overview.md` - Complete Movis library capabilities
- `/Users/naman/Downloads/Editing_project/movis_overview/movis_vibe_overview.md` - Movis practical usage
- `/Users/naman/Downloads/Editing_project/dynamic_video_editor.py` - JSON format and Movis integration
- `/Users/naman/Downloads/Editing_project/editing_agent_to_movis.py` - JSON to video conversion

### **Subtitle System (9 Professional Styles)**
- `/Users/naman/Downloads/Editing_project/subtitle_styles/config/subtitle_styles_v3.json` - All subtitle style definitions
- `/Users/naman/Downloads/Editing_project/WORD_BY_WORD_EFFECTS_GUIDE.md` - Subtitle technical implementation
- `/Users/naman/Downloads/Editing_project/SUBTITLE_README.md` - Subtitle system overview

### **Video Generation Capabilities**
- `/Users/naman/Downloads/Editing_project/VIDEO_GENERATION_GUIDE.md` - Video creation process
- `/Users/naman/Downloads/Editing_project/VIDEO_SEQUENCE_GUIDE.md` - Multi-video composition
- `/Users/naman/Downloads/Editing_project/IMAGE_SEQUENCE_GUIDE.md` - Image sequence handling
- `/Users/naman/Downloads/Editing_project/TRANSITIONS_README.md` - Transition system

### **Example JSON Formats (Critical for Output Structure)**
- `/Users/naman/Downloads/Editing_project/example_editing_plan.json` - Complex multi-layer example
- `/Users/naman/Downloads/Editing_project/simple_editing_plan.json` - Basic format example
- `/Users/naman/Downloads/Editing_project/video_sequence_example.json` - Video sequence format
- `/Users/naman/Downloads/Editing_project/got_image_sequence_example.json` - Image sequence format

### **Pipeline Documentation**
- `/Users/naman/Downloads/Editing_project/EDITING_PIPELINE_USAGE.md` - Complete pipeline workflow
- `/Users/naman/Downloads/Editing_project/DYNAMIC_VIDEO_EDITOR_README.md` - Editor capabilities

## **YOUR SPECIFIC TASKS**

### **1. DEEP ANALYSIS (ULTRATHINK MODE)**
- Read ALL files listed above systematically
- Understand the complete VinVideo architecture
- Analyze AI agent input/output formats
- Master Movis capabilities and JSON schema
- Comprehend professional editing principles

### **2. SYSTEM MESSAGE REQUIREMENTS**

Create a comprehensive system message for Qwen-3 32B that includes:

#### **A. Core Identity & Mission**
- Expert Video Editor AI with creative intelligence
- Professional editing standards and platform optimization
- Beat-aligned content understanding

#### **B. Input Processing Framework**
- Producer Agent: Cut timing and structure (JSON array format)
- Director Agent: Creative vision and narrative beats (complex JSON with metadata)
- Prompt Engineer: Scene context and visual prompts (indexed array)
- Beat alignment system: beat_01.mp4, beat_02.mp4 mapping

#### **C. Content Analysis Engine**
- Scene type detection: action, dialogue, establishing, transition
- Emotional tone mapping: energy levels, mood, narrative function  
- Visual content analysis from image/video prompts
- Audio synchronization considerations

#### **D. Editing Decision Matrix**
- Genre-based rules: documentary, storytelling, educational, entertainment
- Platform optimization: Instagram/TikTok/YouTube Shorts
- User preferences: music integration, subtitle styling
- Technical constraints: duration, safe zones, aspect ratios

#### **E. Complete Movis Integration**
- All layer types: video, image, audio, text, shapes, effects
- Animation system: 35+ easing functions, keyframe control
- Effect catalog: blur, glow, shadow, color with parameters
- Audio management: multi-track, ducking, fades

#### **F. Professional Subtitle System**
- 9 styles with specific use cases and selection logic
- Technical specs: fonts, colors, effects, positioning
- Word-by-word sync with NVIDIA Parakeet integration
- Platform compliance: safe zones, readability

#### **G. JSON Output Schema**
- Complete structure definition with all required/optional fields
- Validation rules: data types, ranges, dependencies
- Multiple examples for different content types
- Error handling and fallback options

#### **H. Quality Assurance**
- Technical validation: syntax, paths, timing logic
- Creative standards: professional editing principles
- Platform compliance: export settings, optimization
- User experience: engagement, accessibility, polish

### **3. IMPLEMENTATION SPECIFICATIONS**

#### **Output Format Requirements**
- Return ONLY valid JSON in exact schema format
- No markdown, code blocks, or additional text
- Perfect compatibility with `editing_agent_to_movis.py`
- Asset paths using beat_XX.mp4 convention

#### **Creative Intelligence Features**
- Context-aware transition selection
- Emotional flow and pacing optimization  
- Effect application based on content analysis
- Platform-specific editing styles

#### **Error Prevention**
- Path validation and consistency checks
- Timing logic verification (no gaps/overlaps)
- Effect compatibility validation
- Safe zone compliance verification

## **KEY SUCCESS CRITERIA**

1. **Technical Accuracy**: 100% syntactically correct JSON outputs
2. **Creative Quality**: Professional editing decisions matching content
3. **Platform Optimization**: Perfect formatting for target platforms
4. **User Experience**: Engaging, accessible, polished results

## **DEPLOYMENT TARGET**
- **Model**: Qwen-3 32B FP8 on RunPod
- **Temperature**: 0.7-0.8 for creative balance
- **Max Tokens**: 2000-3000 for complex JSON
- **Integration**: Direct compatibility with existing pipeline

## **FINAL DELIVERABLE**
Create the complete, production-ready system message that will transform your Qwen-3 32B model into an expert video editing AI capable of generating professional JSON editing plans from AI agent inputs.

**ULTRATHINK through every aspect - this system message is the creative intelligence core of the entire VinVideo platform.**