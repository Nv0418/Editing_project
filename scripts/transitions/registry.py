#!/usr/bin/env python3
"""
Transition Registry for Movis

This module implements a transition registry system that allows custom transitions
to be loaded from a directory structure and applied to videos in Movis.
"""

import os
import json
from pathlib import Path
import numpy as np
import cv2
import movis as mv


class TransitionRegistry:
    """Manages custom transitions for Movis video editing."""
    
    def __init__(self, transitions_dir="/Users/naman/Desktop/movie_py/transitions"):
        """Initialize the transition registry.
        
        Args:
            transitions_dir: Base directory containing transition packages
        """
        self.transitions_dir = Path(transitions_dir)
        self.transitions = {}
        self.categories = {}
        self._load_transitions()
    
    def _load_transitions(self):
        """Load all transitions from the transitions directory."""
        print(f"Loading transitions from {self.transitions_dir}")
        
        # Load each category directory
        for category_dir in self.transitions_dir.iterdir():
            if not category_dir.is_dir():
                continue
                
            # Load category index
            index_path = category_dir / "index.json"
            if not index_path.exists():
                print(f"Warning: No index.json found in {category_dir}")
                continue
                
            with open(index_path, "r") as f:
                category_info = json.load(f)
                
            # Store category info
            category_name = category_info.get("category", category_dir.name)
            self.categories[category_name] = category_info
            
            # Load each transition
            for trans_config_path in category_info.get("transitions", []):
                full_path = category_dir / trans_config_path
                if not full_path.exists():
                    print(f"Warning: Transition config not found: {full_path}")
                    continue
                    
                with open(full_path, "r") as f:
                    trans_config = json.load(f)
                    
                # Create transition entry
                trans_id = f"{category_name}/{full_path.parent.name}"
                trans_config["path"] = full_path.parent
                trans_config["category"] = category_name
                self.transitions[trans_id] = trans_config
                
        print(f"Loaded {len(self.transitions)} transitions in {len(self.categories)} categories")
    
    def get_transition(self, transition_id):
        """Get a transition by its ID.
        
        Args:
            transition_id: The ID of the transition (e.g., "distortion/transition_01")
            
        Returns:
            Transition config dict or None if not found
        """
        if transition_id not in self.transitions:
            print(f"Transition not found: {transition_id}")
            return None
            
        return self.transitions[transition_id]
    
    def list_transitions(self, category=None):
        """List available transitions, optionally filtered by category.
        
        Args:
            category: Optional category name to filter by
            
        Returns:
            List of transition IDs
        """
        if category:
            return [tid for tid in self.transitions.keys() if tid.startswith(f"{category}/")]
        return list(self.transitions.keys())
    
    def list_categories(self):
        """List available transition categories.
        
        Returns:
            List of category names
        """
        return list(self.categories.keys())


class DistortionTransitionEffect:
    """Effect for applying distortion transitions between two videos."""
    
    def __init__(self, transition_id, registry, duration=0.8):
        """Initialize the distortion transition effect.
        
        Args:
            transition_id: ID of the transition to use
            registry: TransitionRegistry instance
            duration: Duration of the transition in seconds
        """
        self.transition_id = transition_id
        self.registry = registry
        self.duration = duration
        self.transition = registry.get_transition(transition_id)
        
        if not self.transition:
            raise ValueError(f"Transition not found: {transition_id}")
            
        # Load transition assets
        self.assets = {}
        for asset_name, asset_file in self.transition.get("assets", {}).items():
            asset_path = self.transition["path"] / asset_file
            if asset_path.exists():
                self.assets[asset_name] = str(asset_path)
                
        if not self.assets:
            raise ValueError(f"No transition assets found for {transition_id}")
            
        print(f"Loaded transition {transition_id} with assets: {list(self.assets.keys())}")
        
    def __call__(self, prev_frame, time, **kwargs):
        """Apply the transition effect.
        
        Args:
            prev_frame: Previous frame from the composition
            time: Current time in seconds
            
        Returns:
            Processed frame
        """
        # This is a placeholder for the actual transition effect
        # In a real implementation, this would apply the distortion effect
        # based on the transition assets
        
        # Normalize time to 0-1 range for the transition
        norm_time = time / self.duration
        if norm_time > 1.0:
            norm_time = 1.0
        
        # For now, we'll just return the original frame
        # In a real implementation, you would apply the transition effect here
        return prev_frame


def apply_distortion_transition(composition, from_layer, to_layer, transition_id, overlap_duration=0.8):
    """Apply a distortion transition between two video layers.
    
    Args:
        composition: Movis composition
        from_layer: Layer to transition from
        to_layer: Layer to transition to
        transition_id: ID of the transition to use
        overlap_duration: Duration of the transition overlap
        
    Returns:
        Transition layer item
    """
    registry = TransitionRegistry()
    transition = registry.get_transition(transition_id)
    
    if not transition:
        raise ValueError(f"Transition not found: {transition_id}")
    
    # Get transition assets
    assets = {}
    for asset_name, asset_file in transition.get("assets", {}).items():
        asset_path = transition["path"] / asset_file
        if asset_path.exists():
            assets[asset_name] = str(asset_path)
    
    # Create transition composition
    trans_comp = mv.layer.Composition(composition.size, duration=overlap_duration)
    
    # Add both videos to the transition composition
    trans_comp.add_layer(from_layer, name="from_video")
    to_item = trans_comp.add_layer(to_layer, name="to_video")
    
    # Apply opacity animation to create a simple transition
    # In a real implementation, you would use the transition assets to create a more complex effect
    to_item.opacity.enable_motion().extend(
        keyframes=[0.0, overlap_duration],
        values=[0.0, 1.0],
        easings=[mv.enum.Easing.EASE_IN_OUT]
    )
    
    # Add a placeholder effect that will be replaced with the actual transition in the future
    # trans_comp.add_effect(DistortionTransitionEffect(transition_id, registry, overlap_duration))
    
    return trans_comp


def register_transition_in_edit_plan(edit_plan, transition_id, from_idx, to_idx, duration=0.8):
    """Register a transition in an edit plan between two video segments.
    
    Args:
        edit_plan: Edit plan dict
        transition_id: ID of the transition to use
        from_idx: Index of the from video in instructions
        to_idx: Index of the to video in instructions
        duration: Duration of the transition
        
    Returns:
        Updated edit plan
    """
    instructions = edit_plan.get("instructions", [])
    
    if from_idx < 0 or from_idx >= len(instructions) or to_idx < 0 or to_idx >= len(instructions):
        raise ValueError(f"Invalid from_idx or to_idx: {from_idx}, {to_idx}")
    
    from_instr = instructions[from_idx]
    to_instr = instructions[to_idx]
    
    if from_instr.get("type") != "video" or to_instr.get("type") != "video":
        raise ValueError("From and to instructions must be videos")
    
    # Add transition to the to_instruction
    to_instr["transition"] = {
        "type": transition_id,
        "duration": duration,
        "from_asset_id": from_instr["asset_id"]
    }
    
    return edit_plan


# Example usage:
"""
# Load registry
registry = TransitionRegistry()

# List available transitions
print(registry.list_transitions())

# Create a composition
composition = mv.layer.Composition((1920, 1080), duration=10.0)

# Add video layers
video1 = mv.layer.Video("video1.mp4")
video2 = mv.layer.Video("video2.mp4")

# Apply transition
transition_comp = apply_distortion_transition(
    composition, video1, video2, "distortion/transition_01", 0.8)
    
# Add transition to main composition
composition.add_layer(transition_comp, offset=4.0, name="transition")
"""
