#!/usr/bin/env python3
"""
Test script to generate videos for all subtitle styles using Game of Thrones images
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dynamic_video_editor import DynamicVideoEditor

def create_got_editing_plan():
    """Create an editing plan using Game of Thrones images"""
    
    # Load the word timestamps
    with open('other_root_files/parakeet_output.json', 'r') as f:
        parakeet_data = json.load(f)
    
    # Get image paths
    image_dir = Path('game_of_thrones_images')
    images = sorted([str(image_dir / f) for f in os.listdir(image_dir) if f.endswith('.png')])
    
    # Create editing plan with equal duration for each image
    total_duration = parakeet_data['word_timestamps'][-1]['end']
    image_duration = total_duration / len(images)
    
    editing_plan = {
        "project_name": "Game of Thrones Style Test",
        "resolution": [1080, 1920],
        "fps": 30,
        "timeline": {
            "segments": []
        }
    }
    
    # Create segments for each image
    for i, image_path in enumerate(images):
        start_time = i * image_duration
        end_time = (i + 1) * image_duration if i < len(images) - 1 else total_duration
        
        segment = {
            "type": "image",
            "start": start_time,
            "end": end_time,
            "asset": {
                "path": image_path,
                "type": "image"
            },
            "effects": {
                "scale_mode": "fit",  # This ensures images fit properly
                "position": "center"
            }
        }
        
        # Add transition on all segments except the first
        if i > 0:
            segment["transition"] = {
                "type": "crossfade",
                "duration": 0.5
            }
        
        editing_plan["timeline"]["segments"].append(segment)
    
    # Add audio segment
    audio_segment = {
        "type": "audio",
        "start": 0,
        "end": total_duration,
        "asset": {
            "path": "other_root_files/got_script.mp3",
            "type": "audio"
        }
    }
    editing_plan["timeline"]["segments"].append(audio_segment)
    
    return editing_plan

def test_all_styles():
    """Test all subtitle styles from the config"""
    
    # Load subtitle styles config
    with open('subtitle_styles/config/subtitle_styles_v3.json', 'r') as f:
        styles_config = json.load(f)
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output_test/got_styles_test_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all style names
    style_names = list(styles_config.keys())
    
    print(f"\nTesting {len(style_names)} subtitle styles:")
    for style in style_names:
        print(f"  - {style}")
    
    # Create editing plan
    editing_plan = create_got_editing_plan()
    
    # Process each style
    successful_styles = []
    failed_styles = []
    
    for i, style_name in enumerate(style_names, 1):
        print(f"\n[{i}/{len(style_names)}] Processing {style_name}...")
        
        try:
            # Create editor instance
            editor = DynamicVideoEditor()
            
            # Create timeline config with subtitles
            timeline_config = {
                "composition": {
                    "resolution": [1080, 1920],
                    "fps": 30,
                    "duration": editing_plan["timeline"]["segments"][-2]["end"]  # Last image end time
                },
                "layers": [],
                "audio": {
                    "main": {
                        "path": "other_root_files/got_script.mp3"
                    }
                },
                "subtitles": {
                    "enabled": True,
                    "style": style_name,
                    "parakeet_data": "other_root_files/parakeet_output.json"
                },
                "image_sequence": {
                    "images": [seg["asset"]["path"] for seg in editing_plan["timeline"]["segments"] if seg["type"] == "image"],
                    "display_duration": editing_plan["timeline"]["segments"][0]["end"],
                    "transition": "crossfade",
                    "transition_duration": 0.5,
                    "scale_mode": "fit"
                }
            }
            
            # Process timeline
            editor.process_timeline_config(timeline_config)
            
            # Export video
            output_path = str(output_dir / f"{style_name}_got.mp4")
            editor.export_video(output_path, quality='high')
            
            print(f"✓ Successfully created: {style_name}")
            successful_styles.append(style_name)
                
        except Exception as e:
            print(f"✗ Error processing {style_name}: {str(e)}")
            failed_styles.append((style_name, str(e)))
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY - Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print(f"Total styles tested: {len(style_names)}")
    print(f"Successful: {len(successful_styles)}")
    print(f"Failed: {len(failed_styles)}")
    print(f"\nOutput directory: {output_dir}")
    
    if successful_styles:
        print(f"\nSuccessful styles ({len(successful_styles)}):")
        for style in successful_styles:
            print(f"  ✓ {style}")
    
    if failed_styles:
        print(f"\nFailed styles ({len(failed_styles)}):")
        for style, error in failed_styles:
            print(f"  ✗ {style}: {error}")
    
    print(f"\nAll videos saved to: {output_dir}/")

if __name__ == "__main__":
    test_all_styles()