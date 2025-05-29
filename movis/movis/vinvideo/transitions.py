"""
Smart Transitions for VinVideo

Implements intelligent transitions that can be automatically selected
by AI agents based on content analysis and cinematographic principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import numpy as np
import movis as mv


class SmartTransition(ABC):
    """Base class for AI-selectable transitions."""
    
    def __init__(self, duration: float = 1.0):
        self.duration = duration
    
    @abstractmethod
    def apply(self, layer_a: mv.layer.BasicLayer, layer_b: mv.layer.BasicLayer,
              composition: mv.layer.Composition, crossover_time: float) -> None:
        """Apply transition between two layers."""
        pass
    
    @property
    @abstractmethod
    def transition_type(self) -> str:
        """Return the type name of this transition."""
        pass


class CrossFadeTransition(SmartTransition):
    """Standard cross-fade transition."""
    
    @property
    def transition_type(self) -> str:
        return "crossfade"
    
    def apply(self, layer_a: mv.layer.BasicLayer, layer_b: mv.layer.BasicLayer,
              composition: mv.layer.Composition, crossover_time: float) -> None:
        """Apply cross-fade between layers."""
        
        # Add layer A with fade out
        item_a = composition.add_layer(layer_a, offset=0.0)
        item_a.opacity.enable_motion().extend(
            keyframes=[crossover_time - self.duration/2, crossover_time + self.duration/2],
            values=[1.0, 0.0],
            easings=['ease_in_out']
        )
        
        # Add layer B with fade in
        item_b = composition.add_layer(layer_b, offset=crossover_time - self.duration/2)
        item_b.opacity.enable_motion().extend(
            keyframes=[0.0, self.duration],
            values=[0.0, 1.0],
            easings=['ease_in_out']
        )


class SlideTransition(SmartTransition):
    """Slide transition with configurable direction."""
    
    def __init__(self, duration: float = 1.0, direction: str = "left"):
        super().__init__(duration)
        self.direction = direction  # "left", "right", "up", "down"
    
    @property
    def transition_type(self) -> str:
        return f"slide_{self.direction}"
    
    def apply(self, layer_a: mv.layer.BasicLayer, layer_b: mv.layer.BasicLayer,
              composition: mv.layer.Composition, crossover_time: float) -> None:
        """Apply slide transition."""
        
        size = composition.size
        
        # Direction vectors
        directions = {
            "left": (-size[0], 0),
            "right": (size[0], 0),
            "up": (0, -size[1]),
            "down": (0, size[1])
        }
        
        offset_x, offset_y = directions.get(self.direction, (0, 0))
        
        # Add layer A - slides out
        item_a = composition.add_layer(layer_a, offset=0.0)
        item_a.position.enable_motion().extend(
            keyframes=[crossover_time, crossover_time + self.duration],
            values=[(size[0]//2, size[1]//2), (size[0]//2 + offset_x, size[1]//2 + offset_y)],
            easings=['ease_in_out']
        )
        
        # Add layer B - slides in
        item_b = composition.add_layer(layer_b, offset=crossover_time,
                                     position=(size[0]//2 - offset_x, size[1]//2 - offset_y))
        item_b.position.enable_motion().extend(
            keyframes=[0.0, self.duration],
            values=[(size[0]//2 - offset_x, size[1]//2 - offset_y), (size[0]//2, size[1]//2)],
            easings=['ease_in_out']
        )


def select_smart_transition(
    content_a_type: str,
    content_b_type: str,
    mood_change: str = "neutral",
    pacing: str = "medium"
) -> SmartTransition:
    """
    AI-assisted transition selection based on content analysis.
    
    Args:
        content_a_type: Type of first content ("action", "dialogue", "landscape", etc.)
        content_b_type: Type of second content
        mood_change: Change in mood ("neutral", "intensify", "calm", "dramatic")
        pacing: Desired pacing ("slow", "medium", "fast")
    """
    
    # Duration based on pacing
    duration_map = {"slow": 2.0, "medium": 1.0, "fast": 0.5}
    duration = duration_map.get(pacing, 1.0)
    
    # Transition selection logic (simplified)
    if mood_change == "dramatic":
        return CrossFadeTransition(duration * 1.5)  # Longer for drama
    elif content_a_type == "action" and content_b_type == "dialogue":
        return SlideTransition(duration, "down")  # Action to calm
    elif content_a_type == "landscape" and content_b_type == "action":
        return SlideTransition(duration, "up")  # Build energy
    else:
        return CrossFadeTransition(duration)  # Default safe choice
