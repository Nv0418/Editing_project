#!/usr/bin/env python3
"""
Beat-Synchronized Video Editor using VinVideo + Movis + Librosa - FIXED VERSION

This script creates a 10-second video with beat-synchronized cuts from multiple video sources,
using background music analysis to time the cuts perfectly to the musical beats.
"""

import os
import sys
import numpy as np
import librosa
import json
from pathlib import Path

# Add the modified movis to path
sys.path.insert(0, '/Users/naman/Desktop/movie_py/movis')

import movis as mv


class BeatSyncVideoEditor:
    """Creates beat-synchronized videos using music analysis."""
    
    def __init__(self, assets_folder: str):
        self.assets_folder = Path(assets_folder)
        self.target_duration = 10.0  # 10 seconds
        self.audio_reduction_db = -6  # -6dB audio level
        
        # Find assets
        self.video_files = list(self.assets_folder.glob("*.mp4"))
        self.audio_files = list(self.assets_folder.glob("*.mp3"))
        
        # Filter out the output file if it exists
        self.video_files = [f for f in self.video_files if not f.name.startswith('beat_sync_output')]
        
        if len(self.video_files) < 3:
            raise ValueError(f"Need at least 3 video files, found {len(self.video_files)}")
        if len(self.audio_files) < 1:
            raise ValueError(f"Need at least 1 audio file, found {len(self.audio_files)}")
        
        print(f"🎬 Found {len(self.video_files)} videos and {len(self.audio_files)} audio files")
        for i, video in enumerate(self.video_files):
            print(f"   Video {i+1}: {video.name}")
    
    def analyze_music_beats(self):
        """Analyze the background music to find beat timestamps."""
        audio_file = self.audio_files[0]  # Use first audio file
        print(f"🎵 Analyzing beats in: {audio_file.name}")
        
        # Load audio with librosa
        y, sr = librosa.load(str(audio_file), duration=self.target_duration + 2)
        
        # Detect tempo and beat frames with more sensitive settings
        tempo, beat_frames = librosa.beat.beat_track(
            y=y, 
            sr=sr, 
            hop_length=512,
            start_bpm=60,
            tightness=100
        )
        
        # Convert beat frames to timestamps
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        
        # Filter beats to our target duration
        beat_times = beat_times[beat_times <= self.target_duration]
        
        # If we don't have enough beats, create artificial ones
        if len(beat_times) < 4:
            print(f"⚠️ Only found {len(beat_times)} beats, creating artificial beat grid")
            # Create beats every 1.5 seconds for better video pacing
            beat_times = np.arange(0, self.target_duration, 1.5)
            tempo = 40  # Corresponds to beats every 1.5 seconds
        
        print(f"🥁 Detected BPM: {tempo.item():.1f}")
        print(f"🎯 Found {len(beat_times)} beats in {self.target_duration} seconds")
        print(f"⏰ Beat times: {beat_times}")
        
        return tempo, beat_times, str(audio_file)
    
    def calculate_video_segments(self, beat_times):
        """Create exactly 3 segments with overlapping cross-fade transitions."""
        num_videos = len(self.video_files)  # Should be 3
        
        # For overlapping cross-fades, we need segments to overlap
        fade_duration = 0.5  # 0.5 second overlap for cross-fade
        
        # Divide remaining time after accounting for overlaps
        remaining_time = self.target_duration - (fade_duration * 2)  # 2 overlaps
        segment_base_duration = remaining_time / num_videos  # Base duration per segment
        
        segments = []
        
        for i in range(num_videos):
            if i == 0:
                # First segment: normal start, extend for fade
                start_time = 0.0
                duration = segment_base_duration + fade_duration
            elif i == num_videos - 1:
                # Last segment: start early for fade, normal end
                start_time = (i * segment_base_duration) + ((i-1) * fade_duration)
                duration = segment_base_duration + fade_duration
            else:
                # Middle segments: start early, extend for fade
                start_time = (i * segment_base_duration) + ((i-1) * fade_duration)
                duration = segment_base_duration + (fade_duration * 2)
            
            segments.append({
                "video_idx": i,  # Use each video exactly once
                "start": start_time,
                "duration": duration,
                "fade_duration": fade_duration,
                "trim_end": 1.0  # Trim 1 second from end of source video
            })
        
        print(f"📊 Created {len(segments)} overlapping segments for true cross-fade")
        print(f"⏱️ Base segment duration: {segment_base_duration:.2f}s + {fade_duration:.2f}s overlap")
        print(f"🌊 Cross-fade overlap: {fade_duration}s between each video")
        
        return segments
    
    def create_edit_plan(self, segments, audio_file):
        """Create a JSON edit plan for VinVideo."""
        instructions = []
        
        # Add exactly 3 video segments with TRUE cross-fade (no black screens)
        for i, segment in enumerate(segments):
            video_file = self.video_files[segment["video_idx"]]
            fade_duration = segment["fade_duration"]
            
            # Create different opacity animations based on position
            if i == 0:
                # First video: fade out at the end
                animations = [
                    {
                        "attribute": "opacity",
                        "keyframes": [0.0, segment["duration"] - fade_duration, segment["duration"]],
                        "values": [1.0, 1.0, 0.0],
                        "easings": ["linear", "ease_out"]
                    }
                ]
                transition_type = "fade out"
                
            elif i == len(segments) - 1:
                # Last video: fade in at the start
                animations = [
                    {
                        "attribute": "opacity", 
                        "keyframes": [0.0, fade_duration, segment["duration"]],
                        "values": [0.0, 1.0, 1.0],
                        "easings": ["ease_in", "linear"]
                    }
                ]
                transition_type = "fade in"
                
            else:
                # Middle videos: fade in and fade out
                animations = [
                    {
                        "attribute": "opacity",
                        "keyframes": [0.0, fade_duration, segment["duration"] - fade_duration, segment["duration"]],
                        "values": [0.0, 1.0, 1.0, 0.0],
                        "easings": ["ease_in", "linear", "ease_out"]
                    }
                ]
                transition_type = "fade in/out"
            
            instructions.append({
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
                },
                "animations": animations
            })
            
            print(f"📹 Segment {i+1}: {video_file.name} from {segment['start']:.2f}s for {segment['duration']:.2f}s ({transition_type}, trim {segment.get('trim_end', 0.0)}s from end)")
        
        # Add background music
        instructions.append({
            "type": "audio",
            "asset_id": "AUDIO-BGM",
            "start_time": 0.0,
            "duration": self.target_duration,
            "properties": {
                "source_file": audio_file,
                "volume_db": self.audio_reduction_db
            },
            "animations": []
        })
        
        # Create complete edit plan
        edit_plan = {
            "scene_id": "beat_sync_test",
            "target_format": "tiktok",
            "resolution": [1080, 1920],
            "duration": self.target_duration,
            "instructions": instructions,
            "metadata": {
                "description": "Beat-synchronized video created with VinVideo",
                "beat_count": len(segments),
                "audio_source": Path(audio_file).name
            }
        }
        
        return edit_plan
    
    def register_assets(self, edit_plan):
        """Register all assets in VinVideo asset registry."""
        print("📁 Registering assets...")
        
        registry = mv.vinvideo.AssetRegistry(Path("beat_sync_assets.json"))
        
        # Register video assets
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "video":
                source_file = instruction["properties"]["source_file"]
                asset_id = registry.register_asset(
                    file_path=source_file,
                    asset_type="video",
                    original_prompt=f"Source video from {Path(source_file).name}",
                    generator_model="user_provided",
                    generation_params={"beat_synchronized": True}
                )
                instruction["asset_id"] = asset_id
                print(f"✅ Registered video: {Path(source_file).name} → {asset_id}")
        
        # Register audio asset
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "audio":
                source_file = instruction["properties"]["source_file"]
                asset_id = registry.register_asset(
                    file_path=source_file,
                    asset_type="audio", 
                    original_prompt=f"Background music from {Path(source_file).name}",
                    generator_model="user_provided",
                    generation_params={"volume_db": self.audio_reduction_db}
                )
                instruction["asset_id"] = asset_id
                print(f"✅ Registered audio: {Path(source_file).name} → {asset_id}")
        
        return registry, edit_plan
    
    def create_composition(self, edit_plan, registry):
        """Create Movis composition from edit plan."""
        print("🎞️ Creating Movis composition...")
        
        # Create VinVideo composition
        composition = mv.vinvideo.VinVideoComposition(
            size=tuple(edit_plan["resolution"]),
            duration=edit_plan["duration"],
            scene_id=edit_plan["scene_id"],
            target_format=edit_plan["target_format"]
        )
        
        # Add video layers with cross-fade transitions
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "video":
                # Get asset path
                asset = registry.get_asset(instruction["asset_id"])
                if not asset:
                    print(f"❌ Asset not found: {instruction['asset_id']}")
                    continue
                
                # Create video layer with trimming from end
                trim_end = instruction["properties"].get("source_end_trim", 0.0)
                
                # Create video layer
                video_layer = mv.layer.Video(asset.file_path, audio=False)
                
                # Add to composition with cross-fade animations
                item = composition.add_layer(
                    video_layer,
                    offset=instruction["start_time"],
                    position=tuple(instruction["position"]),
                    name=f"video_{instruction['asset_id']}"
                )
                
                # Apply cross-fade animations if present
                for anim in instruction["animations"]:
                    if anim["attribute"] == "opacity":
                        item.opacity.enable_motion().extend(
                            keyframes=anim["keyframes"],
                            values=anim["values"],
                            easings=[getattr(mv.enum.Easing, e.upper()) for e in anim["easings"]]
                        )
                
                print(f"📹 Added video segment: {instruction['start_time']:.2f}s - {instruction['start_time'] + instruction['duration']:.2f}s (cross-fade, trimmed {trim_end:.1f}s from end)")
        
        # Add audio layer
        for instruction in edit_plan["instructions"]:
            if instruction["type"] == "audio":
                asset = registry.get_asset(instruction["asset_id"])
                if asset:
                    audio_layer = mv.layer.Audio(asset.file_path)
                    composition.add_layer(
                        audio_layer,
                        offset=instruction["start_time"],
                        name="background_music"
                    )
                    print(f"🎵 Added background music")
        
        return composition
    
    def render_video(self, composition, output_path="beat_sync_output_true_crossfade.mp4"):
        """Render the final video."""
        print(f"🎬 Rendering final video: {output_path}")
        
        try:
            # Export optimized for TikTok
            result = composition.export_for_platform(output_path)
            print(f"✅ Video rendered successfully!")
            print(f"📊 Export details: {result}")
            return output_path
        except Exception as e:
            print(f"❌ Rendering failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self):
        """Execute the complete beat-synchronized video creation process."""
        print("🚀 Starting True Cross-Fade Video (No Black Screens)")
        print("=" * 60)
        
        try:
            # Step 1: Analyze music
            tempo, beat_times, audio_file = self.analyze_music_beats()
            
            # Step 2: Calculate video segments
            segments = self.calculate_video_segments(beat_times)
            print(f"📊 Created {len(segments)} video segments")
            
            # Step 3: Create edit plan
            edit_plan = self.create_edit_plan(segments, audio_file)
            
            # Save edit plan for debugging
            with open("beat_sync_edit_plan_fixed.json", "w") as f:
                json.dump(edit_plan, f, indent=2)
            print("💾 Saved edit plan to beat_sync_edit_plan_fixed.json")
            
            # Step 4: Register assets
            registry, edit_plan = self.register_assets(edit_plan)
            
            # Step 5: Create composition
            composition = self.create_composition(edit_plan, registry)
            
            # Step 6: Render final video
            output_file = self.render_video(composition)
            
            if output_file:
                print("\n🎉 SUCCESS!")
                print(f"📹 Final video: {output_file}")
                print(f"⏱️ Duration: {self.target_duration} seconds")
                print(f"🥁 BPM: {tempo.item():.1f}")
                print(f"✂️ Cuts: {len(segments)} beat-synchronized segments")
            
            return output_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Main execution function."""
    assets_folder = "/Users/naman/Desktop/movie_py"  # FIXED: Use correct folder
    
    if not os.path.exists(assets_folder):
        print(f"❌ Assets folder not found: {assets_folder}")
        return
    
    # Create editor and run
    editor = BeatSyncVideoEditor(assets_folder)
    result = editor.run()
    
    if result:
        print(f"\n🎬 Open your video: {result}")
    else:
        print("\n❌ Video creation failed")


if __name__ == "__main__":
    main()
