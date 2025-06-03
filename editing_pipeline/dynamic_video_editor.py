#!/usr/bin/env python3
"""
VinVideo Dynamic Video Editor
Comprehensive video editing script with Final Cut Pro-like timeline capabilities
Integrates with the existing subtitle system and provides professional multi-layer composition
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import numpy as np
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import movis as mv
from movis import BlendingMode
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer


def get_resolution_from_format(video_format: str) -> Tuple[int, int]:
    """
    Convert video format ratio to resolution.
    
    Args:
        video_format: String format like "9:16" or "16:9"
    
    Returns:
        Tuple of (width, height) for the resolution
    
    Supported formats:
        - "9:16" → 1080x1920 (vertical/portrait - Instagram, TikTok, YouTube Shorts)
        - "16:9" → 1920x1080 (horizontal/landscape - YouTube, standard video)
        - "4:5" → 1080x1350 (Instagram feed posts)
        - "1:1" → 1080x1080 (Instagram square posts)
    """
    format_map = {
        "9:16": (1080, 1920),    # Vertical - Stories, Reels, Shorts
        "16:9": (1920, 1080),    # Horizontal - YouTube, TV
        "4:5": (1080, 1350),     # Instagram portrait feed
        "1:1": (1080, 1080),     # Square - Instagram/Facebook
        "21:9": (2560, 1080),    # Ultrawide cinematic
        "4:3": (1440, 1080),     # Classic TV format
    }
    
    # Normalize the format string (remove spaces, make lowercase)
    normalized_format = video_format.strip().lower()
    
    # Check if format exists in our map
    if normalized_format in format_map:
        return format_map[normalized_format]
    
    # If not found, try to parse custom format
    try:
        if ":" in normalized_format:
            width_ratio, height_ratio = normalized_format.split(":")
            width_ratio = float(width_ratio)
            height_ratio = float(height_ratio)
            
            # Calculate resolution maintaining Full HD quality
            if width_ratio > height_ratio:
                # Landscape orientation
                width = 1920
                height = int(1920 * (height_ratio / width_ratio))
            else:
                # Portrait orientation
                height = 1920
                width = int(1920 * (width_ratio / height_ratio))
            
            # Ensure even dimensions for video encoding
            width = width if width % 2 == 0 else width + 1
            height = height if height % 2 == 0 else height + 1
            
            return (width, height)
    except:
        pass
    
    # Default to vertical format if invalid input
    print(f"Warning: Invalid format '{video_format}'. Defaulting to 9:16 (1080x1920)")
    return (1080, 1920)


class LayerManager:
    """Manages multiple video/audio/subtitle layers with precise timing control"""
    
    def __init__(self, composition: mv.layer.Composition):
        self.composition = composition
        self.layers: Dict[str, mv.layer.LayerItem] = {}
        self.layer_counter = 0
    
    def add_video_layer(
        self,
        source: Union[str, Path],
        name: Optional[str] = None,
        position: Optional[Tuple[float, float]] = None,
        scale: Union[float, Tuple[float, float]] = (1.0, 1.0),
        rotation: float = 0.0,
        opacity: float = 1.0,
        blending_mode: Union[BlendingMode, str] = BlendingMode.NORMAL,
        offset: float = 0.0,
        start_time: float = 0.0,
        end_time: Optional[float] = None,
        effects: Optional[List[mv.effect.Effect]] = None,
        auto_scale: bool = True
    ) -> mv.layer.LayerItem:
        """Add a video layer with full control over positioning and timing"""
        
        # Create unique name if not provided
        if name is None:
            name = f"video_{self.layer_counter}"
            self.layer_counter += 1
        
        # Load video layer
        video_layer = mv.layer.Video(str(source))
        
        # Auto-scale video if requested
        if auto_scale:
            try:
                video_size = video_layer.size  # Get video dimensions
                # Calculate cover scale inline to avoid import issues
                image_width, image_height = video_size
                target_width, target_height = self.composition.size
                
                # Calculate aspect ratios
                image_aspect = image_width / image_height
                target_aspect = target_width / target_height
                
                # If aspect ratios are very close (within 1% tolerance), just fit
                aspect_tolerance = 0.01
                if abs(image_aspect - target_aspect) < aspect_tolerance:
                    cover_scale = min(target_width / image_width, target_height / image_height)
                else:
                    # Different aspect ratios - scale to cover
                    scale_x = target_width / image_width
                    scale_y = target_height / image_height
                    cover_scale = max(scale_x, scale_y)
                
                # Apply the cover scale to the user-provided scale
                if isinstance(scale, tuple):
                    final_scale = (scale[0] * cover_scale, scale[1] * cover_scale)
                else:
                    final_scale = (scale * cover_scale, scale * cover_scale)
            except Exception as e:
                print(f"Warning: Could not auto-scale video {source}: {e}")
                final_scale = scale if isinstance(scale, tuple) else (scale, scale)
        else:
            final_scale = scale if isinstance(scale, tuple) else (scale, scale)
        
        # Add to composition with all parameters
        layer_item = self.composition.add_layer(
            video_layer,
            name=name,
            position=position,
            scale=final_scale,
            rotation=rotation,
            opacity=opacity,
            blending_mode=blending_mode,
            offset=offset,
            start_time=start_time,
            end_time=end_time
        )
        
        # Apply effects if provided
        if effects:
            for effect in effects:
                layer_item.add_effect(effect)
        
        self.layers[name] = layer_item
        return layer_item
    
    def add_image_layer(
        self,
        source: Union[str, Path],
        duration: float,
        name: Optional[str] = None,
        position: Optional[Tuple[float, float]] = None,
        scale: Union[float, Tuple[float, float]] = (1.0, 1.0),
        rotation: float = 0.0,
        opacity: float = 1.0,
        blending_mode: Union[BlendingMode, str] = BlendingMode.NORMAL,
        offset: float = 0.0,
        effects: Optional[List[mv.effect.Effect]] = None,
        **kwargs
    ) -> mv.layer.LayerItem:
        """Add an image layer with specified duration and full control"""
        if name is None:
            name = f"image_{self.layer_counter}"
            self.layer_counter += 1
        
        image_layer = mv.layer.Image(str(source), duration=duration)
        
        layer_item = self.composition.add_layer(
            image_layer,
            name=name,
            position=position,
            scale=scale if isinstance(scale, tuple) else (scale, scale),
            rotation=rotation,
            opacity=opacity,
            blending_mode=blending_mode,
            offset=offset,
            **kwargs
        )
        
        # Apply effects if provided
        if effects:
            for effect in effects:
                layer_item.add_effect(effect)
        
        self.layers[name] = layer_item
        return layer_item
    
    def add_audio_layer(
        self,
        source: Union[str, Path],
        name: Optional[str] = None,
        audio_level: float = 0.0,
        offset: float = 0.0,
        start_time: float = 0.0,
        end_time: Optional[float] = None
    ) -> mv.layer.LayerItem:
        """Add an audio track with level control"""
        if name is None:
            name = f"audio_{self.layer_counter}"
            self.layer_counter += 1
        
        audio_layer = mv.layer.Audio(str(source))
        
        layer_item = self.composition.add_layer(
            audio_layer,
            name=name,
            audio_level=audio_level,
            offset=offset,
            start_time=start_time,
            end_time=end_time
        )
        
        self.layers[name] = layer_item
        return layer_item
    
    def get_layer(self, name: str) -> Optional[mv.layer.LayerItem]:
        """Get a layer by name"""
        return self.layers.get(name)


class AnimationController:
    """Keyframe-based animation system using Movis motion capabilities"""
    
    @staticmethod
    def animate_opacity(
        layer_item: mv.layer.LayerItem,
        keyframes: List[float],
        values: List[float],
        easings: Optional[List[str]] = None
    ):
        """Animate layer opacity over time"""
        if easings is None:
            easings = ['linear'] * (len(keyframes) - 1)
        
        layer_item.opacity.enable_motion().extend(
            keyframes=keyframes,
            values=values,
            easings=easings
        )
    
    @staticmethod
    def animate_position(
        layer_item: mv.layer.LayerItem,
        keyframes: List[float],
        positions: List[Tuple[float, float]],
        easings: Optional[List[str]] = None
    ):
        """Animate layer position over time"""
        if easings is None:
            easings = ['ease_in_out'] * (len(keyframes) - 1)
        
        layer_item.position.enable_motion().extend(
            keyframes=keyframes,
            values=positions,
            easings=easings
        )
    
    @staticmethod
    def animate_scale(
        layer_item: mv.layer.LayerItem,
        keyframes: List[float],
        scales: List[Union[float, Tuple[float, float]]],
        easings: Optional[List[str]] = None
    ):
        """Animate layer scale over time"""
        if easings is None:
            easings = ['ease_out'] * (len(keyframes) - 1)
        
        # Convert single values to tuples
        scale_values = []
        for scale in scales:
            if isinstance(scale, (int, float)):
                scale_values.append((scale, scale))
            else:
                scale_values.append(scale)
        
        layer_item.scale.enable_motion().extend(
            keyframes=keyframes,
            values=scale_values,
            easings=easings
        )
    
    @staticmethod
    def animate_rotation(
        layer_item: mv.layer.LayerItem,
        keyframes: List[float],
        rotations: List[float],
        easings: Optional[List[str]] = None
    ):
        """Animate layer rotation over time"""
        if easings is None:
            easings = ['linear'] * (len(keyframes) - 1)
        
        layer_item.rotation.enable_motion().extend(
            keyframes=keyframes,
            values=rotations,
            easings=easings
        )
    
    @staticmethod
    def apply_fade_in_out(
        layer_item: mv.layer.LayerItem,
        fade_in: float = 0.5,
        fade_out: float = 0.5,
        duration: float = None
    ):
        """Apply fade in and fade out to a layer"""
        if duration is None:
            # Try to get duration from the layer if possible
            duration = 5.0  # Default duration
        
        AnimationController.animate_opacity(
            layer_item,
            keyframes=[0.0, fade_in, duration - fade_out, duration],
            values=[0.0, 1.0, 1.0, 0.0],
            easings=['ease_out', 'linear', 'ease_in']
        )


class AudioManager:
    """Professional audio handling with multi-track support and synchronization"""
    
    def __init__(self, composition: mv.layer.Composition):
        self.composition = composition
        self.audio_tracks: Dict[str, mv.layer.LayerItem] = {}
    
    def add_background_music(
        self,
        source: Union[str, Path],
        level: float = -15.0,
        fade_in: float = 2.0,
        fade_out: float = 2.0,
        name: str = "background_music"
    ) -> mv.layer.LayerItem:
        """Add background music with automatic fade in/out"""
        audio_layer = mv.layer.Audio(str(source))
        duration = min(audio_layer.duration, self.composition.duration)
        
        layer_item = self.composition.add_layer(
            audio_layer,
            name=name,
            audio_level=level,
            end_time=duration
        )
        
        # Apply fade in/out
        if fade_in > 0 or fade_out > 0:
            self.apply_audio_fade(layer_item, fade_in, fade_out, duration)
        
        self.audio_tracks[name] = layer_item
        return layer_item
    
    def add_narration(
        self,
        source: Union[str, Path],
        offset: float = 0.0,
        level: float = 0.0,
        name: str = "narration"
    ) -> mv.layer.LayerItem:
        """Add narration track"""
        audio_layer = mv.layer.Audio(str(source))
        
        layer_item = self.composition.add_layer(
            audio_layer,
            name=name,
            audio_level=level,
            offset=offset
        )
        
        self.audio_tracks[name] = layer_item
        return layer_item
    
    def apply_audio_fade(
        self,
        layer_item: mv.layer.LayerItem,
        fade_in: float,
        fade_out: float,
        duration: float
    ):
        """Apply fade in/out to audio track"""
        current_level = layer_item.audio_level.data if hasattr(layer_item.audio_level, 'data') else 0.0
        
        keyframes = []
        values = []
        easings = []
        
        if fade_in > 0:
            keyframes.extend([0.0, fade_in])
            values.extend([current_level - 40.0, current_level])  # Start from -40dB
            easings.append('ease_out')
        
        if fade_out > 0:
            if not keyframes:
                keyframes.append(duration - fade_out)
                values.append(current_level)
            else:
                keyframes.append(duration - fade_out)
                values.append(current_level)
                easings.append('linear')
            
            keyframes.append(duration)
            values.append(current_level - 40.0)  # Fade to -40dB
            easings.append('ease_in')
        
        if keyframes:
            layer_item.audio_level.enable_motion().extend(
                keyframes=keyframes,
                values=values,
                easings=easings
            )
    
    def apply_ducking(
        self,
        background_track: str,
        trigger_track: str,
        reduction: float = -10.0,
        attack: float = 0.5,
        release: float = 0.5
    ):
        """Apply audio ducking when trigger track is active"""
        bg_layer = self.audio_tracks.get(background_track)
        trigger_layer = self.audio_tracks.get(trigger_track)
        
        if not bg_layer or not trigger_layer:
            print(f"Warning: Could not find tracks for ducking: {background_track}, {trigger_track}")
            return
        
        # Get trigger track timing
        trigger_offset = trigger_layer.offset
        trigger_duration = trigger_layer.layer.duration if hasattr(trigger_layer.layer, 'duration') else 5.0
        
        # Get current background level
        current_level = bg_layer.audio_level.data if hasattr(bg_layer.audio_level, 'data') else 0.0
        ducked_level = current_level + reduction
        
        # Create ducking keyframes
        keyframes = [
            trigger_offset - attack,
            trigger_offset,
            trigger_offset + trigger_duration,
            trigger_offset + trigger_duration + release
        ]
        values = [
            current_level,
            ducked_level,
            ducked_level,
            current_level
        ]
        easings = ['ease_out', 'linear', 'ease_in']
        
        bg_layer.audio_level.enable_motion().extend(
            keyframes=keyframes,
            values=values,
            easings=easings
        )


class TimelineEditor:
    """Professional timeline editing operations using Movis advanced features"""
    
    @staticmethod
    def concatenate_clips(
        clips: List[Union[str, Path, mv.layer.Video]],
        transitions: Optional[List[Dict[str, Any]]] = None
    ) -> mv.layer.Composition:
        """Concatenate multiple clips sequentially with optional transitions"""
        
        # Convert paths to Video layers
        video_layers = []
        for clip in clips:
            if isinstance(clip, (str, Path)):
                video_layers.append(mv.layer.Video(str(clip)))
            else:
                video_layers.append(clip)
        
        # Calculate total duration
        total_duration = sum(layer.duration for layer in video_layers)
        
        # Create composition
        first_video = video_layers[0]
        size = first_video.size if hasattr(first_video, 'size') else (1920, 1080)
        composition = mv.layer.Composition(size=size, duration=total_duration)
        
        # Add clips sequentially
        current_time = 0.0
        for i, video_layer in enumerate(video_layers):
            layer_item = composition.add_layer(
                video_layer,
                name=f"clip_{i}",
                offset=current_time
            )
            
            # Apply transition if specified
            if transitions and i < len(transitions):
                transition = transitions[i]
                TimelineEditor._apply_transition(
                    layer_item,
                    transition,
                    video_layer.duration
                )
            
            current_time += video_layer.duration
        
        return composition
    
    @staticmethod
    def _apply_transition(
        layer_item: mv.layer.LayerItem,
        transition: Dict[str, Any],
        duration: float
    ):
        """Apply a transition effect to a layer"""
        transition_type = transition.get('type', 'fade')
        transition_duration = transition.get('duration', 0.5)
        
        if transition_type == 'fade':
            # Fade in
            layer_item.opacity.enable_motion().extend(
                keyframes=[0.0, transition_duration],
                values=[0.0, 1.0],
                easings=['ease_out']
            )
        elif transition_type == 'slide':
            # Slide from direction
            direction = transition.get('direction', 'left')
            if direction == 'left':
                start_pos = (-layer_item.layer.size[0] // 2, 0)
            elif direction == 'right':
                start_pos = (layer_item.layer.size[0] // 2, 0)
            elif direction == 'top':
                start_pos = (0, -layer_item.layer.size[1] // 2)
            else:  # bottom
                start_pos = (0, layer_item.layer.size[1] // 2)
            
            layer_item.position.enable_motion().extend(
                keyframes=[0.0, transition_duration],
                values=[start_pos, (0, 0)],
                easings=['ease_out3']
            )
    
    @staticmethod
    def create_split_screen(
        videos: List[Union[str, Path]],
        layout: str = "2x2",
        size: Tuple[int, int] = (1920, 1080),
        duration: Optional[float] = None
    ) -> mv.layer.Composition:
        """Create split screen with multiple videos"""
        
        # Parse layout
        if layout == "2x2":
            rows, cols = 2, 2
        elif layout == "1x2":
            rows, cols = 1, 2
        elif layout == "2x1":
            rows, cols = 2, 1
        else:
            raise ValueError(f"Unsupported layout: {layout}")
        
        # Load videos
        video_layers = []
        for video_path in videos[:rows * cols]:
            video_layers.append(mv.layer.Video(str(video_path)))
        
        # Determine duration
        if duration is None:
            duration = min(v.duration for v in video_layers)
        
        # Create composition
        composition = mv.layer.Composition(size=size, duration=duration)
        
        # Calculate cell size
        cell_width = size[0] // cols
        cell_height = size[1] // rows
        
        # Add videos in grid
        for i, video_layer in enumerate(video_layers):
            row = i // cols
            col = i % cols
            
            # Calculate position (center of each cell)
            x = col * cell_width + cell_width // 2
            y = row * cell_height + cell_height // 2
            
            # Calculate scale to fit in cell
            scale_x = cell_width / video_layer.size[0]
            scale_y = cell_height / video_layer.size[1]
            scale = min(scale_x, scale_y) * 0.95  # 95% to add small gap
            
            composition.add_layer(
                video_layer,
                name=f"video_{i}",
                position=(x, y),
                scale=(scale, scale),
                end_time=duration
            )
        
        return composition


class PlatformExporter:
    """Platform-specific optimization and export settings"""
    
    PLATFORM_PRESETS = {
        'instagram': {
            'resolution': (1080, 1920),
            'fps': 30,
            'codec': 'libx264',
            'audio_codec': 'aac',
            'crf': 23,
            'preset': 'medium',
            'pixel_format': 'yuv420p'
        },
        'tiktok': {
            'resolution': (1080, 1920),
            'fps': 30,
            'codec': 'libx264',
            'audio_codec': 'aac',
            'crf': 23,
            'preset': 'medium',
            'pixel_format': 'yuv420p'
        },
        'youtube_shorts': {
            'resolution': (1080, 1920),
            'fps': 30,
            'codec': 'libx264',
            'audio_codec': 'aac',
            'crf': 18,
            'preset': 'slow',
            'pixel_format': 'yuv420p'
        },
        'youtube': {
            'resolution': (1920, 1080),
            'fps': 30,
            'codec': 'libx264',
            'audio_codec': 'aac',
            'crf': 18,
            'preset': 'slow',
            'pixel_format': 'yuv420p'
        }
    }
    
    @classmethod
    def export_for_platform(
        cls,
        composition: mv.layer.Composition,
        output_path: Union[str, Path],
        platform: str = 'instagram',
        quality: str = 'high'
    ):
        """Export video optimized for specific platform"""
        if platform not in cls.PLATFORM_PRESETS:
            print(f"Warning: Unknown platform '{platform}', using Instagram settings")
            platform = 'instagram'
        
        preset = cls.PLATFORM_PRESETS[platform]
        
        # Adjust quality
        if quality == 'low':
            preset['crf'] = min(51, preset['crf'] + 5)
            preset['preset'] = 'faster'
        elif quality == 'high':
            preset['crf'] = max(0, preset['crf'] - 5)
            preset['preset'] = 'slow'
        
        # Export with platform settings
        output_params = [
            '-crf', str(preset['crf']),
            '-preset', preset['preset']
        ]
        
        composition.write_video(
            str(output_path),
            codec=preset['codec'],
            audio_codec=preset['audio_codec'],
            fps=preset['fps'],
            pixelformat=preset['pixel_format'],
            output_params=output_params
        )
        
        print(f"✅ Exported video for {platform} to: {output_path}")
        print(f"   Resolution: {preset['resolution']}")
        print(f"   Quality: {quality} (CRF: {preset['crf']})")


class DynamicVideoEditor:
    """Main class handling all video editing operations with Movis integration"""
    
    def __init__(self):
        self.composition: Optional[mv.layer.Composition] = None
        self.layer_manager: Optional[LayerManager] = None
        self.audio_manager: Optional[AudioManager] = None
        self.subtitle_style: Optional[Any] = None
        self.platform_exporter = PlatformExporter()
        
        # Load subtitle style configuration
        self.subtitle_styles_path = Path(__file__).parent / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
    
    @staticmethod
    def calculate_cover_scale(image_size: Tuple[int, int], target_size: Tuple[int, int]) -> float:
        """Calculate scale factor to cover entire target area (no black borders)"""
        image_width, image_height = image_size
        target_width, target_height = target_size
        
        # Calculate aspect ratios
        image_aspect = image_width / image_height
        target_aspect = target_width / target_height
        
        # If aspect ratios are very close (within 1% tolerance), just fit the image
        aspect_tolerance = 0.01
        if abs(image_aspect - target_aspect) < aspect_tolerance:
            # Same aspect ratio - scale to fit exactly
            return min(target_width / image_width, target_height / image_height)
        
        # Different aspect ratios - scale to cover (no black borders)
        scale_x = target_width / image_width
        scale_y = target_height / image_height
        
        # Use the larger scale to ensure full coverage
        return max(scale_x, scale_y)
        
    def create_composition(
        self,
        resolution: Tuple[int, int] = (1080, 1920),
        duration: float = 10.0,
        fps: int = 30,
        background_color: Optional[Tuple[int, int, int]] = None
    ):
        """Create main Movis composition with specified resolution/fps"""
        self.composition = mv.layer.Composition(size=resolution, duration=duration)
        self.layer_manager = LayerManager(self.composition)
        self.audio_manager = AudioManager(self.composition)
        
        # Add background if specified
        if background_color:
            bg_layer = mv.layer.Rectangle(
                size=resolution,
                color=background_color,
                duration=duration
            )
            self.composition.add_layer(bg_layer, name="background")
    
    def add_subtitle_layer(
        self,
        parakeet_data: Union[str, Path, Dict],
        style_name: str,
        position: str = "bottom",
        safe_zones: bool = True
    ) -> Optional[mv.layer.LayerItem]:
        """Add our professional subtitle layer"""
        
        # Load parakeet data
        if isinstance(parakeet_data, (str, Path)):
            with open(parakeet_data, 'r') as f:
                parakeet_json = json.load(f)
        else:
            parakeet_json = parakeet_data
        
        # Extract word timestamps
        words = []
        for item in parakeet_json.get("word_timestamps", []):
            words.append({
                "word": item["word"],
                "start": item["start"],
                "end": item["end"]
            })
        
        if not words:
            print("Warning: No word timestamps found in parakeet data")
            return None
        
        # Load subtitle style
        style = StyleLoader.load_style_from_json(self.subtitle_styles_path, style_name)
        if not style:
            print(f"Error: Could not load subtitle style '{style_name}'")
            return None
        
        # Create styled subtitle layer
        subtitle_layer = StyledSubtitleLayer(
            words=words,
            style=style,
            resolution=self.composition.size,
            position=position,
            safe_zones=safe_zones
        )
        
        # Add to composition
        layer_item = self.composition.add_layer(subtitle_layer, name="subtitles")
        
        print(f"✅ Added subtitle layer with style: {style_name}")
        return layer_item
    
    def add_video_with_subtitles(
        self,
        video_source: Optional[Union[str, Path]] = None,
        audio_source: Union[str, Path] = None,
        parakeet_data: Union[str, Path, Dict] = None,
        subtitle_style: str = "simple_caption",
        background_color: Tuple[int, int, int] = (0, 0, 0)
    ):
        """Convenience method to add video/audio with subtitles"""
        
        # If no composition exists, create one based on video/audio duration
        if self.composition is None:
            # Determine duration from video or audio
            duration = 10.0  # Default
            if video_source:
                video = mv.layer.Video(str(video_source))
                duration = video.duration
                resolution = video.size
            elif audio_source:
                audio = mv.layer.Audio(str(audio_source))
                duration = audio.duration
                resolution = (1080, 1920)  # Default Instagram size
            else:
                resolution = (1080, 1920)
            
            self.create_composition(resolution=resolution, duration=duration, background_color=background_color)
        
        # Add video if provided
        if video_source:
            self.layer_manager.add_video_layer(video_source, name="main_video")
        
        # Add audio if provided
        if audio_source:
            self.audio_manager.add_narration(audio_source, name="main_audio")
        
        # Add subtitles if parakeet data provided
        if parakeet_data:
            self.add_subtitle_layer(parakeet_data, subtitle_style)
    
    def process_timeline_config(self, config: Dict[str, Any]):
        """Process a timeline configuration dictionary"""
        
        # Create composition
        comp_config = config.get('composition', {})
        
        # Determine resolution from format or explicit resolution
        if 'resolution' in comp_config:
            resolution = tuple(comp_config['resolution'])
        elif 'format' in comp_config:
            resolution = get_resolution_from_format(comp_config['format'])
        else:
            resolution = (1080, 1920)  # Default to 9:16
        
        self.create_composition(
            resolution=resolution,
            duration=comp_config.get('duration', 10.0),
            fps=comp_config.get('fps', 30),
            background_color=comp_config.get('background_color')
        )
        
        # Process layers
        for layer_config in config.get('layers', []):
            self._process_layer_config(layer_config)
        
        # Process image sequence if provided
        if 'image_sequence' in config:
            self.process_image_sequence(config['image_sequence'])
        
        # Process audio
        audio_config = config.get('audio', {})
        if 'background_music' in audio_config:
            music = audio_config['background_music']
            self.audio_manager.add_background_music(
                music['source'],
                level=music.get('level', -15.0),
                fade_in=music.get('fade_in', 2.0),
                fade_out=music.get('fade_out', 2.0)
            )
            
            # Apply ducking if specified
            if 'ducking' in music and 'narration' in audio_config:
                self.audio_manager.apply_ducking(
                    'background_music',
                    'narration',
                    reduction=music['ducking'].get('reduction', -10.0)
                )
        
        if 'narration' in audio_config:
            narration = audio_config['narration']
            self.audio_manager.add_narration(
                narration['source'],
                offset=narration.get('offset', 0.0),
                level=narration.get('level', 0.0)
            )
        
        # Process subtitles
        subtitle_config = config.get('subtitles', {})
        if subtitle_config:
            self.add_subtitle_layer(
                subtitle_config['parakeet_data'],
                subtitle_config.get('style', 'simple_caption'),
                position=subtitle_config.get('position', 'bottom')
            )
    
    def process_image_sequence(self, sequence_config: List[Dict[str, Any]]):
        """Process a sequence of images with precise timing"""
        for i, image_config in enumerate(sequence_config):
            # Each image in the sequence should have:
            # - source: path to image file
            # - start_time: when to show the image
            # - end_time: when to stop showing the image
            # - (optional) transition: type of transition to next image
            # - (optional) animation: ken burns, zoom, pan effects
            
            source = image_config['source']
            start_time = image_config['start_time']
            end_time = image_config['end_time']
            duration = end_time - start_time
            
            # Calculate proper scale to cover entire screen
            # First, we need to get the image dimensions
            from PIL import Image
            try:
                with Image.open(source) as img:
                    image_size = img.size  # (width, height)
                cover_scale = self.calculate_cover_scale(image_size, self.composition.size)
                
                
                # Apply any additional scaling from config
                final_scale = cover_scale * image_config.get('scale', 1.0)
            except Exception as e:
                print(f"Warning: Could not determine image size for {source}, using default scale. Error: {e}")
                cover_scale = 1.2  # Default cover scale
                final_scale = cover_scale * image_config.get('scale', 1.0)
            
            # Add the image layer
            layer_item = self.layer_manager.add_image_layer(
                source=source,
                duration=duration,
                name=image_config.get('name', f'image_seq_{i}'),
                position=tuple(image_config.get('position', [540, 960])),
                scale=final_scale,
                opacity=image_config.get('opacity', 1.0),
                offset=start_time
            )
            
            # Apply zoom transition automatically from second image onwards
            # Note: Don't apply zoom transition if ken_burns is specified (to avoid conflicts)
            if i > 0 and 'ken_burns' not in image_config:
                # Apply zoom in transition by default if no transition specified
                if 'transition' not in image_config:
                    zoom_transition = {
                        'type': 'zoom_fade',
                        'duration': 0.5,
                        'zoom_start': 1.2 * cover_scale,
                        'zoom_end': 1.0 * cover_scale
                    }
                    self._apply_image_transition(layer_item, zoom_transition, duration)
                else:
                    # Apply specified transition
                    self._apply_image_transition(layer_item, image_config['transition'], duration)
            elif i == 0 or 'ken_burns' in image_config:
                # For first image or if ken burns is specified, only apply non-zoom transitions
                transition = image_config.get('transition')
                if transition and transition.get('type') != 'zoom_fade':
                    self._apply_image_transition(layer_item, transition, duration)
                elif i > 0 and not transition:
                    # Apply simple fade for images with ken burns
                    fade_transition = {
                        'type': 'fade',
                        'duration': 0.5
                    }
                    self._apply_image_transition(layer_item, fade_transition, duration)
            
            # Apply Ken Burns effect if specified
            if 'ken_burns' in image_config:
                self._apply_ken_burns(layer_item, image_config['ken_burns'], duration, base_scale=cover_scale)
            
            # Apply other animations
            if 'animations' in image_config:
                self._process_animations(layer_item, image_config['animations'])
    
    def _apply_image_transition(self, layer_item: mv.layer.LayerItem, transition: Dict[str, Any], duration: float):
        """Apply transition effects to image"""
        transition_type = transition.get('type', 'fade')
        transition_duration = transition.get('duration', 0.5)
        
        if transition_type == 'fade':
            # Fade in at start, fade out at end
            AnimationController.animate_opacity(
                layer_item,
                keyframes=[0.0, transition_duration, duration - transition_duration, duration],
                values=[0.0, 1.0, 1.0, 0.0],
                easings=['ease_out', 'linear', 'ease_in']
            )
        elif transition_type == 'crossfade':
            # Just fade in (next image will fade in on top)
            AnimationController.animate_opacity(
                layer_item,
                keyframes=[0.0, transition_duration],
                values=[0.0, 1.0],
                easings=['ease_out']
            )
        elif transition_type == 'zoom_fade':
            # Zoom in while fading in
            zoom_start = transition.get('zoom_start', 1.2)
            zoom_end = transition.get('zoom_end', 1.0)
            
            # Animate scale from zoomed in to normal
            AnimationController.animate_scale(
                layer_item,
                keyframes=[0.0, transition_duration],
                scales=[zoom_start, zoom_end],
                easings=['ease_out3']
            )
            
            # Animate opacity fade in
            AnimationController.animate_opacity(
                layer_item,
                keyframes=[0.0, transition_duration],
                values=[0.0, 1.0],
                easings=['ease_out']
            )
    
    def _apply_ken_burns(self, layer_item: mv.layer.LayerItem, ken_burns: Dict[str, Any], duration: float, base_scale: float = 1.0):
        """Apply Ken Burns effect (zoom and pan)"""
        effect_type = ken_burns.get('type', 'zoom_in')
        
        if effect_type == 'zoom_in':
            # Start wide, zoom in - scale relative to base scale
            start_scale_factor = ken_burns.get('start_scale', 1.0)
            end_scale_factor = ken_burns.get('end_scale', 1.2)
            start_scale = base_scale * start_scale_factor
            end_scale = base_scale * end_scale_factor
            AnimationController.animate_scale(
                layer_item,
                keyframes=[0.0, duration],
                scales=[start_scale, end_scale],
                easings=['ease_in_out']
            )
        elif effect_type == 'zoom_out':
            # Start close, zoom out - scale relative to base scale
            start_scale_factor = ken_burns.get('start_scale', 1.2)
            end_scale_factor = ken_burns.get('end_scale', 1.0)
            start_scale = base_scale * start_scale_factor
            end_scale = base_scale * end_scale_factor
            AnimationController.animate_scale(
                layer_item,
                keyframes=[0.0, duration],
                scales=[start_scale, end_scale],
                easings=['ease_in_out']
            )
        elif effect_type == 'pan':
            # Pan across image
            start_pos = tuple(ken_burns.get('start_position', [540, 960]))
            end_pos = tuple(ken_burns.get('end_position', [540, 960]))
            AnimationController.animate_position(
                layer_item,
                keyframes=[0.0, duration],
                positions=[start_pos, end_pos],
                easings=['ease_in_out']
            )
    
    def _process_layer_config(self, layer_config: Dict[str, Any]):
        """Process individual layer configuration"""
        layer_type = layer_config.get('type', 'video')
        
        if layer_type == 'video':
            layer_item = self.layer_manager.add_video_layer(
                source=layer_config['source'],
                name=layer_config.get('name'),
                position=tuple(layer_config.get('position', [540, 960])),
                scale=layer_config.get('scale', 1.0),
                rotation=layer_config.get('rotation', 0.0),
                opacity=layer_config.get('opacity', 1.0),
                blending_mode=layer_config.get('blending_mode', 'normal'),
                offset=layer_config.get('start_time', 0.0),
                start_time=layer_config.get('trim_start', 0.0),
                end_time=layer_config.get('duration')
            )
            
            # Process animations
            if 'animations' in layer_config:
                self._process_animations(layer_item, layer_config['animations'])
            
            # Process effects
            if 'effects' in layer_config:
                self._process_effects(layer_item, layer_config['effects'])
        
        elif layer_type == 'image':
            # Calculate duration from start_time and end_time if provided
            if 'start_time' in layer_config and 'end_time' in layer_config:
                duration = layer_config['end_time'] - layer_config['start_time']
                offset = layer_config['start_time']
            else:
                duration = layer_config.get('duration', 5.0)
                offset = layer_config.get('start_time', 0.0)
            
            layer_item = self.layer_manager.add_image_layer(
                source=layer_config['source'],
                duration=duration,
                name=layer_config.get('name'),
                position=tuple(layer_config.get('position', [540, 960])),
                scale=layer_config.get('scale', 1.0),
                opacity=layer_config.get('opacity', 1.0),
                rotation=layer_config.get('rotation', 0.0),
                blending_mode=layer_config.get('blending_mode', 'normal'),
                offset=offset
            )
            
            # Process animations
            if 'animations' in layer_config:
                self._process_animations(layer_item, layer_config['animations'])
            
            # Process effects
            if 'effects' in layer_config:
                self._process_effects(layer_item, layer_config['effects'])
    
    def _process_animations(self, layer_item: mv.layer.LayerItem, animations: Dict[str, Any]):
        """Process animation configurations for a layer"""
        animation_controller = AnimationController()
        
        for prop, anim_config in animations.items():
            keyframes = anim_config.get('keyframes', [])
            values = anim_config.get('values', [])
            easings = anim_config.get('easings')
            
            if prop == 'opacity':
                animation_controller.animate_opacity(layer_item, keyframes, values, easings)
            elif prop == 'position':
                animation_controller.animate_position(layer_item, keyframes, values, easings)
            elif prop == 'scale':
                animation_controller.animate_scale(layer_item, keyframes, values, easings)
            elif prop == 'rotation':
                animation_controller.animate_rotation(layer_item, keyframes, values, easings)
    
    def _process_effects(self, layer_item: mv.layer.LayerItem, effects: List[str]):
        """Process effect configurations for a layer"""
        for effect_name in effects:
            if effect_name == 'glow':
                layer_item.add_effect(mv.effect.Glow(radius=20.0, strength=1.5))
            elif effect_name == 'blur':
                layer_item.add_effect(mv.effect.GaussianBlur(radius=10.0))
            elif effect_name == 'shadow':
                layer_item.add_effect(mv.effect.DropShadow(
                    radius=5.0,
                    offset=10.0,
                    angle=45.0,
                    opacity=0.5
                ))
    
    def export_video(
        self,
        output_path: Union[str, Path],
        platform: Optional[str] = None,
        quality: str = 'medium'
    ):
        """Export video with platform-specific optimization"""
        if not self.composition:
            print("Error: No composition to export")
            return
        
        output_path = Path(output_path)
        
        if platform:
            self.platform_exporter.export_for_platform(
                self.composition,
                output_path,
                platform,
                quality
            )
        else:
            # Standard export
            self.composition.write_video(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                fps=30,
                pixelformat='yuv420p'
            )
            print(f"✅ Exported video to: {output_path}")


def parse_overlay_args(args) -> Dict[str, Any]:
    """Parse overlay video arguments into configuration"""
    config = {
        'layers': []
    }
    
    if args.overlay_videos:
        videos = args.overlay_videos.split(',')
        positions = args.overlay_positions.split(',') if args.overlay_positions else []
        opacities = [float(x) for x in args.overlay_opacities.split(',')] if args.overlay_opacities else []
        times = args.overlay_times.split(',') if args.overlay_times else []
        
        for i, video in enumerate(videos):
            layer_config = {
                'type': 'video',
                'source': video.strip(),
                'name': f'overlay_{i}'
            }
            
            # Parse position
            if i < len(positions):
                pos = positions[i].strip().lower()
                if pos == 'top-right':
                    layer_config['position'] = [900, 200]
                    layer_config['scale'] = 0.3
                elif pos == 'top-left':
                    layer_config['position'] = [180, 200]
                    layer_config['scale'] = 0.3
                elif pos == 'bottom-right':
                    layer_config['position'] = [900, 1720]
                    layer_config['scale'] = 0.3
                elif pos == 'bottom-left':
                    layer_config['position'] = [180, 1720]
                    layer_config['scale'] = 0.3
                else:
                    # Try to parse as x,y coordinates
                    try:
                        x, y = pos.split(':')
                        layer_config['position'] = [float(x), float(y)]
                    except:
                        layer_config['scale'] = 0.3
            
            # Parse opacity
            if i < len(opacities):
                layer_config['opacity'] = opacities[i]
            
            # Parse timing
            if i < len(times):
                try:
                    start, end = times[i].split('-')
                    layer_config['start_time'] = float(start)
                    layer_config['duration'] = float(end) - float(start)
                except:
                    pass
            
            config['layers'].append(layer_config)
    
    return config


def main():
    parser = argparse.ArgumentParser(
        description='VinVideo Dynamic Video Editor - Professional video editing with subtitle integration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic subtitle generation
  python3 dynamic_video_editor.py --audio audio.mp3 --parakeet parakeet.json --style simple_caption

  # Add video background
  python3 dynamic_video_editor.py --main-video video.mp4 --audio narration.mp3 --parakeet parakeet.json --style highlight_caption

  # Multi-layer composition
  python3 dynamic_video_editor.py --main-video main.mp4 --overlay-videos "broll1.mp4,broll2.mp4" --overlay-positions "top-right,bottom-left" --overlay-opacities "0.8,0.6" --overlay-times "10-15,20-25" --audio narration.mp3 --parakeet parakeet.json --style karaoke_style

  # Use JSON configuration
  python3 dynamic_video_editor.py --config editing_plan.json

  # Export for specific platform
  python3 dynamic_video_editor.py --audio audio.mp3 --parakeet parakeet.json --style glow_caption --platform instagram --quality high
        """
    )
    
    # Input options
    parser.add_argument('--audio', type=str, help='Path to audio file (narration or main audio)')
    parser.add_argument('--parakeet', type=str, help='Path to NVIDIA Parakeet JSON transcription')
    parser.add_argument('--style', type=str, default='simple_caption', 
                        choices=['simple_caption', 'background_caption', 'glow_caption', 'karaoke_style',
                                'highlight_caption', 'deep_diver', 'popling_caption', 'greengoblin', 'sgone_caption'],
                        help='Subtitle style to use')
    
    # Video options
    parser.add_argument('--main-video', type=str, help='Path to main video file')
    parser.add_argument('--overlay-videos', type=str, help='Comma-separated paths to overlay videos')
    parser.add_argument('--overlay-positions', type=str, help='Comma-separated positions (top-right, bottom-left, or x:y)')
    parser.add_argument('--overlay-opacities', type=str, help='Comma-separated opacity values (0.0-1.0)')
    parser.add_argument('--overlay-times', type=str, help='Comma-separated time ranges (start-end)')
    
    # Audio options
    parser.add_argument('--background-music', type=str, help='Path to background music file')
    parser.add_argument('--music-volume', type=float, default=-15.0, help='Background music volume in dB')
    parser.add_argument('--music-ducking', type=float, help='Ducking reduction in dB when voice is active')
    
    # Configuration
    parser.add_argument('--config', type=str, help='Path to JSON configuration file')
    parser.add_argument('--format', type=str, default='9:16', 
                        help='Video format ratio (9:16, 16:9, 4:5, 1:1, etc.)')
    parser.add_argument('--resolution', type=str, help='Output resolution (WIDTHxHEIGHT) - overrides format')
    parser.add_argument('--fps', type=int, default=30, help='Output frame rate')
    parser.add_argument('--background-color', type=str, help='Background color as R,G,B (e.g., "0,0,0" for black)')
    
    # Export options
    parser.add_argument('--platform', type=str, choices=['instagram', 'tiktok', 'youtube_shorts', 'youtube'],
                        help='Export optimized for specific platform')
    parser.add_argument('--quality', type=str, choices=['low', 'medium', 'high'], default='medium',
                        help='Export quality level')
    parser.add_argument('--output', '-o', type=str, default='output.mp4', help='Output video file path')
    
    args = parser.parse_args()
    
    # Create editor instance
    editor = DynamicVideoEditor()
    
    # Process based on input method
    if args.config:
        # Load from JSON configuration
        with open(args.config, 'r') as f:
            config = json.load(f)
        editor.process_timeline_config(config)
    else:
        # Build configuration from command line arguments
        
        # Parse resolution - use format parameter or explicit resolution
        if args.resolution:
            # User provided explicit resolution
            width, height = map(int, args.resolution.split('x'))
            resolution = (width, height)
        else:
            # Use format parameter to determine resolution
            resolution = get_resolution_from_format(args.format)
        
        # Parse background color
        bg_color = None
        if args.background_color:
            bg_color = tuple(map(int, args.background_color.split(',')))
        
        # Create composition
        if args.main_video:
            video = mv.layer.Video(args.main_video)
            duration = video.duration
        elif args.audio:
            audio = mv.layer.Audio(args.audio)
            duration = audio.duration
        else:
            duration = 10.0
        
        editor.create_composition(
            resolution=resolution,
            duration=duration,
            fps=args.fps,
            background_color=bg_color or (0, 0, 0)
        )
        
        # Add main video if provided
        if args.main_video:
            editor.layer_manager.add_video_layer(args.main_video, name='main_video')
        
        # Add overlay videos
        if args.overlay_videos:
            overlay_config = parse_overlay_args(args)
            for layer_config in overlay_config['layers']:
                editor._process_layer_config(layer_config)
        
        # Add audio
        if args.audio:
            editor.audio_manager.add_narration(args.audio, name='narration')
        
        # Add background music
        if args.background_music:
            music_item = editor.audio_manager.add_background_music(
                args.background_music,
                level=args.music_volume
            )
            
            # Apply ducking if specified
            if args.music_ducking and args.audio:
                editor.audio_manager.apply_ducking(
                    'background_music',
                    'narration',
                    reduction=args.music_ducking
                )
        
        # Add subtitles
        if args.parakeet:
            editor.add_subtitle_layer(args.parakeet, args.style)
    
    # Export video
    editor.export_video(args.output, platform=args.platform, quality=args.quality)
    
    print(f"\n✨ Video editing complete!")
    print(f"   Output: {args.output}")
    print(f"   Duration: {editor.composition.duration:.1f}s")
    print(f"   Resolution: {editor.composition.size}")
    if args.platform:
        print(f"   Optimized for: {args.platform}")


if __name__ == "__main__":
    main()