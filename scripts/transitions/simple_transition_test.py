#!/usr/bin/env python3
"""
Simplified Custom Transition Video Editor using Movis

This script creates a 10-second video with simple custom transitions between video segments.
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
from scripts.transitions.registry import TransitionRegistry


def create_simple_transition_video():
    """Create a simple video with custom transitions."""
    print("🚀 Creating simple video with custom transitions")
    
    # Initialize transition registry
    registry = TransitionRegistry()
    print(f"🎭 Available transitions: {registry.list_transitions()}")
    
    # Setup basic parameters
    duration = 10.0
    resolution = (1080, 1920)
    
    # Get media files
    media_dir = Path("/Users/naman/Desktop/movie_py/media")
    video_files = sorted(list(media_dir.glob("*.mp4")))[:3]  # Get first 3 videos
    audio_file = next(media_dir.glob("*.mp3"))
    
    print(f"📹 Using videos: {[v.name for v in video_files]}")
    print(f"🎵 Using audio: {audio_file.name}")
    
    # Create composition
    composition = mv.layer.Composition(size=resolution, duration=duration)
    
    # Add black background
    composition.add_layer(
        mv.layer.Rectangle(resolution, color=(0, 0, 0), duration=duration),
        name="background"
    )
    
    # Add three video segments with simple transitions
    segment_duration = duration / 3  # 3.33 seconds each
    
    # First video segment
    video1 = mv.layer.Video(str(video_files[0]), audio=False)
    composition.add_layer(
        video1,
        name="video1",
        offset=0.0,
        position=(resolution[0]//2, resolution[1]//2)
    )
    
    # Fade out first video at the end
    composition["video1"].opacity.enable_motion().extend(
        keyframes=[segment_duration - 0.5, segment_duration],
        values=[1.0, 0.0],
        easings=["ease_out"]
    )
    
    # Second video segment
    video2 = mv.layer.Video(str(video_files[1]), audio=False)
    composition.add_layer(
        video2,
        name="video2",
        offset=segment_duration - 0.5,  # Start during fade-out of first video
        position=(resolution[0]//2, resolution[1]//2),
        opacity=0.0  # Start invisible
    )
    
    # Fade in and out for second video
    composition["video2"].opacity.enable_motion().extend(
        keyframes=[0.0, 0.5, segment_duration - 0.5, segment_duration],
        values=[0.0, 1.0, 1.0, 0.0],
        easings=["ease_in", "linear", "ease_out"]
    )
    
    # Third video segment
    video3 = mv.layer.Video(str(video_files[2]), audio=False)
    composition.add_layer(
        video3,
        name="video3",
        offset=segment_duration * 2 - 0.5,  # Start during fade-out of second video
        position=(resolution[0]//2, resolution[1]//2),
        opacity=0.0  # Start invisible
    )
    
    # Fade in third video
    composition["video3"].opacity.enable_motion().extend(
        keyframes=[0.0, 0.5],
        values=[0.0, 1.0],
        easings=["ease_in"]
    )
    
    # Add background music
    audio = mv.layer.Audio(str(audio_file))
    composition.add_layer(
        audio,
        name="background_music",
        offset=0.0
    )
    
    # Render the video
    output_file = "simple_transition_output.mp4"
    print(f"🎬 Rendering video to {output_file}...")
    composition.write_video(output_file)
    print(f"✅ Video rendered successfully: {output_file}")
    
    return output_file


if __name__ == "__main__":
    try:
        output = create_simple_transition_video()
        print(f"\n🎉 SUCCESS! Video created: {output}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
