#!/usr/bin/env python3
"""
Editing Agent to Movis Converter
Converts Editing Agent JSON output to Movis composition and generates final video
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the existing dynamic video editor components
from dynamic_video_editor import (
    DynamicVideoEditor,
    LayerManager,
    AnimationController,
    AudioManager,
    PlatformExporter
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EditingAgentConverter:
    """Converts Editing Agent JSON plans to Movis compositions"""
    
    def __init__(self):
        self.editor = DynamicVideoEditor()
    
    def convert_and_render(self, json_path: str, output_path: str, validate_assets: bool = True):
        """Convert JSON plan to video using Movis pipeline"""
        
        logger.info(f"Loading editing plan from: {json_path}")
        
        # Load the editing plan
        with open(json_path, 'r') as f:
            editing_plan = json.load(f)
        
        # Validate the plan structure
        self._validate_editing_plan(editing_plan)
        
        # Optionally validate that asset files exist
        if validate_assets:
            self._validate_assets(editing_plan)
        
        # Convert to Movis composition
        logger.info("Converting to Movis composition...")
        self._create_movis_composition(editing_plan)
        
        # Export the final video
        logger.info(f"Rendering video to: {output_path}")
        platform = editing_plan.get("export", {}).get("platform", "instagram")
        quality = editing_plan.get("export", {}).get("quality", "high")
        
        self.editor.export_video(output_path, platform=platform, quality=quality)
        
        logger.info("✅ Video generation complete!")
        
        return {
            "output_path": output_path,
            "duration": self.editor.composition.duration,
            "resolution": self.editor.composition.size,
            "platform": platform,
            "layers_count": len(editing_plan.get("layers", [])),
            "metadata": editing_plan.get("metadata", {})
        }
    
    def _validate_editing_plan(self, plan: Dict[str, Any]):
        """Validate the structure of the editing plan"""
        required_fields = ["composition", "layers"]
        
        for field in required_fields:
            if field not in plan:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate composition
        comp = plan["composition"]
        comp_required = ["resolution", "duration", "fps"]
        for field in comp_required:
            if field not in comp:
                raise ValueError(f"Missing composition field: {field}")
        
        # Validate layers
        for i, layer in enumerate(plan.get("layers", [])):
            if "type" not in layer:
                raise ValueError(f"Layer {i} missing 'type' field")
            if "source" not in layer:
                raise ValueError(f"Layer {i} missing 'source' field")
        
        logger.info("✅ Editing plan structure validated")
    
    def _validate_assets(self, plan: Dict[str, Any]):
        """Validate that all referenced assets exist"""
        missing_assets = []
        
        # Check video/image layers
        for layer in plan.get("layers", []):
            source = layer.get("source")
            if source and not os.path.exists(source):
                missing_assets.append(source)
        
        # Check image sequence
        for image in plan.get("image_sequence", []):
            source = image.get("source")
            if source and not os.path.exists(source):
                missing_assets.append(source)
        
        # Check audio
        audio = plan.get("audio", {})
        for audio_track in audio.values():
            if isinstance(audio_track, dict):
                source = audio_track.get("source")
                if source and not os.path.exists(source):
                    missing_assets.append(source)
        
        # Check subtitles
        subtitles = plan.get("subtitles", {})
        parakeet_data = subtitles.get("parakeet_data")
        if parakeet_data and not os.path.exists(parakeet_data):
            missing_assets.append(parakeet_data)
        
        if missing_assets:
            logger.warning(f"⚠️  Missing assets detected: {missing_assets}")
            logger.warning("Proceeding anyway - will use placeholder or skip missing assets")
        else:
            logger.info("✅ All assets validated")
    
    def _create_movis_composition(self, plan: Dict[str, Any]):
        """Create Movis composition from editing plan"""
        
        # Create main composition
        comp_config = plan["composition"]
        self.editor.create_composition(
            resolution=tuple(comp_config["resolution"]),
            duration=comp_config["duration"],
            fps=comp_config.get("fps", 30),
            background_color=comp_config.get("background_color")
        )
        
        # Process layers in order
        self._process_layers(plan.get("layers", []))
        
        # Process image sequence if present
        if "image_sequence" in plan:
            self._process_image_sequence(plan["image_sequence"])
        
        # Process audio
        self._process_audio(plan.get("audio", {}))
        
        # Process subtitles
        self._process_subtitles(plan.get("subtitles", {}))
        
        logger.info("✅ Movis composition created successfully")
    
    def _process_layers(self, layers: List[Dict[str, Any]]):
        """Process video/image layers"""
        
        for layer_config in layers:
            try:
                layer_type = layer_config["type"]
                source = layer_config["source"]
                
                # Skip if source file doesn't exist
                if not os.path.exists(source):
                    logger.warning(f"Skipping layer - file not found: {source}")
                    continue
                
                if layer_type == "video":
                    self._add_video_layer(layer_config)
                elif layer_type == "image":
                    self._add_image_layer(layer_config)
                else:
                    logger.warning(f"Unknown layer type: {layer_type}")
                    
            except Exception as e:
                logger.error(f"Error processing layer: {e}")
                continue
    
    def _add_video_layer(self, config: Dict[str, Any]):
        """Add a video layer to the composition"""
        
        # Calculate timing
        start_time = config.get("start_time", 0.0)
        end_time = config.get("end_time")
        duration = None
        
        if end_time is not None:
            duration = end_time - start_time
        
        # Add the video layer
        layer_item = self.editor.layer_manager.add_video_layer(
            source=config["source"],
            name=config.get("name", "video_layer"),
            position=tuple(config.get("position", [540, 960])),
            scale=config.get("scale", 1.0),
            rotation=config.get("rotation", 0.0),
            opacity=config.get("opacity", 1.0),
            offset=start_time,
            end_time=duration  # This will be duration from start_time
        )
        
        # Apply animations
        if "animations" in config:
            self._apply_animations(layer_item, config["animations"])
        
        # Apply effects
        if "effects" in config:
            self._apply_effects(layer_item, config["effects"])
        
        logger.info(f"Added video layer: {config['source']}")
    
    def _add_image_layer(self, config: Dict[str, Any]):
        """Add an image layer to the composition"""
        
        # Calculate timing and duration
        start_time = config.get("start_time", 0.0)
        end_time = config.get("end_time")
        duration = 5.0  # Default duration
        
        if end_time is not None:
            duration = end_time - start_time
        elif "duration" in config:
            duration = config["duration"]
        
        # Add the image layer
        layer_item = self.editor.layer_manager.add_image_layer(
            source=config["source"],
            duration=duration,
            name=config.get("name", "image_layer"),
            position=tuple(config.get("position", [540, 960])),
            scale=config.get("scale", 1.0),
            rotation=config.get("rotation", 0.0),
            opacity=config.get("opacity", 1.0),
            offset=start_time
        )
        
        # Apply animations
        if "animations" in config:
            self._apply_animations(layer_item, config["animations"])
        
        # Apply effects
        if "effects" in config:
            self._apply_effects(layer_item, config["effects"])
        
        logger.info(f"Added image layer: {config['source']}")
    
    def _process_image_sequence(self, sequence: List[Dict[str, Any]]):
        """Process image sequence using existing dynamic editor logic"""
        self.editor.process_image_sequence(sequence)
        logger.info(f"Processed image sequence with {len(sequence)} images")
    
    def _process_audio(self, audio_config: Dict[str, Any]):
        """Process audio tracks"""
        
        for track_name, track_config in audio_config.items():
            if not isinstance(track_config, dict):
                continue
            
            source = track_config.get("source")
            if not source or not os.path.exists(source):
                logger.warning(f"Audio file not found: {source}")
                continue
            
            if track_name == "background_music":
                self.editor.audio_manager.add_background_music(
                    source=source,
                    level=track_config.get("level", -15.0),
                    fade_in=track_config.get("fade_in", 2.0),
                    fade_out=track_config.get("fade_out", 2.0)
                )
                logger.info("Added background music")
                
            elif track_name == "narration":
                self.editor.audio_manager.add_narration(
                    source=source,
                    offset=track_config.get("offset", 0.0),
                    level=track_config.get("level", 0.0)
                )
                logger.info("Added narration track")
    
    def _process_subtitles(self, subtitle_config: Dict[str, Any]):
        """Process subtitles using existing subtitle system"""
        
        if not subtitle_config:
            return
        
        parakeet_data = subtitle_config.get("parakeet_data")
        style_name = subtitle_config.get("style", "simple_caption")
        position = subtitle_config.get("position", "bottom")
        
        if parakeet_data and os.path.exists(parakeet_data):
            self.editor.add_subtitle_layer(
                parakeet_data=parakeet_data,
                style_name=style_name,
                position=position
            )
            logger.info(f"Added subtitles with style: {style_name}")
        else:
            logger.warning("Subtitle data not found or not specified")
    
    def _apply_animations(self, layer_item, animations: Dict[str, Any]):
        """Apply animations to a layer using existing animation controller"""
        
        for property_name, anim_config in animations.items():
            keyframes = anim_config.get("keyframes", [])
            values = anim_config.get("values", [])
            easings = anim_config.get("easings")
            
            if not keyframes or not values:
                continue
            
            try:
                if property_name == "opacity":
                    AnimationController.animate_opacity(layer_item, keyframes, values, easings)
                elif property_name == "position":
                    AnimationController.animate_position(layer_item, keyframes, values, easings)
                elif property_name == "scale":
                    AnimationController.animate_scale(layer_item, keyframes, values, easings)
                elif property_name == "rotation":
                    AnimationController.animate_rotation(layer_item, keyframes, values, easings)
                
                logger.info(f"Applied {property_name} animation")
                
            except Exception as e:
                logger.error(f"Error applying {property_name} animation: {e}")
    
    def _apply_effects(self, layer_item, effects: List[str]):
        """Apply effects to a layer"""
        
        # Import movis effects here to avoid import errors during module load
        try:
            import movis as mv
            
            for effect_name in effects:
                try:
                    if effect_name == "glow":
                        layer_item.add_effect(mv.effect.Glow(radius=20.0, strength=1.5))
                    elif effect_name == "blur":
                        layer_item.add_effect(mv.effect.GaussianBlur(radius=10.0))
                    elif effect_name == "shadow":
                        layer_item.add_effect(mv.effect.DropShadow(
                            radius=5.0, offset=10.0, angle=45.0, opacity=0.5
                        ))
                    
                    logger.info(f"Applied effect: {effect_name}")
                    
                except Exception as e:
                    logger.error(f"Error applying effect {effect_name}: {e}")
                    
        except ImportError:
            logger.warning("Movis not available - skipping effects")


def validate_json_plan(json_path: str) -> bool:
    """Validate that a JSON file is a valid editing plan"""
    try:
        with open(json_path, 'r') as f:
            plan = json.load(f)
        
        required_fields = ["composition", "layers"]
        for field in required_fields:
            if field not in plan:
                return False
        
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert Editing Agent JSON to video using Movis pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert editing plan to video
  python3 editing_agent_to_movis.py plan.json output.mp4

  # Convert with custom platform
  python3 editing_agent_to_movis.py plan.json output.mp4 --platform youtube_shorts

  # Convert without asset validation (for testing)
  python3 editing_agent_to_movis.py plan.json output.mp4 --no-validate-assets
        """
    )
    
    parser.add_argument('json_file', type=str, help='Path to Editing Agent JSON plan')
    parser.add_argument('output_file', type=str, help='Output video file path')
    parser.add_argument('--platform', type=str, 
                        choices=['instagram', 'tiktok', 'youtube_shorts', 'youtube'],
                        help='Override platform from JSON plan')
    parser.add_argument('--quality', type=str, choices=['low', 'medium', 'high'],
                        help='Override quality from JSON plan')
    parser.add_argument('--no-validate-assets', action='store_true',
                        help='Skip validation of asset file existence')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input file
    if not os.path.exists(args.json_file):
        print(f"❌ Error: JSON file not found: {args.json_file}")
        return 1
    
    if not validate_json_plan(args.json_file):
        print(f"❌ Error: Invalid editing plan format: {args.json_file}")
        return 1
    
    # Create output directory if needed
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create converter and process
        converter = EditingAgentConverter()
        
        # Override platform/quality if specified
        if args.platform or args.quality:
            with open(args.json_file, 'r') as f:
                plan = json.load(f)
            
            if args.platform:
                plan.setdefault("export", {})["platform"] = args.platform
            if args.quality:
                plan.setdefault("export", {})["quality"] = args.quality
            
            # Save modified plan temporarily
            temp_json = args.json_file + ".tmp"
            with open(temp_json, 'w') as f:
                json.dump(plan, f, indent=2)
            
            result = converter.convert_and_render(
                temp_json, 
                args.output_file, 
                validate_assets=not args.no_validate_assets
            )
            
            # Clean up temp file
            os.remove(temp_json)
        else:
            result = converter.convert_and_render(
                args.json_file, 
                args.output_file, 
                validate_assets=not args.no_validate_assets
            )
        
        # Print summary
        print(f"\n🎬 Video Generation Complete!")
        print(f"   Output: {result['output_path']}")
        print(f"   Duration: {result['duration']:.1f}s")
        print(f"   Resolution: {result['resolution']}")
        print(f"   Platform: {result['platform']}")
        print(f"   Layers: {result['layers_count']}")
        
        metadata = result.get('metadata', {})
        if metadata:
            print(f"   Style: {metadata.get('editing_style', 'N/A')}")
            print(f"   Agent Version: {metadata.get('agent_version', 'N/A')}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())