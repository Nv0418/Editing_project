"""
AI Agent to Movis Translation Layer

This module handles converting AI agent edit plans (JSON) into executable Movis code.
Designed specifically for VinVideo's multi-agent architecture.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field

import movis as mv
from ..layer.composition import Composition
from ..motion import Motion
from ..enum import Easing, BlendingMode
from .asset_registry import AssetRegistry


@dataclass
class EditInstruction:
    """Single editing instruction from AI agents."""
    type: str  # 'video', 'image', 'text', 'transition', 'effect'
    asset_id: Optional[str] = None
    start_time: float = 0.0
    end_time: Optional[float] = None
    duration: Optional[float] = None
    position: Optional[tuple[float, float]] = None
    scale: Optional[tuple[float, float]] = None
    opacity: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)
    animations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class EditPlan:
    """Complete edit plan from Director/DoP agents."""
    scene_id: str
    target_format: str  # 'tiktok', 'instagram_reel', 'youtube_short'
    resolution: tuple[int, int]
    duration: float
    instructions: List[EditInstruction]
    metadata: Dict[str, Any] = field(default_factory=dict)


class EditPlanParser:
    """Converts AI agent edit plans into Movis compositions."""
    
    def __init__(self, asset_registry: AssetRegistry):
        self.asset_registry = asset_registry
        self._layer_factories = {
            'video': self._create_video_layer,
            'image': self._create_image_layer, 
            'text': self._create_text_layer,
            'shape': self._create_shape_layer,
            'audio': self._create_audio_layer
        }
        self._easing_map = {
            'linear': Easing.LINEAR,
            'ease_in': Easing.EASE_IN,
            'ease_out': Easing.EASE_OUT,
            'ease_in_out': Easing.EASE_IN_OUT,
            'ease_in_out3': Easing.EASE_IN_OUT3,
            'ease_in_out5': Easing.EASE_IN_OUT5
        }
    
    def parse_json_plan(self, plan_json: str | Path) -> EditPlan:
        """Parse JSON edit plan from file or string."""
        if isinstance(plan_json, Path):
            with open(plan_json, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(plan_json)
        
        instructions = [
            EditInstruction(**instr) for instr in data.get('instructions', [])
        ]
        
        return EditPlan(
            scene_id=data['scene_id'],
            target_format=data['target_format'],
            resolution=tuple(data['resolution']),
            duration=data['duration'],
            instructions=instructions,
            metadata=data.get('metadata', {})
        )
    
    def execute_plan(self, plan: EditPlan) -> 'VinVideoComposition':
        """Convert edit plan to executable Movis composition."""
        composition = VinVideoComposition(
            size=plan.resolution,
            duration=plan.duration,
            scene_id=plan.scene_id,
            target_format=plan.target_format
        )
        
        # Sort instructions by start time for proper layering
        sorted_instructions = sorted(plan.instructions, key=lambda x: x.start_time)
        
        for instruction in sorted_instructions:
            layer = self._create_layer(instruction)
            if layer is None:
                continue
                
            # Add layer to composition
            item = composition.add_layer(
                layer,
                offset=instruction.start_time,
                position=instruction.position,
                opacity=instruction.opacity,
                name=instruction.asset_id or f"{instruction.type}_{len(composition)}"
            )
            
            # Apply animations
            self._apply_animations(item, instruction.animations)
            
        return composition
    
    def _create_layer(self, instruction: EditInstruction):
        """Factory method to create appropriate layer type."""
        factory = self._layer_factories.get(instruction.type)
        if factory is None:
            print(f"Warning: Unknown instruction type '{instruction.type}'")
            return None
        return factory(instruction)
    
    def _create_video_layer(self, instruction: EditInstruction):
        """Create video layer from instruction."""
        asset_path = self.asset_registry.get_asset_path(instruction.asset_id)
        if asset_path is None:
            raise ValueError(f"Asset not found: {instruction.asset_id}")
        
        duration = instruction.duration or instruction.end_time - instruction.start_time
        return mv.layer.Video(str(asset_path), duration=duration)
    
    def _create_image_layer(self, instruction: EditInstruction):
        """Create image layer from instruction.""" 
        asset_path = self.asset_registry.get_asset_path(instruction.asset_id)
        if asset_path is None:
            raise ValueError(f"Asset not found: {instruction.asset_id}")
        
        duration = instruction.duration or instruction.end_time - instruction.start_time
        return mv.layer.Image(str(asset_path), duration=duration)
    
    def _create_text_layer(self, instruction: EditInstruction):
        """Create text layer from instruction."""
        props = instruction.properties
        duration = instruction.duration or instruction.end_time - instruction.start_time
        
        return mv.layer.Text(
            text=props.get('text', ''),
            font_family=props.get('font_family', 'Arial'),
            font_size=props.get('font_size', 48),
            color=props.get('color', '#ffffff'),
            duration=duration,
            font_style=props.get('font_style', 'Regular'),
            text_align=props.get('text_align', 'center')
        )
    
    def _create_shape_layer(self, instruction: EditInstruction):
        """Create shape layer from instruction."""
        props = instruction.properties
        duration = instruction.duration or instruction.end_time - instruction.start_time
        shape_type = props.get('shape_type', 'rectangle')
        
        if shape_type == 'rectangle':
            return mv.layer.Rectangle(
                size=props.get('size', (100, 100)),
                color=props.get('color', '#ffffff'),
                duration=duration
            )
        elif shape_type == 'ellipse':
            return mv.layer.Ellipse(
                size=props.get('size', (100, 100)),
                color=props.get('color', '#ffffff'),
                duration=duration
            )
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")
    
    def _create_audio_layer(self, instruction: EditInstruction):
        """Create audio layer from instruction."""
        asset_path = self.asset_registry.get_asset_path(instruction.asset_id)
        if asset_path is None:
            raise ValueError(f"Asset not found: {instruction.asset_id}")
        
        duration = instruction.duration or instruction.end_time - instruction.start_time
        return mv.layer.Audio(str(asset_path), duration=duration)
    
    def _apply_animations(self, layer_item, animations: List[Dict[str, Any]]):
        """Apply animation keyframes to layer attributes."""
        for anim in animations:
            attribute_name = anim['attribute']
            keyframes = anim['keyframes']
            values = anim['values']
            easings = [self._easing_map.get(e, Easing.LINEAR) for e in anim.get('easings', [])]
            
            # Get the attribute object
            if hasattr(layer_item, attribute_name):
                attr = getattr(layer_item, attribute_name)
            elif hasattr(layer_item.layer, attribute_name):
                attr = getattr(layer_item.layer, attribute_name)
            else:
                print(f"Warning: Attribute '{attribute_name}' not found")
                continue
            
            # Enable motion and add keyframes
            attr.enable_motion().extend(
                keyframes=keyframes,
                values=values,
                easings=easings if easings else None
            )


class VinVideoComposition(Composition):
    """Extended Composition with VinVideo-specific features."""
    
    def __init__(self, size: tuple[int, int], duration: float, 
                 scene_id: str, target_format: str):
        super().__init__(size=size, duration=duration)
        self.scene_id = scene_id
        self.target_format = target_format
        self._qc_results = []
    
    def add_qc_result(self, result):
        """Add quality control result for tracking."""
        self._qc_results.append(result)
    
    def get_qc_summary(self) -> Dict[str, Any]:
        """Get summary of all QC results."""
        if not self._qc_results:
            return {"status": "no_qc_run"}
        
        passed = sum(1 for r in self._qc_results if r.passed)
        total = len(self._qc_results)
        
        return {
            "total_checks": total,
            "passed": passed,
            "failed": total - passed,
            "overall_quality_score": sum(r.quality_score for r in self._qc_results) / total,
            "issues": [r.issues for r in self._qc_results if r.issues]
        }
    
    def export_for_platform(self, output_path: str, **kwargs):
        """Export video optimized for the target social media platform."""
        from .social_formats import format_for_platform
        
        platform_settings = format_for_platform(self.target_format)
        
        # Merge platform settings with any user overrides
        export_params = {**platform_settings, **kwargs}
        
        self.write_video(output_path, **export_params)
        
        return {
            "output_path": output_path,
            "format": self.target_format,
            "settings_used": export_params,
            "qc_summary": self.get_qc_summary()
        }
