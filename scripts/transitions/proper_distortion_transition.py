#!/usr/bin/env python3
"""
Proper Distortion Transition Editor for Movis

This script implements proper distortion-based transitions using displacement maps
from Final Cut Pro transition packs without overlaying any text or graphics.
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


class ProperDistortionTransitionEffect:
    """Effect to apply a proper distortion transition between videos using displacement maps."""
    
    def __init__(self, transition_path, max_displacement=15.0, noise_level=0.2):
        """Initialize with transition displacement maps.
        
        Args:
            transition_path: Path to the transition directory
            max_displacement: Maximum pixel displacement (default: 15.0)
            noise_level: Random noise factor for displacement (default: 0.2)
        """
        self.transition_path = Path(transition_path)
        self.max_displacement = max_displacement
        self.noise_level = noise_level
        
        # Load transition masks as displacement maps only
        self.mask_a = cv2.imread(str(self.transition_path / "mask_a.jpg"))
        self.mask_b = cv2.imread(str(self.transition_path / "mask_b.jpg"))
        
        if self.mask_a is None or self.mask_b is None:
            raise ValueError(f"Could not load transition masks from {self.transition_path}")
        
        # Convert masks to grayscale for displacement maps
        self.map_a = cv2.cvtColor(self.mask_a, cv2.COLOR_BGR2GRAY)
        self.map_b = cv2.cvtColor(self.mask_b, cv2.COLOR_BGR2GRAY)
        
        print(f"✅ Loaded displacement maps from {self.transition_path}")
    
    def __call__(self, frame, time, **kwargs):
        """Apply distortion transition effect using displacement maps.
        
        Args:
            frame: Input frame (numpy array, RGBA)
            time: Current time (0.0 to 1.0)
            
        Returns:
            Processed frame with distortion effect
        """
        # We don't actually use time here since we're not animating between masks
        # In a real implementation, you would use time to blend between mask_a and mask_b
        
        # Get frame dimensions
        h, w = frame.shape[:2]
        
        # Resize displacement map to match frame size
        map_resized = cv2.resize(self.map_a, (w, h))
        
        # Create output frame
        result = frame.copy()
        
        # Calculate appropriate distortion amount based on time
        # Use a sine curve to ramp up and down the effect
        progress = np.sin(time * np.pi) 
        distortion_amount = self.max_displacement * progress
        
        # Apply distortion using the displacement map
        # This is a simplified version - a full implementation would use proper optical flow
        for y in range(0, h, 2):  # Skip pixels for performance
            for x in range(0, w, 2):
                # Get displacement amount from map (0-255 value)
                displacement = (map_resized[y, x] / 255.0) * distortion_amount
                
                # Add some randomness for more natural effect
                noise_x = np.random.uniform(-self.noise_level, self.noise_level) * displacement
                noise_y = np.random.uniform(-self.noise_level, self.noise_level) * displacement
                
                # Calculate source coordinates with displacement
                src_x = int(max(0, min(w-1, x + displacement + noise_x)))
                src_y = int(max(0, min(h-1, y + displacement + noise_y)))
                
                # Copy pixel
                if 0 <= y < h and 0 <= x < w and 0 <= src_y < h and 0 <= src_x < w:
                    result[y, x] = frame[src_y, src_x]
        
        # For a proper implementation, we would blend original frame with distorted frame
        # based on alpha values and transition progress
        
        return result


def create_distortion_transition_video():
    """Create a video with proper distortion transitions."""
    print("🚀 Creating video with proper distortion transitions")
    
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
        
        # Apply proper distortion effect to the layer
        v1_item.add_effect(ProperDistortionTransitionEffect(
            transition1["path"], 
            max_displacement=20.0,  # Adjust for desired effect strength
            noise_level=0.3
        ))
    
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
        
        # Apply proper distortion effect to the layer
        v2_item.add_effect(ProperDistortionTransitionEffect(
            transition2["path"],
            max_displacement=25.0,
            noise_level=0.4
        ))
    
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
        
        # Apply proper distortion effect to the layer
        v3_item.add_effect(ProperDistortionTransitionEffect(
            transition3["path"],
            max_displacement=30.0,
            noise_level=0.5
        ))
    
    # Add background music
    audio = mv.layer.Audio(str(audio_file))
    composition.add_layer(
        audio,
        name="background_music",
        offset=0.0
    )
    
    # Render the video
    output_file = "proper_distortion_transition.mp4"
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
