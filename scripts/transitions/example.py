#!/usr/bin/env python3
"""
Example script demonstrating how to use custom distortion transitions with Movis.
"""

import sys
import json
from pathlib import Path

# Add the movie_py directory to path
sys.path.insert(0, '/Users/naman/Desktop/movie_py')

import movis as mv
from scripts.transitions.registry import TransitionRegistry, apply_distortion_transition


def create_example_with_transitions():
    """Create an example video using distortion transitions."""
    # Initialize transition registry
    registry = TransitionRegistry()
    
    # List available transitions
    print("Available transition categories:")
    for category in registry.list_categories():
        print(f"  - {category}")
    
    print("\nAvailable transitions:")
    for transition_id in registry.list_transitions():
        print(f"  - {transition_id}")
    
    # Create a composition
    composition = mv.layer.Composition(size=(1080, 1920), duration=10.0)
    
    # Add background
    composition.add_layer(
        mv.layer.Rectangle(composition.size, color=(0, 0, 0), duration=10.0),
        name='background'
    )
    
    # Add sample videos (use your actual video paths)
    video_paths = [
        "/Users/naman/Desktop/movie_py/media/comfyuiblog_00004.mp4",
        "/Users/naman/Desktop/movie_py/media/comfyuiblog_00005.mp4",
        "/Users/naman/Desktop/movie_py/media/comfyuiblog_00006.mp4"
    ]
    
    # Add first video segment
    video1 = mv.layer.Video(video_paths[0], audio=False)
    composition.add_layer(
        video1,
        name="video1",
        offset=0.0,
        position=(540, 960),
        duration=4.0
    )
    
    # Add second video segment
    video2 = mv.layer.Video(video_paths[1], audio=False)
    composition.add_layer(
        video2,
        name="video2",
        offset=3.5,  # Overlap for transition
        position=(540, 960),
        opacity=0.0  # Start invisible
    )
    
    # Animate opacity for second video (simple fade in)
    composition["video2"].opacity.enable_motion().extend(
        keyframes=[0.0, 0.5],
        values=[0.0, 1.0],
        easings=["ease_in_out"]
    )
    
    # Add third video segment
    video3 = mv.layer.Video(video_paths[2], audio=False)
    composition.add_layer(
        video3,
        name="video3",
        offset=7.0,  # Overlap for transition
        position=(540, 960),
        opacity=0.0  # Start invisible
    )
    
    # Animate opacity for third video (simple fade in)
    composition["video3"].opacity.enable_motion().extend(
        keyframes=[0.0, 0.5],
        values=[0.0, 1.0],
        easings=["ease_in_out"]
    )
    
    # Add background music
    audio = mv.layer.Audio("/Users/naman/Desktop/movie_py/media/Sad Emotional Piano Music - Background Music (HD).mp3")
    composition.add_layer(
        audio,
        name="background_music",
        offset=0.0
    )
    
    # Create edit plan (for reference)
    edit_plan = {
        "scene_id": "distortion_transition_example",
        "target_format": "tiktok",
        "resolution": [1080, 1920],
        "duration": 10.0,
        "instructions": [
            {
                "type": "video",
                "asset_id": "VIDEO-001",
                "start_time": 0.0,
                "duration": 4.0,
                "position": [540, 960],
                "scale": [1.0, 1.0],
                "opacity": 1.0,
                "properties": {
                    "source_file": video_paths[0]
                }
            },
            {
                "type": "video",
                "asset_id": "VIDEO-002",
                "start_time": 3.5,
                "duration": 4.0,
                "position": [540, 960],
                "scale": [1.0, 1.0],
                "opacity": 1.0,
                "properties": {
                    "source_file": video_paths[1]
                },
                "transition": {
                    "type": "distortion/transition_01",
                    "duration": 0.5,
                    "from_asset_id": "VIDEO-001"
                }
            },
            {
                "type": "video",
                "asset_id": "VIDEO-003",
                "start_time": 7.0,
                "duration": 3.0,
                "position": [540, 960],
                "scale": [1.0, 1.0],
                "opacity": 1.0,
                "properties": {
                    "source_file": video_paths[2]
                },
                "transition": {
                    "type": "distortion/transition_02",
                    "duration": 0.5,
                    "from_asset_id": "VIDEO-002"
                }
            },
            {
                "type": "audio",
                "asset_id": "AUDIO-001",
                "start_time": 0.0,
                "duration": 10.0,
                "properties": {
                    "source_file": "/Users/naman/Desktop/movie_py/media/Sad Emotional Piano Music - Background Music (HD).mp3",
                    "volume_db": -6
                }
            }
        ]
    }
    
    # Save edit plan for reference
    with open("distortion_transition_example.json", "w") as f:
        json.dump(edit_plan, f, indent=2)
    
    # Render the video
    print("Rendering video...")
    composition.write_video("distortion_transition_example.mp4")
    print("Done! Video saved as distortion_transition_example.mp4")


if __name__ == "__main__":
    create_example_with_transitions()
