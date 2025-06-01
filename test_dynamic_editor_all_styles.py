#!/usr/bin/env python3
"""
Test script for Dynamic Video Editor with all 9 subtitle styles
Uses Game of Thrones images, got_script.mp3 audio, and parakeet_output.json
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_video_editor import DynamicVideoEditor

def create_got_image_sequence_config():
    """Create image sequence configuration for Game of Thrones images"""
    
    # Get all Game of Thrones images
    image_dir = Path("game_of_thrones_images")
    images = sorted(list(image_dir.glob("*.png")))
    
    if not images:
        print(f"Error: No images found in {image_dir}")
        return None
    
    print(f"Found {len(images)} Game of Thrones images")
    
    # Create image sequence - each image shows for ~2.5 seconds with 0.5s transitions
    image_sequence = []
    duration_per_image = 2.5
    transition_duration = 0.5
    
    current_time = 0.0
    for i, image_path in enumerate(images):
        # Calculate timing with overlap for transitions
        start_time = current_time
        end_time = start_time + duration_per_image
        
        image_config = {
            "source": str(image_path),
            "start_time": start_time,
            "end_time": end_time,
            "position": [540, 960],  # Center of 1080x1920 canvas
            "scale": 1.0,  # Auto-scaling will be applied
            "name": f"got_image_{i+1}"
        }
        
        # Add Ken Burns effect for visual interest
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
        
        # Add crossfade transition (except for first image)
        if i > 0:
            image_config["transition"] = {
                "type": "crossfade",
                "duration": transition_duration
            }
        
        image_sequence.append(image_config)
        current_time += duration_per_image - transition_duration
    
    # Calculate total duration
    total_duration = current_time + transition_duration
    
    return image_sequence, total_duration

def test_all_subtitle_styles():
    """Test dynamic video editor with all 9 subtitle styles"""
    
    # All 9 finalized subtitle styles
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
    
    # Create image sequence config
    image_sequence, total_duration = create_got_image_sequence_config()
    if not image_sequence:
        return
    
    # Paths to assets
    audio_path = "other_root_files/got_script.mp3"
    parakeet_path = "other_root_files/parakeet_output.json"
    
    # Verify assets exist
    if not Path(audio_path).exists():
        print(f"Error: Audio file not found: {audio_path}")
        return
    
    if not Path(parakeet_path).exists():
        print(f"Error: Parakeet file not found: {parakeet_path}")
        return
    
    # Create output directory with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output_test/dynamic_editor_all_styles_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🎬 Testing Dynamic Video Editor with all 9 subtitle styles")
    print(f"📁 Output directory: {output_dir}")
    print(f"⏱️  Total video duration: {total_duration:.1f}s")
    print(f"🖼️  Using {len(image_sequence)} Game of Thrones images")
    print(f"🎵 Audio: {audio_path}")
    print(f"📝 Subtitles: {parakeet_path}")
    print("-" * 60)
    
    results = []
    
    for i, style in enumerate(styles, 1):
        print(f"\n[{i}/{len(styles)}] Testing style: {style}")
        
        try:
            # Create editor instance
            editor = DynamicVideoEditor()
            
            # Create timeline configuration
            config = {
                "composition": {
                    "resolution": [1080, 1920],
                    "duration": total_duration,
                    "fps": 30,
                    "background_color": [0, 0, 0]  # Black background
                },
                "image_sequence": image_sequence,
                "audio": {
                    "narration": {
                        "source": audio_path,
                        "level": 0.0,
                        "offset": 0.0
                    }
                },
                "subtitles": {
                    "parakeet_data": parakeet_path,
                    "style": style,
                    "position": "bottom",
                    "safe_zones": True
                }
            }
            
            # Process the timeline configuration
            editor.process_timeline_config(config)
            
            # Set output path
            output_path = output_dir / f"{style}_got_test.mp4"
            
            # Export video optimized for Instagram
            print(f"   📹 Rendering {style}...")
            editor.export_video(
                output_path,
                platform="instagram",
                quality="high"
            )
            
            # Verify output
            if output_path.exists():
                file_size = output_path.stat().st_size / (1024 * 1024)  # Size in MB
                print(f"   ✅ Success: {output_path.name} ({file_size:.1f} MB)")
                results.append({
                    "style": style,
                    "status": "success",
                    "output": str(output_path),
                    "size_mb": round(file_size, 1)
                })
            else:
                print(f"   ❌ Failed: Output file not created")
                results.append({
                    "style": style,
                    "status": "failed",
                    "error": "Output file not created"
                })
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "style": style,
                "status": "error",
                "error": str(e)
            })
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("🎯 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]
    
    print(f"✅ Successful: {len(successful)}/{len(styles)} styles")
    print(f"❌ Failed: {len(failed)}/{len(styles)} styles")
    
    if successful:
        print(f"\n📹 Successfully generated videos:")
        for result in successful:
            print(f"   • {result['style']}: {result['size_mb']} MB")
    
    if failed:
        print(f"\n❌ Failed styles:")
        for result in failed:
            print(f"   • {result['style']}: {result.get('error', 'Unknown error')}")
    
    # Save detailed results
    results_file = output_dir / "test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "total_styles": len(styles),
            "successful": len(successful),
            "failed": len(failed),
            "config": {
                "duration": total_duration,
                "images": len(image_sequence),
                "audio": audio_path,
                "parakeet": parakeet_path,
                "platform": "instagram",
                "quality": "high"
            },
            "results": results
        }, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: {results_file}")
    print(f"📁 All videos in directory: {output_dir}")
    
    return results

def main():
    """Main function to run the test"""
    print("🎬 VinVideo Dynamic Editor - All Styles Test")
    print("Testing all 9 professional subtitle styles with Game of Thrones assets")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Run the test
    results = test_all_subtitle_styles()
    
    if results:
        successful = len([r for r in results if r["status"] == "success"])
        total = len(results)
        print(f"\n🎉 Test completed: {successful}/{total} styles successful!")
    else:
        print("\n❌ Test failed to run")

if __name__ == "__main__":
    main()