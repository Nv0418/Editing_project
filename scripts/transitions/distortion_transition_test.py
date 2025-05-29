#!/usr/bin/env python3
"""
Custom Distortion Transition Video Editor using Movis

This script creates a 10-second video with distortion transitions between video segments.
"""

import os
import sys
import json
import cv2
import numpy as np
from pathlib import Path

# Add the modified movis to path
sys.path.insert(0, '/Users/naman/Desktop/movie_py/movis')

import movis as mv
# Import our custom transition registry
sys.path.insert(0, '/Users/naman/Desktop/movie_py')
from scripts.transitions.registry import TransitionRegistry


class DistortionTransitionEffect:
    """Effect to apply a distortion transition between videos."""
    
    def __init__(self, transition_path, transition_progress=0.0):
        """Initialize with transition mask images.
        
        Args:
            transition_path: Path to the transition directory
            transition_progress: Value between 0.0 and 1.0 representing transition progress
        """
        self.transition_path = Path(transition_path)
        self.transition_progress = transition_progress
        
        # Load transition masks
        self.mask_a = cv2.imread(str(self.transition_path / "mask_a.jpg"))
        self.mask_b = cv2.imread(str(self.transition_path / "mask_b.jpg"))
        
        if self.mask_a is None or self.mask_b is None:
            raise ValueError(f"Could not load transition masks from {self.transition_path}")
        
        # Convert to RGB
        self.mask_a = cv2.cvtColor(self.mask_a, cv2.COLOR_BGR2RGB)
        self.mask_b = cv2.cvtColor(self.mask_b, cv2.COLOR_BGR2RGB)
        
        print(f"✅ Loaded transition masks from {self.transition_path}")
    
    def __call__(self, image, time, **kwargs):
        """Apply distortion transition effect.
        
        Args:
            image: Input image (numpy array, RGBA)
            time: Current time
            
        Returns:
            Processed image
        """
        # Resize masks to match input image
        h, w = image.shape[:2]
        mask_a = cv2.resize(self.mask_a, (w, h))
        mask_b = cv2.resize(self.mask_b, (w, h))
        
        # Use time parameter to blend between the two masks
        blend_factor = min(1.0, max(0.0, time))
        mask = cv2.addWeighted(mask_a, 1.0 - blend_factor, mask_b, blend_factor, 0)
        
        # Apply the mask (simple alpha blending)
        # In a real implementation, this would use more sophisticated distortion effects
        mask = mask.astype(np.float32) / 255.0
        image_rgb = image[:, :, :3].astype(np.float32) / 255.0
        alpha = image[:, :, 3:4].astype(np.float32) / 255.0
        
        # Simple masking effect
        result_rgb = image_rgb * mask
        result = np.concatenate([result_rgb, alpha], axis=2)
        
        return (result * 255).astype(np.uint8)


def create_distortion_transition_video():
    """Create a video with custom distortion transitions."""
    print("🚀 Creating video with distortion transitions")
    
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
    
    # Add three video segments with transitions
    segment_duration = duration / 3  # 3.33 seconds each
    
    # First video segment
    video1 = mv.layer.Video(str(video_files[0]), audio=False)
    v1_item = composition.add_layer(
        video1,
        name="video1",
        offset=0.0,
        position=(resolution[0]//2, resolution[1]//2)
    )
    
    # Add transition to first video
    transition1 = registry.get_transition("distortion/transition_01")
    if transition1:
        # Apply opacity animation for transition
        v1_item.opacity.enable_motion().extend(
            keyframes=[0.0, segment_duration - 0.5, segment_duration],
            values=[1.0, 1.0, 0.0],
            easings=["linear", "ease_out"]
        )
        
        # Apply distortion effect to the layer
        v1_item.add_effect(DistortionTransitionEffect(transition1["path"]))
    
    # Second video segment
    video2 = mv.layer.Video(str(video_files[1]), audio=False)
    v2_item = composition.add_layer(
        video2,
        name="video2",
        offset=segment_duration - 0.5,  # Start during transition
        position=(resolution[0]//2, resolution[1]//2),
        opacity=0.0  # Start invisible
    )
    
    # Add transition to second video
    transition2 = registry.get_transition("distortion/transition_02")
    if transition2:
        # Apply opacity animation for both transitions
        v2_item.opacity.enable_motion().extend(
            keyframes=[0.0, 0.5, segment_duration - 0.5, segment_duration],
            values=[0.0, 1.0, 1.0, 0.0],
            easings=["ease_in", "linear", "ease_out"]
        )
        
        # Apply distortion effect to the layer
        v2_item.add_effect(DistortionTransitionEffect(transition2["path"]))
    
    # Third video segment
    video3 = mv.layer.Video(str(video_files[2]), audio=False)
    v3_item = composition.add_layer(
        video3,
        name="video3",
        offset=segment_duration * 2 - 0.5,  # Start during transition
        position=(resolution[0]//2, resolution[1]//2),
        opacity=0.0  # Start invisible
    )
    
    # Add transition to third video
    transition3 = registry.get_transition("distortion/transition_03")
    if transition3:
        # Apply opacity animation for transition
        v3_item.opacity.enable_motion().extend(
            keyframes=[0.0, 0.5, segment_duration],
            values=[0.0, 1.0, 1.0],
            easings=["ease_in", "linear"]
        )
        
        # Apply distortion effect to the layer
        v3_item.add_effect(DistortionTransitionEffect(transition3["path"]))
    
    # Add background music
    audio = mv.layer.Audio(str(audio_file))
    composition.add_layer(
        audio,
        name="background_music",
        offset=0.0
    )
    
    # Render the video
    output_file = "distortion_transition_output.mp4"
    print(f"🎬 Rendering video to {output_file}...")
    composition.write_video(output_file)
    print(f"✅ Video rendered successfully: {output_file}")
    
    return output_file


if __name__ == "__main__":
    try:
        output = create_distortion_transition_video()
        print(f"\n🎉 SUCCESS! Video created: {output}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
