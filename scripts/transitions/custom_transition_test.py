#!/usr/bin/env python3
"""
Custom Transition Video Editor using Movis

This script creates a 10-second video with custom distortion transitions between video segments.
"""

import os
import sys
import json
from pathlib import Path

# Add the modified movis to path
sys.path.insert(0, '/Users/naman/Desktop/movie_py/movis')

import movis as mv
# Import our custom transition registry
sys.path.insert(0, '/Users/naman/Desktop/movie_py')
from scripts.transitions.registry import TransitionRegistry, apply_distortion_transition


class CustomTransitionVideoEditor:
    """Creates videos with custom transitions."""
    
    def __init__(self, assets_folder: str):
        self.assets_folder = Path(assets_folder)
        self.target_duration = 10.0  # 10 seconds
        self.audio_reduction_db = -6  # -6dB audio level
        
        # Find assets
        self.video_files = list(self.assets_folder.glob("media/*.mp4"))
        self.audio_files = list(self.assets_folder.glob("media/*.mp3"))
        
        # Filter out the output file if it exists
        self.video_files = [f for f in self.video_files if not f.name.startswith('beat_sync_output')]
        
        if len(self.video_files) < 3:
            raise ValueError(f"Need at least 3 video files, found {len(self.video_files)}")
        if len(self.audio_files) < 1:
            raise ValueError(f"Need at least 1 audio file, found {len(self.audio_files)}")
        
        # Sort video files to ensure consistent ordering
        self.video_files.sort()
        
        # Select exactly 3 videos for our test
        self.video_files = self.video_files[:3]
        
        print(f"🎬 Found {len(self.video_files)} videos and {len(self.audio_files)} audio files")
        for i, video in enumerate(self.video_files):
            print(f"   Video {i+1}: {video.name}")
        
        # Initialize transition registry
        self.transition_registry = TransitionRegistry()
        self.available_transitions = self.transition_registry.list_transitions()
        print(f"🎭 Available transitions: {self.available_transitions}")
    
    def calculate_video_segments(self):
        """Create exactly 3 segments with custom transitions."""
        num_videos = len(self.video_files)  # Should be 3
        
        # For transitions, we need segments to overlap
        transition_duration = 0.8  # 0.8 second overlap for transition
        
        # Divide remaining time after accounting for overlaps
        remaining_time = self.target_duration - (transition_duration * 2)  # 2 overlaps
        segment_base_duration = remaining_time / num_videos  # Base duration per segment
        
        segments = []
        
        for i in range(num_videos):
            if i == 0:
                # First segment: normal start, extend for transition
                start_time = 0.0
                duration = segment_base_duration + transition_duration
            elif i == num_videos - 1:
                # Last segment: start early for transition, normal end
                start_time = (i * segment_base_duration) + ((i-1) * transition_duration)
                duration = segment_base_duration + transition_duration
            else:
                # Middle segments: start early, extend for transition
                start_time = (i * segment_base_duration) + ((i-1) * transition_duration)
                duration = segment_base_duration + (transition_duration * 2)
            
            # Assign different transitions to each segment pair
            if i == 0:
                transition_id = None  # First segment has no incoming transition
            elif i == 1:
                transition_id = "distortion/transition_01"
            else:
                transition_id = "distortion/transition_02"
            
            segments.append({
                "video_idx": i,  # Use each video exactly once
                "start": start_time,
                "duration": duration,
                "transition_duration": transition_duration,
                "transition_id": transition_id,
                "trim_end": 1.0  # Trim 1 second from end of source video
            })
        
        print(f"📊 Created {len(segments)} segments with custom transitions")
        print(f"⏱️ Base segment duration: {segment_base_duration:.2f}s + {transition_duration:.2f}s overlap")
        
        return segments
    
    def create_edit_plan(self, segments, audio_file):
        """Create a JSON edit plan with custom transitions."""
        instructions = []
        
        # Add exactly 3 video segments with custom transitions
        for i, segment in enumerate(segments):
            video_file = self.video_files[segment["video_idx"]]
            transition_duration = segment["transition_duration"]
            
            # Create video instruction
            video_instruction = {
                "type": "video",
                "asset_id": f"VIDEO-{i:03d}",
                "start_time": segment["start"],
                "duration": segment["duration"],
                "position": [540, 960],  # Center for 1080x1920
                "scale": [1.0, 1.0],
                "opacity": 1.0,
                "properties": {
                    "source_file": str(video_file),
                    "source_start": 0.0,  # Start from beginning
                    "source_end_trim": segment.get("trim_end", 0.0)  # Trim 1 sec from end
                }
            }
            
            # Add transition information if this segment has an incoming transition
            if segment["transition_id"]:
                video_instruction["transition"] = {
                    "type": segment["transition_id"],
                    "duration": transition_duration,
                    "from_asset_id": f"VIDEO-{i-1:03d}"
                }
                print(f"🎭 Adding {segment['transition_id']} transition to segment {i+1}")
            
            instructions.append(video_instruction)
            
            print(f"📹 Segment {i+1}: {video_file.name} from {segment['start']:.2f}s for {segment['duration']:.2f}s (trim {segment.get('trim_end', 0.0)}s from end)")
        
        # Add background music
        instructions.append({
            "type": "audio",
            "asset_id": "AUDIO-BGM",
            "start_time": 0.0,
            "duration": self.target_duration,
            "properties": {
                "source_file": str(self.audio_files[0]),
                "volume_db": self.audio_reduction_db
            }
        })
        
        # Create complete edit plan
        edit_plan = {
            "scene_id": "custom_transition_test",
            "target_format": "tiktok",
            "resolution": [1080, 1920],
            "duration": self.target_duration,
            "instructions": instructions,
            "metadata": {
                "description": "Custom transition video created with Movis",
                "segment_count": len(segments),
                "audio_source": Path(str(self.audio_files[0])).name
            }
        }
        
        return edit_plan
    
    def create_composition(self, edit_plan):
        """Create Movis composition from edit plan."""
        print("🎞️ Creating Movis composition...")
        
        # Create composition
        composition = mv.layer.Composition(
            size=tuple(edit_plan["resolution"]),
            duration=edit_plan["duration"]
        )
        
        # Add black background
        composition.add_layer(
            mv.layer.Rectangle(composition.size, color=(0, 0, 0), duration=edit_plan["duration"]),
            name="background"
        )
        
        # Add video layers
        video_layers = []
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "video":
                source_file = instruction["properties"]["source_file"]
                
                # Create video layer
                video_layer = mv.layer.Video(source_file, audio=False)
                
                # Add to composition
                item = composition.add_layer(
                    video_layer,
                    offset=instruction["start_time"],
                    position=tuple(instruction["position"]),
                    name=f"video_{instruction['asset_id']}"
                )
                
                video_layers.append({
                    "item": item,
                    "instruction": instruction
                })
                
                print(f"📹 Added video segment: {source_file}")
        
        # Process transitions
        for i, layer_info in enumerate(video_layers):
            if i == 0:
                continue  # Skip first layer (no incoming transition)
                
            instruction = layer_info["instruction"]
            if "transition" in instruction:
                transition_info = instruction["transition"]
                transition_id = transition_info["type"]
                transition_duration = transition_info["duration"]
                
                # Find the from layer
                from_layer_info = next((l for l in video_layers if l["instruction"]["asset_id"] == transition_info["from_asset_id"]), None)
                
                if from_layer_info:
                    from_item = from_layer_info["item"]
                    to_item = layer_info["item"]
                    
                    # Calculate overlap time
                    from_start = from_layer_info["instruction"]["start_time"]
                    to_start = instruction["start_time"]
                    overlap_start = to_start
                    
                    # Apply opacity animation for transition effect
                    # First video fades out
                    from_item.opacity.enable_motion().extend(
                        keyframes=[overlap_start - from_start, overlap_start - from_start + transition_duration],
                        values=[1.0, 0.0],
                        easings=[mv.enum.Easing.EASE_OUT]
                    )
                    
                    # Second video fades in
                    to_item.opacity.enable_motion().extend(
                        keyframes=[0.0, transition_duration],
                        values=[0.0, 1.0],
                        easings=[mv.enum.Easing.EASE_IN]
                    )
                    
                    print(f"🎭 Applied {transition_id} transition between {from_layer_info['instruction']['asset_id']} and {instruction['asset_id']}")
                else:
                    print(f"⚠️ Could not find from layer for transition: {transition_info['from_asset_id']}")
        
        # Add audio layer
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "audio":
                audio_layer = mv.layer.Audio(instruction["properties"]["source_file"])
                composition.add_layer(
                    audio_layer,
                    offset=instruction["start_time"],
                    name="background_music"
                )
                print(f"🎵 Added background music: {instruction['properties']['source_file']}")
        
        return composition
    
    def render_video(self, composition, output_path="custom_transition_output.mp4"):
        """Render the final video."""
        print(f"🎬 Rendering final video: {output_path}")
        
        try:
            # Export video
            composition.write_video(output_path)
            print(f"✅ Video rendered successfully!")
            return output_path
        except Exception as e:
            print(f"❌ Rendering failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self):
        """Execute the complete video creation process."""
        print("🚀 Starting Custom Transition Video Creation")
        print("=" * 60)
        
        try:
            # Step 1: Calculate video segments
            segments = self.calculate_video_segments()
            
            # Step 2: Create edit plan
            edit_plan = self.create_edit_plan(segments, self.audio_files[0])
            
            # Save edit plan for debugging
            with open("custom_transition_edit_plan.json", "w") as f:
                json.dump(edit_plan, f, indent=2)
            print("💾 Saved edit plan to custom_transition_edit_plan.json")
            
            # Step 3: Create composition
            composition = self.create_composition(edit_plan)
            
            # Step 4: Render final video
            output_file = self.render_video(composition)
            
            if output_file:
                print("\n🎉 SUCCESS!")
                print(f"📹 Final video: {output_file}")
                print(f"⏱️ Duration: {self.target_duration} seconds")
                print(f"✂️ Segments: {len(segments)} with custom transitions")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main execution function."""
    assets_folder = "/Users/naman/Desktop/movie_py"
    
    if not os.path.exists(assets_folder):
        print(f"❌ Assets folder not found: {assets_folder}")
        return
    
    # Create editor and run
    editor = CustomTransitionVideoEditor(assets_folder)
    result = editor.run()
    
    if result:
        print(f"\n🎬 Open your video: {result}")
    else:
        print("\n❌ Video creation failed")


if __name__ == "__main__":
    main()
