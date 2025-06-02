#!/usr/bin/env python3
"""
Dynamic Assets Video Generator
Creates video using assets folder: images, cut times, audio, and subtitles
Completely dynamic - no hardcoded values
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Add movis directory to path
movis_dir = os.path.join(current_dir, 'movis')
if os.path.exists(movis_dir):
    sys.path.insert(0, movis_dir)

from dynamic_video_editor import DynamicVideoEditor


def load_cut_times(cuts_json_path: Path) -> List[Dict[str, Any]]:
    """Load cut times from JSON file"""
    with open(cuts_json_path, 'r') as f:
        return json.load(f)


def discover_assets(assets_dir: Path) -> Dict[str, Any]:
    """Dynamically discover all assets in the assets directory"""
    assets = {
        'images': [],
        'audio_file': None,
        'transcription_file': None,
        'cuts_file': None
    }
    
    # Find all numbered images (looking for image_N_timestamp.png pattern)
    for i in range(1, 33):  # Looking for 1-32
        # Look for the pattern image_N_timestamp.png
        matching_files = list(assets_dir.glob(f"image_{i}_*.png"))
        if matching_files:
            # Use the first match (should only be one)
            image_path = matching_files[0]
            assets['images'].append({
                'number': i,
                'path': str(image_path)
            })
    
    # Sort images by number to ensure correct order
    assets['images'].sort(key=lambda x: x['number'])
    
    # Find WAV audio file
    for file in assets_dir.glob("*.wav"):
        assets['audio_file'] = str(file)
        break
    
    # Find transcription JSON (not video_cuts.json)
    for file in assets_dir.glob("*_transcription.json"):
        assets['transcription_file'] = str(file)
        break
    
    # Find cuts JSON
    cuts_file = assets_dir / "video_cuts.json"
    if cuts_file.exists():
        assets['cuts_file'] = str(cuts_file)
    
    return assets


def create_image_sequence_config(images: List[Dict], cut_times: List[Dict]) -> List[Dict[str, Any]]:
    """Create image sequence configuration from images and cut times"""
    sequence = []
    
    # Ensure we have the right number of images
    if len(images) != len(cut_times):
        print(f"Warning: {len(images)} images found but {len(cut_times)} cuts defined")
        # Use minimum of both
        num_segments = min(len(images), len(cut_times))
    else:
        num_segments = len(images)
    
    print(f"Creating sequence with {num_segments} segments")
    
    for i in range(num_segments):
        image = images[i]
        cut = cut_times[i]
        
        # Calculate timing
        if i == 0:
            start_time = 0.0
        else:
            start_time = cut_times[i-1]['cut_time']
        
        end_time = cut['cut_time']
        
        # Create image config
        image_config = {
            "source": image['path'],
            "start_time": start_time,
            "end_time": end_time,
            "name": f"image_{i+1}",
            "position": [540, 960],  # Center position for 1080x1920
            "scale": 1.0,
            "opacity": 1.0
        }
        
        # Add Ken Burns effect for variety (alternate zoom in/out)
        if i % 2 == 0:
            image_config["ken_burns"] = {
                "type": "zoom_in",
                "start_scale": 1.0,
                "end_scale": 1.15
            }
        else:
            image_config["ken_burns"] = {
                "type": "zoom_out", 
                "start_scale": 1.15,
                "end_scale": 1.0
            }
        
        sequence.append(image_config)
        print(f"  Segment {i+1}: {start_time:.2f}s - {end_time:.2f}s ({image['path'].split('/')[-1]})")
    
    return sequence


def calculate_total_duration(cut_times: List[Dict]) -> float:
    """Calculate total video duration from cut times"""
    if not cut_times:
        return 10.0  # Default duration
    
    return cut_times[-1]['cut_time'] + 0.5  # Add small buffer at end


def create_timeline_config(assets: Dict[str, Any], cut_times: List[Dict]) -> Dict[str, Any]:
    """Create complete timeline configuration"""
    
    total_duration = calculate_total_duration(cut_times)
    
    # Create image sequence
    image_sequence = create_image_sequence_config(assets['images'], cut_times)
    
    # Build timeline configuration
    config = {
        "composition": {
            "resolution": [1080, 1920],  # Instagram format
            "duration": total_duration,
            "fps": 30,
            "background_color": [0, 0, 0]  # Black background
        },
        "image_sequence": image_sequence,
        "audio": {},
        "export": {
            "platform": "instagram",
            "quality": "high"
        }
    }
    
    # Add audio if available
    if assets['audio_file']:
        config["audio"]["narration"] = {
            "source": assets['audio_file'],
            "offset": 0.0,
            "level": 0.0
        }
        print(f"Added audio: {assets['audio_file'].split('/')[-1]}")
    
    # Add subtitles if transcription available
    if assets['transcription_file']:
        config["subtitles"] = {
            "parakeet_data": assets['transcription_file'],
            "style": "popling_caption",
            "position": "bottom"
        }
        print(f"Added subtitles: {assets['transcription_file'].split('/')[-1]}")
    
    return config


def generate_video(assets_dir: Path, output_path: Path, save_config: bool = False):
    """Generate video from assets directory"""
    
    print(f"\n🎬 Dynamic Video Generation from Assets")
    print("=" * 50)
    print(f"Assets Directory: {assets_dir}")
    print(f"Output Path: {output_path}")
    
    # Discover assets
    print(f"\n📁 Discovering Assets...")
    assets = discover_assets(assets_dir)
    
    print(f"Found {len(assets['images'])} images:")
    for img in assets['images']:
        print(f"  - {img['path'].split('/')[-1]}")
    
    if assets['audio_file']:
        print(f"Found audio: {assets['audio_file'].split('/')[-1]}")
    else:
        print("No audio file found")
    
    if assets['transcription_file']:
        print(f"Found transcription: {assets['transcription_file'].split('/')[-1]}")
    else:
        print("No transcription file found")
    
    # Load cut times
    if not assets['cuts_file']:
        print("❌ Error: video_cuts.json not found in assets directory")
        return False
    
    print(f"\n⏱️  Loading Cut Times...")
    cut_times = load_cut_times(Path(assets['cuts_file']))
    print(f"Loaded {len(cut_times)} cut points")
    
    # Validate we have enough images
    if len(assets['images']) < len(cut_times):
        print(f"⚠️  Warning: Only {len(assets['images'])} images found for {len(cut_times)} cuts")
    
    # Create timeline configuration
    print(f"\n🎯 Creating Timeline Configuration...")
    timeline_config = create_timeline_config(assets, cut_times)
    
    total_duration = timeline_config['composition']['duration']
    print(f"Total video duration: {total_duration:.2f}s")
    
    # Save configuration if requested
    if save_config:
        config_path = output_path.parent / f"{output_path.stem}_config.json"
        with open(config_path, 'w') as f:
            json.dump(timeline_config, f, indent=2)
        print(f"💾 Saved configuration to: {config_path}")
    
    # Create video using DynamicVideoEditor
    print(f"\n🎬 Generating Video...")
    editor = DynamicVideoEditor()
    
    try:
        # Process timeline configuration
        editor.process_timeline_config(timeline_config)
        
        # Export video
        editor.export_video(
            output_path,
            platform=timeline_config['export']['platform'],
            quality=timeline_config['export']['quality']
        )
        
        print(f"\n✅ Video generation complete!")
        print(f"   Output: {output_path}")
        print(f"   Duration: {total_duration:.1f}s")
        print(f"   Resolution: {timeline_config['composition']['resolution']}")
        print(f"   Images: {len(assets['images'])} segments")
        if assets['audio_file']:
            print(f"   Audio: ✓ Included")
        if assets['transcription_file']:
            print(f"   Subtitles: ✓ Highlight Caption style")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Dynamic Assets Video Generator - Create video from assets folder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate video from assets folder
  python3 dynamic_assets_video_generator.py

  # Specify custom output path
  python3 dynamic_assets_video_generator.py --output my_video.mp4

  # Save timeline configuration
  python3 dynamic_assets_video_generator.py --save-config

  # Use custom assets directory
  python3 dynamic_assets_video_generator.py --assets-dir /path/to/assets
        """
    )
    
    # Arguments
    parser.add_argument('--assets-dir', type=str,
                        help='Path to assets directory (default: ./assets)')
    parser.add_argument('--output', '-o', type=str, default='dynamic_assets_video.mp4',
                        help='Output video file path')
    parser.add_argument('--save-config', action='store_true',
                        help='Save timeline configuration JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    
    args = parser.parse_args()
    
    # Determine assets directory
    if args.assets_dir:
        assets_dir = Path(args.assets_dir)
    else:
        # Default to assets folder in same directory as script
        script_dir = Path(__file__).parent
        assets_dir = script_dir / "assets"
    
    # Validate assets directory
    if not assets_dir.exists():
        print(f"❌ Error: Assets directory not found: {assets_dir}")
        return 1
    
    # Output path
    output_path = Path(args.output)
    
    # Generate video
    success = generate_video(assets_dir, output_path, args.save_config)
    
    if success:
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())