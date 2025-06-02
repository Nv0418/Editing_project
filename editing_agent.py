#!/usr/bin/env python3
"""
VinVideo Editing Agent
The creative intelligence core that transforms AI agent outputs into professional video editing plans
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AgentOutput:
    """Base class for all agent outputs"""
    agent_type: str
    timestamp: str
    data: Dict[str, Any]


@dataclass
class ProducerOutput(AgentOutput):
    """Producer Agent output containing timeline structure and asset information"""
    shot_count: int
    total_duration: float
    beat_durations: Dict[str, float]  # beat_01: 3.5, beat_02: 4.2, etc.
    asset_paths: Dict[str, str]       # beat_01: /path/to/beat_01.mp4
    
    def __post_init__(self):
        self.agent_type = "producer"


@dataclass
class DirectorOutput(AgentOutput):
    """Director Agent output containing creative vision and storytelling approach"""
    genre: str                        # documentary, storytelling, action, educational
    tone: str                         # energetic, calm, dramatic, inspiring
    pacing: str                       # fast, medium, slow
    story_arc: Dict[str, Any]         # narrative structure
    emotional_beats: Dict[str, str]   # beat_01: "introduction", beat_02: "conflict"
    
    def __post_init__(self):
        self.agent_type = "director"


@dataclass
class PromptEngineerOutput(AgentOutput):
    """Prompt Engineer output containing scene context and generation details"""
    beat_contexts: Dict[str, Dict[str, Any]]  # beat_01: {image_prompt, video_prompt, scene_type}
    
    def __post_init__(self):
        self.agent_type = "prompt_engineer"


class BeatAlignmentSystem:
    """Manages the alignment and semantic understanding of beats across agent outputs"""
    
    def __init__(self):
        self.beat_registry: Dict[str, Dict[str, Any]] = {}
    
    def register_beat(self, beat_id: str, producer_data: Dict, director_data: Dict, prompt_data: Dict):
        """Register a beat with data from all agents"""
        self.beat_registry[beat_id] = {
            "asset_path": producer_data.get("asset_path"),
            "duration": producer_data.get("duration"),
            "emotional_context": director_data.get("emotional_context"),
            "scene_type": prompt_data.get("scene_type"),
            "image_prompt": prompt_data.get("image_prompt"),
            "video_prompt": prompt_data.get("video_prompt"),
            "action_level": self._detect_action_level(prompt_data),
            "dialogue_present": self._detect_dialogue(prompt_data)
        }
    
    def _detect_action_level(self, prompt_data: Dict) -> str:
        """Detect if scene is action-heavy, moderate, or static"""
        video_prompt = prompt_data.get("video_prompt", "").lower()
        
        action_keywords = ["running", "fighting", "jumping", "moving", "chase", "explosion", "fast"]
        static_keywords = ["sitting", "standing", "talking", "portrait", "still", "calm"]
        
        action_score = sum(1 for keyword in action_keywords if keyword in video_prompt)
        static_score = sum(1 for keyword in static_keywords if keyword in video_prompt)
        
        if action_score > static_score:
            return "high"
        elif static_score > action_score:
            return "low"
        else:
            return "medium"
    
    def _detect_dialogue(self, prompt_data: Dict) -> bool:
        """Detect if scene likely contains dialogue"""
        prompts = f"{prompt_data.get('image_prompt', '')} {prompt_data.get('video_prompt', '')}".lower()
        dialogue_keywords = ["talking", "speaking", "conversation", "dialogue", "interview", "speech"]
        return any(keyword in prompts for keyword in dialogue_keywords)
    
    def get_beat_info(self, beat_id: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a specific beat"""
        return self.beat_registry.get(beat_id)
    
    def get_all_beats(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered beats"""
        return self.beat_registry


class EditingStyleProfiles:
    """Defines different editing personalities and style approaches"""
    
    PROFILES = {
        "energetic": {
            "avg_shot_duration": 2.5,
            "transition_intensity": "high",
            "preferred_transitions": ["quick_cut", "zoom_fade", "slide"],
            "effect_intensity": 0.8,
            "pacing_multiplier": 1.3,
            "ken_burns_usage": 0.7
        },
        "calm": {
            "avg_shot_duration": 4.5,
            "transition_intensity": "low",
            "preferred_transitions": ["fade", "dissolve", "gentle_slide"],
            "effect_intensity": 0.3,
            "pacing_multiplier": 0.8,
            "ken_burns_usage": 0.4
        },
        "cinematic": {
            "avg_shot_duration": 3.8,
            "transition_intensity": "medium",
            "preferred_transitions": ["fade", "zoom_fade", "cross_dissolve"],
            "effect_intensity": 0.6,
            "pacing_multiplier": 1.0,
            "ken_burns_usage": 0.8
        },
        "social_media": {
            "avg_shot_duration": 2.0,
            "transition_intensity": "high",
            "preferred_transitions": ["quick_cut", "zoom_fade", "slide"],
            "effect_intensity": 0.9,
            "pacing_multiplier": 1.4,
            "ken_burns_usage": 0.9
        }
    }
    
    @classmethod
    def get_profile(cls, style_name: str) -> Dict[str, Any]:
        """Get editing style profile by name"""
        return cls.PROFILES.get(style_name, cls.PROFILES["cinematic"])
    
    @classmethod
    def select_profile_for_genre(cls, genre: str, tone: str) -> Dict[str, Any]:
        """Automatically select appropriate profile based on genre and tone"""
        if genre == "action" or tone == "energetic":
            return cls.get_profile("energetic")
        elif genre == "documentary" or tone == "calm":
            return cls.get_profile("calm")
        elif genre == "storytelling":
            return cls.get_profile("cinematic")
        else:
            return cls.get_profile("social_media")


class CreativeDecisionEngine:
    """The core intelligence that makes human-like editing decisions"""
    
    def __init__(self, beat_system: BeatAlignmentSystem):
        self.beat_system = beat_system
        self.style_profiles = EditingStyleProfiles()
    
    def select_transitions(self, beat_from: str, beat_to: str, style_profile: Dict) -> Dict[str, Any]:
        """Select appropriate transition between two beats"""
        beat_from_info = self.beat_system.get_beat_info(beat_from)
        beat_to_info = self.beat_system.get_beat_info(beat_to)
        
        if not beat_from_info or not beat_to_info:
            return {"type": "fade", "duration": 0.5}
        
        # Analyze emotional and action continuity
        emotional_change = self._calculate_emotional_change(beat_from_info, beat_to_info)
        action_change = self._calculate_action_change(beat_from_info, beat_to_info)
        
        # Select transition based on changes and style
        if emotional_change > 0.7:  # Major emotional shift
            return {"type": "quick_cut", "duration": 0.1}
        elif action_change > 0.5:  # Significant action change
            if "zoom_fade" in style_profile["preferred_transitions"]:
                return {"type": "zoom_fade", "duration": 0.4, "zoom_start": 1.2, "zoom_end": 1.0}
            else:
                return {"type": "slide", "duration": 0.3, "direction": "left"}
        else:  # Smooth continuity
            return {"type": "fade", "duration": 0.5}
    
    def _calculate_emotional_change(self, beat_from: Dict, beat_to: Dict) -> float:
        """Calculate emotional discontinuity between beats"""
        # Simplified emotional mapping - in practice this would be more sophisticated
        emotional_weights = {
            "introduction": 0.2,
            "conflict": 0.8,
            "resolution": 0.4,
            "climax": 1.0,
            "calm": 0.1
        }
        
        from_weight = emotional_weights.get(beat_from.get("emotional_context", ""), 0.5)
        to_weight = emotional_weights.get(beat_to.get("emotional_context", ""), 0.5)
        
        return abs(to_weight - from_weight)
    
    def _calculate_action_change(self, beat_from: Dict, beat_to: Dict) -> float:
        """Calculate action level discontinuity between beats"""
        action_levels = {"low": 0.1, "medium": 0.5, "high": 1.0}
        
        from_level = action_levels.get(beat_from.get("action_level", "medium"), 0.5)
        to_level = action_levels.get(beat_to.get("action_level", "medium"), 0.5)
        
        return abs(to_level - from_level)
    
    def select_effects(self, beat_id: str, style_profile: Dict) -> List[str]:
        """Select appropriate effects for a beat based on content and style"""
        beat_info = self.beat_system.get_beat_info(beat_id)
        if not beat_info:
            return []
        
        effects = []
        
        # Add effects based on action level and style intensity
        if beat_info["action_level"] == "high" and style_profile["effect_intensity"] > 0.6:
            effects.append("motion_blur")
        
        if beat_info["emotional_context"] in ["climax", "conflict"]:
            if style_profile["effect_intensity"] > 0.5:
                effects.append("glow")
        
        return effects
    
    def calculate_beat_timing(self, beat_id: str, base_duration: float, style_profile: Dict) -> float:
        """Calculate optimal duration for a beat based on content and style"""
        beat_info = self.beat_system.get_beat_info(beat_id)
        if not beat_info:
            return base_duration
        
        # Adjust duration based on content
        duration_modifier = 1.0
        
        # Action scenes can be shorter for impact
        if beat_info["action_level"] == "high":
            duration_modifier *= 0.9
        elif beat_info["action_level"] == "low":
            duration_modifier *= 1.1
        
        # Dialogue scenes need more time
        if beat_info["dialogue_present"]:
            duration_modifier *= 1.2
        
        # Apply style pacing
        duration_modifier *= style_profile["pacing_multiplier"]
        
        return base_duration * duration_modifier


class TimelineComposer:
    """Composes the final timeline with proper timing, transitions, and effects"""
    
    def __init__(self, beat_system: BeatAlignmentSystem, decision_engine: CreativeDecisionEngine):
        self.beat_system = beat_system
        self.decision_engine = decision_engine
    
    def compose_timeline(self, producer_output: ProducerOutput, director_output: DirectorOutput, 
                        style_profile: Dict) -> List[Dict[str, Any]]:
        """Create the main timeline structure"""
        timeline = []
        current_time = 0.0
        
        # Get all beats sorted by beat number
        beats = sorted(self.beat_system.get_all_beats().keys(), 
                      key=lambda x: int(x.split('_')[1]))
        
        for i, beat_id in enumerate(beats):
            beat_info = self.beat_system.get_beat_info(beat_id)
            if not beat_info:
                continue
            
            # Calculate timing for this beat
            base_duration = producer_output.beat_durations.get(beat_id, 3.0)
            final_duration = self.decision_engine.calculate_beat_timing(
                beat_id, base_duration, style_profile
            )
            
            # Create layer configuration
            layer_config = {
                "type": "video",
                "source": beat_info["asset_path"],
                "name": f"layer_{beat_id}",
                "start_time": current_time,
                "end_time": current_time + final_duration,
                "position": [540, 960],
                "scale": 1.0,
                "opacity": 1.0,
                "animations": self._create_animations(beat_info, final_duration, style_profile),
                "effects": self.decision_engine.select_effects(beat_id, style_profile)
            }
            
            timeline.append(layer_config)
            current_time += final_duration
        
        return timeline
    
    def _create_animations(self, beat_info: Dict, duration: float, style_profile: Dict) -> Dict[str, Any]:
        """Create animations for a beat based on content and style"""
        animations = {}
        
        # Standard fade in/out for all beats
        animations["opacity"] = {
            "keyframes": [0.0, 0.5, duration - 0.5, duration],
            "values": [0.0, 1.0, 1.0, 0.0],
            "easings": ["ease_out", "linear", "ease_in"]
        }
        
        # Ken Burns effect for static scenes
        if (beat_info["action_level"] == "low" and 
            style_profile.get("ken_burns_usage", 0) > 0.5):
            
            animations["scale"] = {
                "keyframes": [0.0, duration],
                "values": [1.0, 1.1],
                "easings": ["ease_in_out"]
            }
        
        # Movement for high-energy scenes
        if (beat_info["action_level"] == "high" and 
            style_profile["transition_intensity"] == "high"):
            
            animations["position"] = {
                "keyframes": [0.0, duration],
                "values": [[540, 970], [540, 950]],
                "easings": ["ease_in_out"]
            }
        
        return animations


class JSONGenerator:
    """Generates JSON editing plans compatible with dynamic_video_editor.py"""
    
    def __init__(self):
        self.template = {
            "metadata": {
                "agent_version": "1.0",
                "creation_timestamp": "",
                "editing_style": "",
                "target_platform": "instagram"
            },
            "composition": {
                "resolution": [1080, 1920],
                "duration": 0.0,
                "fps": 30,
                "background_color": [0, 0, 0]
            },
            "layers": [],
            "audio": {},
            "subtitles": {},
            "export": {
                "platform": "instagram",
                "quality": "high"
            }
        }
    
    def generate_editing_plan(self, timeline: List[Dict], producer_output: ProducerOutput,
                            director_output: DirectorOutput, style_name: str) -> Dict[str, Any]:
        """Generate complete JSON editing plan"""
        
        plan = self.template.copy()
        
        # Update metadata
        plan["metadata"]["creation_timestamp"] = datetime.now().isoformat()
        plan["metadata"]["editing_style"] = style_name
        
        # Update composition
        total_duration = max(layer["end_time"] for layer in timeline) if timeline else 10.0
        plan["composition"]["duration"] = total_duration
        
        # Add layers
        plan["layers"] = timeline
        
        # Add audio if available
        if hasattr(producer_output, 'audio_path') and producer_output.audio_path:
            plan["audio"] = {
                "narration": {
                    "source": producer_output.audio_path,
                    "offset": 0.0,
                    "level": 0.0
                }
            }
        
        # Add subtitles if available
        if hasattr(producer_output, 'subtitle_data') and producer_output.subtitle_data:
            plan["subtitles"] = {
                "parakeet_data": producer_output.subtitle_data,
                "style": self._select_subtitle_style(director_output.genre, director_output.tone),
                "position": "bottom"
            }
        
        return plan
    
    def _select_subtitle_style(self, genre: str, tone: str) -> str:
        """Select appropriate subtitle style based on content"""
        style_mapping = {
            ("documentary", "calm"): "simple_caption",
            ("documentary", "energetic"): "highlight_caption",
            ("storytelling", "dramatic"): "deep_diver",
            ("action", "energetic"): "glow_caption",
            ("educational", "calm"): "background_caption"
        }
        
        return style_mapping.get((genre, tone), "simple_caption")


class EditingAgent:
    """Main Editing Agent that orchestrates the entire editing process"""
    
    def __init__(self):
        self.beat_system = BeatAlignmentSystem()
        self.decision_engine = CreativeDecisionEngine(self.beat_system)
        self.timeline_composer = TimelineComposer(self.beat_system, self.decision_engine)
        self.json_generator = JSONGenerator()
    
    def process_agent_outputs(self, producer_output: ProducerOutput,
                            director_output: DirectorOutput,
                            prompt_engineer_output: PromptEngineerOutput) -> Dict[str, Any]:
        """Process all agent outputs and generate editing plan"""
        
        logger.info("Processing agent outputs...")
        
        # Register all beats with the alignment system
        self._register_beats(producer_output, director_output, prompt_engineer_output)
        
        # Select editing style based on director input
        style_profile = EditingStyleProfiles.select_profile_for_genre(
            director_output.genre, director_output.tone
        )
        style_name = self._get_style_name(director_output.genre, director_output.tone)
        
        logger.info(f"Selected editing style: {style_name}")
        
        # Compose timeline
        timeline = self.timeline_composer.compose_timeline(
            producer_output, director_output, style_profile
        )
        
        logger.info(f"Composed timeline with {len(timeline)} layers")
        
        # Generate final JSON editing plan
        editing_plan = self.json_generator.generate_editing_plan(
            timeline, producer_output, director_output, style_name
        )
        
        logger.info("Generated JSON editing plan successfully")
        
        return editing_plan
    
    def _register_beats(self, producer_output: ProducerOutput,
                       director_output: DirectorOutput,
                       prompt_engineer_output: PromptEngineerOutput):
        """Register all beats with data from all agents"""
        
        for beat_id in producer_output.beat_durations.keys():
            producer_data = {
                "asset_path": producer_output.asset_paths.get(beat_id),
                "duration": producer_output.beat_durations.get(beat_id)
            }
            
            director_data = {
                "emotional_context": director_output.emotional_beats.get(beat_id)
            }
            
            prompt_data = prompt_engineer_output.beat_contexts.get(beat_id, {})
            
            self.beat_system.register_beat(beat_id, producer_data, director_data, prompt_data)
    
    def _get_style_name(self, genre: str, tone: str) -> str:
        """Get style name for metadata"""
        if genre == "action" or tone == "energetic":
            return "energetic"
        elif genre == "documentary" or tone == "calm":
            return "calm"
        elif genre == "storytelling":
            return "cinematic"
        else:
            return "social_media"
    
    def save_editing_plan(self, editing_plan: Dict[str, Any], output_path: str):
        """Save the generated editing plan to file"""
        with open(output_path, 'w') as f:
            json.dump(editing_plan, f, indent=2)
        logger.info(f"Saved editing plan to: {output_path}")


def create_mock_agent_outputs() -> Tuple[ProducerOutput, DirectorOutput, PromptEngineerOutput]:
    """Create mock agent outputs for testing"""
    
    # Mock Producer Output
    producer = ProducerOutput(
        agent_type="producer",
        timestamp=datetime.now().isoformat(),
        data={},
        shot_count=3,
        total_duration=15.0,
        beat_durations={"beat_01": 5.0, "beat_02": 5.0, "beat_03": 5.0},
        asset_paths={
            "beat_01": "/path/to/beat_01.mp4",
            "beat_02": "/path/to/beat_02.mp4", 
            "beat_03": "/path/to/beat_03.mp4"
        }
    )
    
    # Mock Director Output
    director = DirectorOutput(
        agent_type="director",
        timestamp=datetime.now().isoformat(),
        data={},
        genre="storytelling",
        tone="cinematic",
        pacing="medium",
        story_arc={"act1": "setup", "act2": "conflict", "act3": "resolution"},
        emotional_beats={
            "beat_01": "introduction",
            "beat_02": "conflict", 
            "beat_03": "resolution"
        }
    )
    
    # Mock Prompt Engineer Output
    prompt_engineer = PromptEngineerOutput(
        agent_type="prompt_engineer",
        timestamp=datetime.now().isoformat(),
        data={},
        beat_contexts={
            "beat_01": {
                "image_prompt": "A peaceful landscape with mountains",
                "video_prompt": "Camera slowly pans across the serene mountain landscape",
                "scene_type": "establishing"
            },
            "beat_02": {
                "image_prompt": "Two characters in heated discussion",
                "video_prompt": "Characters arguing intensely, quick camera movements",
                "scene_type": "conflict"
            },
            "beat_03": {
                "image_prompt": "Characters embracing at sunset",
                "video_prompt": "Slow motion embrace as the sun sets behind them",
                "scene_type": "resolution"
            }
        }
    )
    
    return producer, director, prompt_engineer


def main():
    """Example usage of the Editing Agent"""
    
    # Create editing agent
    agent = EditingAgent()
    
    # Create mock inputs (in practice these come from other agents)
    producer_output, director_output, prompt_engineer_output = create_mock_agent_outputs()
    
    # Process inputs and generate editing plan
    editing_plan = agent.process_agent_outputs(
        producer_output, director_output, prompt_engineer_output
    )
    
    # Save editing plan
    output_path = "generated_editing_plan.json"
    agent.save_editing_plan(editing_plan, output_path)
    
    print(f"✅ Generated editing plan saved to: {output_path}")
    print(f"Timeline duration: {editing_plan['composition']['duration']:.1f}s")
    print(f"Number of layers: {len(editing_plan['layers'])}")
    print(f"Editing style: {editing_plan['metadata']['editing_style']}")


if __name__ == "__main__":
    main()