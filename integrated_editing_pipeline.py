#!/usr/bin/env python3
"""
VinVideo Integrated Editing Pipeline
Combines producer cut plan with image assets and advanced subtitle styles
Supports 3:2 aspect ratio and all 9 finalized subtitle styles
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
import numpy as np
from datetime import datetime

# Add current directory and parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

import movis as mv
from movis import BlendingMode
from subtitle_styles.core.json_style_loader import StyleLoader
from subtitle_styles.core.movis_layer import StyledSubtitleLayer


def get_resolution_from_format(video_format: str) -> Tuple[int, int]:
    """
    Convert video format ratio to resolution with 3:2 support.
    
    Args:
        video_format: String format like "3:2", "9:16", or "16:9"
    
    Returns:
        Tuple of (width, height) for the resolution
    """
    format_map = {
        "3:2": (1620, 1080),     # 3:2 aspect ratio - classic photo format
        "9:16": (1080, 1920),    # Vertical - Stories, Reels, Shorts
        "16:9": (1920, 1080),    # Horizontal - YouTube, TV
        "4:5": (1080, 1350),     # Instagram portrait feed
        "1:1": (1080, 1080),     # Square - Instagram/Facebook
        "21:9": (2560, 1080),    # Ultrawide cinematic
        "4:3": (1440, 1080),     # Classic TV format
    }
    
    # Normalize the format string
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
            
            # Calculate resolution maintaining quality
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
    
    # Default to 3:2 format if invalid input
    print(f"Warning: Invalid format '{video_format}'. Defaulting to 3:2 (1620x1080)")
    return (1620, 1080)


class IntegratedVideoEditor:
    """Main editor class that integrates producer cuts, images, and subtitle styles"""
    
    def __init__(self):
        self.composition: Optional[mv.layer.Composition] = None
        self.subtitle_styles_path = Path(__file__).parent / "subtitle_styles" / "config" / "subtitle_styles_v3.json"
        
        # Available subtitle styles
        self.available_styles = [
            'simple_caption', 'background_caption', 'glow_caption', 'karaoke_style',
            'highlight_caption', 'deep_diver', 'popling_caption', 'greengoblin', 'sgone_caption'
        ]
    
    def load_producer_cuts(self, cuts_file: Union[str, Path]) -> List[Dict[str, Any]]:
        """Load producer cut plan from JSON file"""
        with open(cuts_file, 'r') as f:
            data = json.load(f)
        
        # Extract cut points from the structure
        if 'cut_points' in data:
            return data['cut_points']
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Invalid cut plan format - expected 'cut_points' array or direct array")
    
    def discover_image_assets(self, assets_dir: Path) -> List[Dict[str, Any]]:
        """Discover and organize image assets from directory"""
        images = []
        
        # Look for numbered images (multiple patterns supported)
        for i in range(1, 33):  # Looking for 1-32
            image_path = None
            
            # Try different naming patterns
            patterns = [
                f"prompt_engineer_image_{i}.png",  # prompt_engineer_image_N.png
                f"image_{i}_*.png",               # image_N_timestamp.png
                f"image_{i}.png",                 # image_N.png
                f"beat_{i:02d}.png"               # beat_NN.png
            ]
            
            for pattern in patterns:
                matching_files = list(assets_dir.glob(pattern))
                if matching_files:
                    image_path = matching_files[0]
                    break
            
            if image_path:
                images.append({
                    'number': i,
                    'path': str(image_path),
                    'name': image_path.name
                })
        
        # Sort images by number to ensure correct order
        images.sort(key=lambda x: x['number'])
        
        print(f"📁 Discovered {len(images)} image assets")
        for img in images[:5]:  # Show first 5
            print(f"  - {img['name']}")
        if len(images) > 5:
            print(f"  ... and {len(images) - 5} more")
        
        return images
    
    def calculate_cover_scale(self, image_size: Tuple[int, int], target_size: Tuple[int, int]) -> float:
        """Calculate scale factor to cover entire target area (no black borders)"""
        image_width, image_height = image_size
        target_width, target_height = target_size
        
        # Calculate aspect ratios
        image_aspect = image_width / image_height
        target_aspect = target_width / target_height
        
        # Different aspect ratios - scale to cover (no black borders)
        scale_x = target_width / image_width
        scale_y = target_height / image_height
        
        # Use the larger scale to ensure full coverage
        return max(scale_x, scale_y)
    
    def create_image_sequence_from_cuts(
        self, 
        images: List[Dict[str, Any]], 
        cut_points: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Create image sequence configuration from images and producer cut points"""
        sequence = []
        
        # Ensure we have enough images for all cuts
        num_segments = min(len(images), len(cut_points))
        if len(images) != len(cut_points):
            print(f"⚠️  Warning: {len(images)} images found but {len(cut_points)} cuts defined")
            print(f"   Using {num_segments} segments")
        
        print(f"🎬 Creating sequence with {num_segments} segments")
        
        for i in range(num_segments):
            image = images[i]
            cut = cut_points[i]
            
            # Calculate timing
            start_time = cut['cut_time']
            if i < len(cut_points) - 1:
                end_time = cut_points[i + 1]['cut_time']
            else:
                # Last segment - add small buffer
                end_time = start_time + 2.5  # Default end
            
            duration = end_time - start_time
            
            # Create image config
            image_config = {
                "source": image['path'],
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "name": f"cut_{i+1}_{image['name'].split('.')[0]}",
                "cut_reason": cut.get('reason', 'Scene transition'),
                "cut_number": cut.get('cut_number', i + 1)
            }
            
            # No transitions - direct cuts only
            # (Removed crossfade transitions)
            
            # No Ken Burns effects - static images only
            # (Removed all zoom effects)
            
            sequence.append(image_config)
            print(f"  Cut {i+1}: {start_time:.2f}s - {end_time:.2f}s | {duration:.1f}s | {cut.get('reason', 'N/A')[:50]}...")
        
        return sequence
    
    def load_word_timestamps(self, transcription_file: Union[str, Path]) -> Tuple[str, List[Dict[str, Any]]]:
        """Load word timestamps from transcription file"""
        with open(transcription_file, 'r') as f:
            data = json.load(f)
        
        transcript = data.get('transcript', '')
        words = []
        
        for item in data.get("word_timestamps", []):
            words.append({
                "word": item["word"],
                "start": item["start"],
                "end": item["end"]
            })
        
        print(f"📝 Loaded transcript: {len(words)} words, {len(transcript)} characters")
        print(f"   Preview: \"{transcript[:80]}...\"")
        
        return transcript, words
    
    def create_composition(
        self,
        resolution: Tuple[int, int],
        duration: float,
        fps: int = 30,
        background_color: Tuple[int, int, int] = (0, 0, 0)
    ):
        """Create main Movis composition"""
        self.composition = mv.layer.Composition(size=resolution, duration=duration)
        
        # Add black background
        bg_layer = mv.layer.Rectangle(
            size=resolution,
            color=background_color,
            duration=duration
        )
        self.composition.add_layer(bg_layer, name="background")
        
        print(f"🎯 Created composition: {resolution[0]}x{resolution[1]} @ {fps}fps, {duration:.1f}s")
    
    def add_image_sequence(self, sequence_config: List[Dict[str, Any]]):
        """Add image sequence to composition with proper scaling and transitions"""
        for i, image_config in enumerate(sequence_config):
            source = image_config['source']
            start_time = image_config['start_time']
            end_time = image_config['end_time']
            duration = image_config['duration']
            
            # Calculate proper scale to cover entire screen
            from PIL import Image
            try:
                with Image.open(source) as img:
                    image_size = img.size  # (width, height)
                cover_scale = self.calculate_cover_scale(image_size, self.composition.size)
            except Exception as e:
                print(f"Warning: Could not determine image size for {source}, using default scale. Error: {e}")
                cover_scale = 1.2  # Default cover scale
            
            # Create image layer
            image_layer = mv.layer.Image(str(source), duration=duration)
            
            # Center position
            center_x = self.composition.size[0] // 2
            center_y = self.composition.size[1] // 2
            
            # Add the image layer
            layer_item = self.composition.add_layer(
                image_layer,
                name=image_config.get('name', f'image_seq_{i}'),
                position=(center_x, center_y),
                scale=(cover_scale, cover_scale),
                opacity=1.0,
                offset=start_time
            )
            
            # No transitions or Ken Burns effects applied
            # Direct cuts with static images only
    
    def _apply_image_transition(self, layer_item: mv.layer.LayerItem, transition: Dict[str, Any], duration: float):
        """Apply transition effects to image"""
        transition_type = transition.get('type', 'crossfade')
        transition_duration = transition.get('duration', 0.4)
        
        if transition_type == 'crossfade':
            # Fade in at start
            layer_item.opacity.enable_motion().extend(
                keyframes=[0.0, transition_duration],
                values=[0.0, 1.0],
                easings=['ease_out']
            )
    
    def _apply_ken_burns(self, layer_item: mv.layer.LayerItem, ken_burns: Dict[str, Any], duration: float, base_scale: float):
        """Apply Ken Burns effect (zoom and pan)"""
        effect_type = ken_burns.get('type', 'zoom_in')
        
        if effect_type == 'zoom_in':
            start_scale_factor = ken_burns.get('start_scale', 1.0)
            end_scale_factor = ken_burns.get('end_scale', 1.2)
            start_scale = base_scale * start_scale_factor
            end_scale = base_scale * end_scale_factor
            
            layer_item.scale.enable_motion().extend(
                keyframes=[0.0, duration],
                values=[(start_scale, start_scale), (end_scale, end_scale)],
                easings=['ease_in_out']
            )
        elif effect_type == 'zoom_out':
            start_scale_factor = ken_burns.get('start_scale', 1.2)
            end_scale_factor = ken_burns.get('end_scale', 1.0)
            start_scale = base_scale * start_scale_factor
            end_scale = base_scale * end_scale_factor
            
            layer_item.scale.enable_motion().extend(
                keyframes=[0.0, duration],
                values=[(start_scale, start_scale), (end_scale, end_scale)],
                easings=['ease_in_out']
            )
    
    def add_audio_layer(self, audio_file: Union[str, Path]):
        """Add audio narration to composition"""
        audio_layer = mv.layer.Audio(str(audio_file))
        
        layer_item = self.composition.add_layer(
            audio_layer,
            name="narration",
            audio_level=0.0  # Full volume for narration
        )
        
        print(f"🔊 Added audio: {Path(audio_file).name} ({audio_layer.duration:.1f}s)")
        return layer_item
    
    def add_subtitle_layer(
        self,
        words: List[Dict[str, Any]],
        style_name: str,
        position: str = "bottom",
        safe_zones: bool = True
    ) -> Optional[mv.layer.LayerItem]:
        """Add professional subtitle layer with specified style"""
        
        if style_name not in self.available_styles:
            print(f"❌ Error: Unknown subtitle style '{style_name}'")
            print(f"   Available styles: {', '.join(self.available_styles)}")
            return None
        
        # Load subtitle style
        style = StyleLoader.load_style_from_json(self.subtitle_styles_path, style_name)
        if not style:
            print(f"❌ Error: Could not load subtitle style '{style_name}'")
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
        
        print(f"✅ Added subtitle layer: {style.config.get('name', style_name)}")
        print(f"   Effect type: {style.config.get('effect_type', 'unknown')}")
        print(f"   Font: {Path(style.config['typography']['font_family']).name}")
        
        return layer_item
    
    def export_video(
        self,
        output_path: Union[str, Path],
        quality: str = 'high',
        fps: int = 30
    ):
        """Export video with specified quality settings"""
        if not self.composition:
            print("❌ Error: No composition to export")
            return False
        
        output_path = Path(output_path)
        
        # Quality settings
        quality_settings = {
            'low': {'crf': 28, 'preset': 'faster'},
            'medium': {'crf': 23, 'preset': 'medium'},
            'high': {'crf': 18, 'preset': 'slow'}
        }
        
        settings = quality_settings.get(quality, quality_settings['medium'])
        
        # Export parameters
        output_params = [
            '-crf', str(settings['crf']),
            '-preset', settings['preset']
        ]
        
        print(f"🎬 Exporting video...")
        print(f"   Quality: {quality} (CRF: {settings['crf']})")
        print(f"   Output: {output_path}")
        
        try:
            self.composition.write_video(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                fps=fps,
                pixelformat='yuv420p',
                output_params=output_params
            )
            
            print(f"✅ Video export complete!")
            print(f"   Duration: {self.composition.duration:.1f}s")
            print(f"   Resolution: {self.composition.size[0]}x{self.composition.size[1]}")
            
            return True
            
        except Exception as e:
            print(f"❌ Export error: {e}")
            import traceback
            traceback.print_exc()
            return False


def create_integrated_video(
    assets_dir: Path,
    cut_plan_file: Union[str, Path],
    audio_file: Union[str, Path],
    transcription_file: Union[str, Path],
    output_path: Union[str, Path],
    subtitle_style: str = 'simple_caption',
    video_format: str = '3:2',
    quality: str = 'high'
) -> bool:
    """Main function to create integrated video with all components"""
    
    print("🎬 VinVideo Integrated Editing Pipeline")
    print("=" * 60)
    print(f"Assets Directory: {assets_dir}")
    print(f"Cut Plan: {Path(cut_plan_file).name}")
    print(f"Audio: {Path(audio_file).name}")
    print(f"Transcription: {Path(transcription_file).name}")
    print(f"Subtitle Style: {subtitle_style}")
    print(f"Video Format: {video_format}")
    print(f"Output: {output_path}")
    print("=" * 60)
    
    # Initialize editor
    editor = IntegratedVideoEditor()
    
    # Load producer cuts
    print("\n📋 Loading Producer Cut Plan...")
    try:
        cut_points = editor.load_producer_cuts(cut_plan_file)
        print(f"✅ Loaded {len(cut_points)} cut points")
        
        # Show first few cuts
        for i, cut in enumerate(cut_points[:3]):
            print(f"   Cut {i+1}: {cut['cut_time']:.2f}s - {cut.get('reason', 'N/A')[:50]}...")
        if len(cut_points) > 3:
            print(f"   ... and {len(cut_points) - 3} more cuts")
            
    except Exception as e:
        print(f"❌ Error loading cut plan: {e}")
        return False
    
    # Discover image assets
    print(f"\n📁 Discovering Image Assets...")
    images = editor.discover_image_assets(assets_dir)
    if not images:
        print("❌ Error: No image assets found")
        return False
    
    # Load word timestamps
    print(f"\n📝 Loading Word Timestamps...")
    try:
        transcript, words = editor.load_word_timestamps(transcription_file)
        if not words:
            print("❌ Error: No word timestamps found")
            return False
    except Exception as e:
        print(f"❌ Error loading transcription: {e}")
        return False
    
    # Calculate video duration and resolution
    total_duration = cut_points[-1]['cut_time'] + 2.0  # Add buffer at end
    resolution = get_resolution_from_format(video_format)
    
    print(f"\n🎯 Creating Composition...")
    print(f"   Resolution: {resolution[0]}x{resolution[1]} ({video_format})")
    print(f"   Duration: {total_duration:.1f}s")
    
    # Create composition
    editor.create_composition(
        resolution=resolution,
        duration=total_duration,
        fps=30,
        background_color=(0, 0, 0)
    )
    
    # Create image sequence from cuts
    print(f"\n🎬 Creating Image Sequence...")
    sequence_config = editor.create_image_sequence_from_cuts(images, cut_points)
    
    # Add image sequence
    print(f"\n📸 Adding Image Sequence...")
    editor.add_image_sequence(sequence_config)
    
    # Add audio
    print(f"\n🔊 Adding Audio...")
    editor.add_audio_layer(audio_file)
    
    # Add subtitles
    print(f"\n📝 Adding Subtitles...")
    subtitle_layer = editor.add_subtitle_layer(
        words=words,
        style_name=subtitle_style,
        position="bottom",
        safe_zones=True
    )
    
    if not subtitle_layer:
        print("❌ Failed to add subtitle layer")
        return False
    
    # Export video
    print(f"\n🎬 Exporting Video...")
    success = editor.export_video(
        output_path=output_path,
        quality=quality,
        fps=30
    )
    
    if success:
        print(f"\n🎉 SUCCESS! Integrated video created!")
        print(f"   🎬 {len(sequence_config)} image segments")
        print(f"   🔊 Audio narration")
        print(f"   📝 {len(words)} word timestamps")
        print(f"   ✨ {subtitle_style} subtitle style")
        print(f"   📐 {video_format} format ({resolution[0]}x{resolution[1]})")
        print(f"   📁 Output: {output_path}")
        return True
    else:
        print(f"\n❌ Video export failed")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='VinVideo Integrated Editing Pipeline - Producer cuts + Images + Subtitles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic 3:2 video with simple captions
  python3 integrated_editing_pipeline.py --assets-dir ASSETS_3 --style simple_caption

  # 9:16 Instagram video with highlight captions
  python3 integrated_editing_pipeline.py --assets-dir ASSETS_3 --format 9:16 --style highlight_caption

  # Custom output with specific quality
  python3 integrated_editing_pipeline.py --assets-dir ASSETS_3 --style karaoke_style --output my_video.mp4 --quality high

  # All available subtitle styles:
  simple_caption, background_caption, glow_caption, karaoke_style,
  highlight_caption, deep_diver, popling_caption, greengoblin, sgone_caption
        """
    )
    
    # Required arguments
    parser.add_argument('--assets-dir', type=str, required=True,
                        help='Path to assets directory (e.g., ASSETS_3)')
    
    # Optional arguments
    parser.add_argument('--cut-plan', type=str,
                        help='Path to producer cut plan JSON (default: assets-dir/producer_cut_plan.json)')
    parser.add_argument('--audio', type=str,
                        help='Path to audio file (default: search in assets-dir)')
    parser.add_argument('--transcription', type=str,
                        help='Path to transcription JSON (default: search in assets-dir)')
    parser.add_argument('--style', type=str, default='simple_caption',
                        choices=['simple_caption', 'background_caption', 'glow_caption', 'karaoke_style',
                                'highlight_caption', 'deep_diver', 'popling_caption', 'greengoblin', 'sgone_caption'],
                        help='Subtitle style to use')
    parser.add_argument('--format', type=str, default='3:2',
                        help='Video format ratio (3:2, 9:16, 16:9, 4:5, 1:1, etc.)')
    parser.add_argument('--output', '-o', type=str, default='integrated_video.mp4',
                        help='Output video file path')
    parser.add_argument('--quality', type=str, choices=['low', 'medium', 'high'], default='high',
                        help='Export quality level')
    
    args = parser.parse_args()
    
    # Validate assets directory
    assets_dir = Path(args.assets_dir)
    if not assets_dir.exists():
        print(f"❌ Error: Assets directory not found: {assets_dir}")
        return 1
    
    # Auto-discover files if not specified
    cut_plan_file = args.cut_plan or assets_dir / "producer_cut_plan.json"
    
    # Find audio file
    if args.audio:
        audio_file = Path(args.audio)
    else:
        audio_files = list(assets_dir.glob("*.wav")) + list(assets_dir.glob("*.mp3"))
        if not audio_files:
            print(f"❌ Error: No audio file found in {assets_dir}")
            return 1
        audio_file = audio_files[0]
    
    # Find transcription file
    if args.transcription:
        transcription_file = Path(args.transcription)
    else:
        transcription_files = list(assets_dir.glob("*_transcription.json"))
        if not transcription_files:
            print(f"❌ Error: No transcription file found in {assets_dir}")
            return 1
        transcription_file = transcription_files[0]
    
    # Validate required files
    for file_path, name in [(cut_plan_file, "cut plan"), (audio_file, "audio"), (transcription_file, "transcription")]:
        if not file_path.exists():
            print(f"❌ Error: {name} file not found: {file_path}")
            return 1
    
    # Create integrated video
    success = create_integrated_video(
        assets_dir=assets_dir,
        cut_plan_file=cut_plan_file,
        audio_file=audio_file,
        transcription_file=transcription_file,
        output_path=args.output,
        subtitle_style=args.style,
        video_format=args.format,
        quality=args.quality
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())