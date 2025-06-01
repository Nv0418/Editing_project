#!/usr/bin/env python3
"""
Create test videos for all 9 subtitle styles with Game of Thrones images
"""

import os
import json
from pathlib import Path

def create_got_image_sequence():
    """Create Game of Thrones image sequence configuration"""
    image_dir = Path("game_of_thrones_images")
    images = sorted(list(image_dir.glob("*.png")))
    
    # Create image sequence with all 8 images, 2.5 seconds each with 0.5s overlap
    image_sequence = []
    duration_per_image = 2.5
    transition_duration = 0.5
    
    current_time = 0.0
    for i, image_path in enumerate(images):
        start_time = current_time
        end_time = start_time + duration_per_image
        
        image_config = {
            "source": str(image_path),
            "start_time": start_time,
            "end_time": end_time,
            "position": [540, 960],
            "scale": 1.0,
            "name": f"got_image_{i+1}"
        }
        
        # Add Ken Burns effect for visual interest
        if i % 3 == 0:
            image_config["ken_burns"] = {
                "type": "zoom_in",
                "start_scale": 1.0,
                "end_scale": 1.15
            }
        elif i % 3 == 1:
            image_config["ken_burns"] = {
                "type": "zoom_out", 
                "start_scale": 1.15,
                "end_scale": 1.0
            }
        else:
            image_config["ken_burns"] = {
                "type": "pan",
                "start_position": [540, 960],
                "end_position": [520, 940]
            }
        
        # Add crossfade transition (except for first image)
        if i > 0:
            image_config["transition"] = {
                "type": "crossfade",
                "duration": transition_duration
            }
        
        image_sequence.append(image_config)
        current_time += duration_per_image - transition_duration
    
    # Calculate total duration (add back the last transition duration)
    total_duration = current_time + transition_duration
    
    return image_sequence, total_duration

def create_style_config(style_name, image_sequence, total_duration):
    """Create configuration for a specific style"""
    return {
        "composition": {
            "resolution": [1080, 1920],
            "duration": total_duration,
            "fps": 30,
            "background_color": [0, 0, 0]
        },
        "image_sequence": image_sequence,
        "audio": {
            "narration": {
                "source": "other_root_files/got_script.mp3",
                "level": 0.0,
                "offset": 0.0
            }
        },
        "subtitles": {
            "parakeet_data": "other_root_files/parakeet_output.json",
            "style": style_name,
            "position": "bottom",
            "safe_zones": True
        }
    }

def main():
    """Generate all test videos with Game of Thrones images"""
    
    # All 9 styles
    styles = [
        "simple_caption",
        "background_caption", 
        "glow_caption",
        "karaoke_style",
        "highlight_caption",
        "deep_diver",
        "popling_caption",
        "greengoblin",
        "sgone_caption"
    ]
    
    # Create image sequence
    image_sequence, total_duration = create_got_image_sequence()
    
    print(f"🎬 Creating test videos for all 9 styles with Game of Thrones images")
    print(f"📁 Image sequence: {len(image_sequence)} images")
    print(f"⏱️  Total duration: {total_duration:.1f} seconds")
    print("-" * 60)
    
    # Clean test_videos directory
    test_videos_dir = Path("test_videos")
    test_videos_dir.mkdir(exist_ok=True)
    
    # Remove old test files
    for old_file in test_videos_dir.glob("test_*_got.mp4"):
        old_file.unlink()
    
    for i, style in enumerate(styles, 1):
        print(f"\n[{i}/{len(styles)}] Processing style: {style}")
        
        # Create config file
        config = create_style_config(style, image_sequence, total_duration)
        config_file = f"config_{style}_got.json"
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Generate video
        output_file = f"test_videos/test_{style}_got.mp4"
        
        print(f"   📝 Created config: {config_file}")
        print(f"   🎥 Generating: {output_file}")
        
        # Run dynamic video editor
        cmd = f'python3 dynamic_video_editor.py --config {config_file} --platform instagram --quality medium --output {output_file}'
        result = os.system(cmd)
        
        if result == 0:
            # Check if file was created and get size
            output_path = Path(output_file)
            if output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"   ✅ Success: {size_mb:.1f} MB")
            else:
                print(f"   ❌ Failed: Output file not created")
        else:
            print(f"   ❌ Failed: Command returned error code {result}")
        
        # Clean up config file
        os.remove(config_file)
    
    print(f"\n🎉 Test video generation complete!")
    print(f"📁 All videos saved to: test_videos/")
    
    # List final results
    print(f"\n📋 Generated videos:")
    for style in styles:
        output_file = Path(f"test_videos/test_{style}_got.mp4")
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"   ✅ test_{style}_got.mp4 ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ test_{style}_got.mp4 (MISSING)")

if __name__ == "__main__":
    main()