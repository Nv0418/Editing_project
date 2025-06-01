#!/usr/bin/env python3
"""
Quick test script for Dynamic Video Editor with all 9 subtitle styles
Uses simplified configuration for faster testing
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dynamic_video_editor import DynamicVideoEditor

def test_single_style_quick(style_name: str, output_dir: Path) -> dict:
    """Test a single style with quick configuration"""
    
    try:
        # Create editor instance
        editor = DynamicVideoEditor()
        
        # Use just 3 images for quick testing
        image_dir = Path("game_of_thrones_images")
        images = sorted(list(image_dir.glob("*.png")))[:3]
        
        # Quick image sequence - 10 second total video
        image_sequence = []
        for i, image_path in enumerate(images):
            image_config = {
                "source": str(image_path),
                "start_time": i * 3.0,
                "end_time": (i + 1) * 3.0 + 0.5,  # 3.5s per image with overlap
                "position": [540, 960],
                "scale": 1.0
            }
            image_sequence.append(image_config)
        
        # Create timeline configuration for 10 seconds
        config = {
            "composition": {
                "resolution": [1080, 1920],
                "duration": 10.0,  # Short duration for quick test
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
        
        # Process the timeline configuration
        editor.process_timeline_config(config)
        
        # Set output path
        output_path = output_dir / f"{style_name}_quick_test.mp4"
        
        # Export video with medium quality for speed
        editor.export_video(
            output_path,
            platform="instagram",
            quality="medium"
        )
        
        # Verify output
        if output_path.exists():
            file_size = output_path.stat().st_size / (1024 * 1024)  # Size in MB
            return {
                "style": style_name,
                "status": "success",
                "output": str(output_path),
                "size_mb": round(file_size, 1)
            }
        else:
            return {
                "style": style_name,
                "status": "failed",
                "error": "Output file not created"
            }
            
    except Exception as e:
        return {
            "style": style_name,
            "status": "error",
            "error": str(e)
        }

def test_all_styles_quick():
    """Quick test of all 9 subtitle styles"""
    
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
    
    # Verify assets exist
    audio_path = "other_root_files/got_script.mp3"
    parakeet_path = "other_root_files/parakeet_output.json"
    
    if not Path(audio_path).exists():
        print(f"Error: Audio file not found: {audio_path}")
        return
    
    if not Path(parakeet_path).exists():
        print(f"Error: Parakeet file not found: {parakeet_path}")
        return
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"output_test/quick_test_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🚀 Quick Test - Dynamic Video Editor with all 9 subtitle styles")
    print(f"📁 Output directory: {output_dir}")
    print(f"⏱️  Video duration: 10 seconds each")
    print(f"🖼️  Using 3 Game of Thrones images")
    print(f"🎵 Audio: {audio_path}")
    print(f"📝 Subtitles: {parakeet_path}")
    print("-" * 60)
    
    results = []
    
    for i, style in enumerate(styles, 1):
        print(f"\n[{i}/{len(styles)}] Testing style: {style}")
        
        result = test_single_style_quick(style, output_dir)
        results.append(result)
        
        if result["status"] == "success":
            print(f"   ✅ Success: {result['size_mb']} MB")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Generate summary report
    print("\n" + "=" * 60)
    print("🎯 QUICK TEST RESULTS")
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
    
    # Save results
    results_file = output_dir / "quick_test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "test_type": "quick_test",
            "duration_seconds": 10,
            "total_styles": len(styles),
            "successful": len(successful),
            "failed": len(failed),
            "results": results
        }, f, indent=2)
    
    print(f"\n📊 Results saved to: {results_file}")
    print(f"📁 All videos in directory: {output_dir}")
    
    return results

def main():
    """Main function to run the quick test"""
    print("🎬 VinVideo Dynamic Editor - Quick Test")
    print("Testing all 9 professional subtitle styles (10 seconds each)")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Run the test
    results = test_all_styles_quick()
    
    if results:
        successful = len([r for r in results if r["status"] == "success"])
        total = len(results)
        print(f"\n🎉 Quick test completed: {successful}/{total} styles successful!")
        
        if successful == total:
            print("🌟 All styles working perfectly with the Dynamic Video Editor!")
        
    else:
        print("\n❌ Test failed to run")

if __name__ == "__main__":
    main()