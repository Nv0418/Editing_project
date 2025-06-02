#!/usr/bin/env python3
"""
Full VinVideo Editing Pipeline
Complete workflow from agent inputs to final video
"""

import json
import os
import argparse
from pathlib import Path
from datetime import datetime
import logging

# Import our components
from editing_agent import (
    EditingAgent, 
    ProducerOutput, 
    DirectorOutput, 
    PromptEngineerOutput,
    create_mock_agent_outputs
)
from editing_agent_to_movis import EditingAgentConverter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_agent_outputs_from_files(producer_file: str, director_file: str, prompt_engineer_file: str):
    """Load agent outputs from JSON files"""
    
    # Load Producer output
    with open(producer_file, 'r') as f:
        producer_data = json.load(f)
    
    producer_output = ProducerOutput(
        agent_type="producer",
        timestamp=producer_data.get("timestamp", datetime.now().isoformat()),
        data=producer_data,
        shot_count=producer_data["shot_count"],
        total_duration=producer_data["total_duration"],
        beat_durations=producer_data["beat_durations"],
        asset_paths=producer_data["asset_paths"]
    )
    
    # Load Director output
    with open(director_file, 'r') as f:
        director_data = json.load(f)
    
    director_output = DirectorOutput(
        agent_type="director",
        timestamp=director_data.get("timestamp", datetime.now().isoformat()),
        data=director_data,
        genre=director_data["genre"],
        tone=director_data["tone"],
        pacing=director_data["pacing"],
        story_arc=director_data["story_arc"],
        emotional_beats=director_data["emotional_beats"]
    )
    
    # Load Prompt Engineer output
    with open(prompt_engineer_file, 'r') as f:
        pe_data = json.load(f)
    
    prompt_engineer_output = PromptEngineerOutput(
        agent_type="prompt_engineer",
        timestamp=pe_data.get("timestamp", datetime.now().isoformat()),
        data=pe_data,
        beat_contexts=pe_data["beat_contexts"]
    )
    
    return producer_output, director_output, prompt_engineer_output


def create_sample_agent_files(output_dir: str):
    """Create sample agent output files for testing"""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Sample Producer output
    producer_data = {
        "timestamp": datetime.now().isoformat(),
        "shot_count": 4,
        "total_duration": 20.0,
        "beat_durations": {
            "beat_01": 5.0,
            "beat_02": 5.0,
            "beat_03": 5.0,
            "beat_04": 5.0
        },
        "asset_paths": {
            "beat_01": "/Users/naman/Desktop/movie_py/media/VIDEOS_TEST/comfyuiblog_00004.mp4",
            "beat_02": "/Users/naman/Desktop/movie_py/media/VIDEOS_TEST/comfyuiblog_00005.mp4",
            "beat_03": "/Users/naman/Desktop/movie_py/media/VIDEOS_TEST/comfyuiblog_00006.mp4",
            "beat_04": "/Users/naman/Desktop/movie_py/media/VIDEOS_TEST/comfyuiblog_00007.mp4"
        },
        "audio_path": "other_root_files/got_script.mp3",
        "subtitle_data": "other_root_files/parakeet_output.json"
    }
    
    with open(output_dir / "producer_output.json", 'w') as f:
        json.dump(producer_data, f, indent=2)
    
    # Sample Director output
    director_data = {
        "timestamp": datetime.now().isoformat(),
        "genre": "storytelling",
        "tone": "dramatic",
        "pacing": "medium",
        "story_arc": {
            "act1": "setup",
            "act2": "conflict", 
            "act3": "climax",
            "act4": "resolution"
        },
        "emotional_beats": {
            "beat_01": "introduction",
            "beat_02": "rising_tension",
            "beat_03": "climax",
            "beat_04": "resolution"
        }
    }
    
    with open(output_dir / "director_output.json", 'w') as f:
        json.dump(director_data, f, indent=2)
    
    # Sample Prompt Engineer output
    prompt_engineer_data = {
        "timestamp": datetime.now().isoformat(),
        "beat_contexts": {
            "beat_01": {
                "image_prompt": "A vast medieval castle on a hilltop, dramatic lighting",
                "video_prompt": "Slow aerial approach to the imposing castle, morning mist",
                "scene_type": "establishing"
            },
            "beat_02": {
                "image_prompt": "Two characters in heated argument, medieval chamber",
                "video_prompt": "Quick cuts between characters arguing, intense facial expressions",
                "scene_type": "dialogue"
            },
            "beat_03": {
                "image_prompt": "Epic battle scene, swords clashing, fire in background",
                "video_prompt": "Fast-paced action, warriors fighting, dramatic camera movements",
                "scene_type": "action"
            },
            "beat_04": {
                "image_prompt": "Peaceful sunset over the kingdom, characters embracing",
                "video_prompt": "Slow motion embrace, warm golden hour lighting, gentle camera movement",
                "scene_type": "resolution"
            }
        }
    }
    
    with open(output_dir / "prompt_engineer_output.json", 'w') as f:
        json.dump(prompt_engineer_data, f, indent=2)
    
    logger.info(f"Created sample agent files in: {output_dir}")
    return (
        str(output_dir / "producer_output.json"),
        str(output_dir / "director_output.json"), 
        str(output_dir / "prompt_engineer_output.json")
    )


def run_full_pipeline(producer_file: str, director_file: str, prompt_engineer_file: str, 
                     output_video: str, intermediate_json: str = None):
    """Run the complete editing pipeline"""
    
    logger.info("🚀 Starting Full VinVideo Editing Pipeline")
    
    # Step 1: Load agent outputs
    logger.info("📥 Loading agent outputs...")
    producer_output, director_output, prompt_engineer_output = load_agent_outputs_from_files(
        producer_file, director_file, prompt_engineer_file
    )
    
    # Step 2: Generate editing plan with Editing Agent
    logger.info("🤖 Generating editing plan with Editing Agent...")
    editing_agent = EditingAgent()
    editing_plan = editing_agent.process_agent_outputs(
        producer_output, director_output, prompt_engineer_output
    )
    
    # Save intermediate JSON if requested
    if intermediate_json:
        with open(intermediate_json, 'w') as f:
            json.dump(editing_plan, f, indent=2)
        logger.info(f"💾 Saved editing plan to: {intermediate_json}")
    
    # Step 3: Convert to video using Movis
    logger.info("🎬 Converting to video with Movis...")
    
    # Write temporary JSON file if no intermediate requested
    if not intermediate_json:
        intermediate_json = "temp_editing_plan.json"
        with open(intermediate_json, 'w') as f:
            json.dump(editing_plan, f, indent=2)
        temp_file = True
    else:
        temp_file = False
    
    # Convert to video
    converter = EditingAgentConverter()
    result = converter.convert_and_render(
        intermediate_json, output_video, validate_assets=False
    )
    
    # Clean up temp file
    if temp_file:
        os.remove(intermediate_json)
    
    # Step 4: Report results
    logger.info("✅ Pipeline Complete!")
    
    return {
        "editing_plan": editing_plan,
        "video_result": result,
        "pipeline_summary": {
            "input_files": [producer_file, director_file, prompt_engineer_file],
            "output_video": output_video,
            "intermediate_json": intermediate_json if not temp_file else None,
            "total_beats": len(editing_plan.get("layers", [])),
            "video_duration": result["duration"],
            "editing_style": editing_plan.get("metadata", {}).get("editing_style"),
            "platform": result["platform"]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Full VinVideo Editing Pipeline - From Agent Outputs to Final Video',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use mock data (for testing)
  python3 full_editing_pipeline.py --mock --output final_video.mp4

  # Use real agent output files
  python3 full_editing_pipeline.py --producer producer.json --director director.json --prompt-engineer pe.json --output video.mp4

  # Save intermediate editing plan
  python3 full_editing_pipeline.py --mock --output video.mp4 --save-json editing_plan.json

  # Create sample agent files
  python3 full_editing_pipeline.py --create-samples ./agent_outputs/
        """
    )
    
    # Input options
    parser.add_argument('--producer', type=str, help='Producer agent output JSON file')
    parser.add_argument('--director', type=str, help='Director agent output JSON file')
    parser.add_argument('--prompt-engineer', type=str, help='Prompt Engineer agent output JSON file')
    
    # Alternative: mock data
    parser.add_argument('--mock', action='store_true', help='Use mock agent data for testing')
    
    # Sample creation
    parser.add_argument('--create-samples', type=str, metavar='DIR', 
                        help='Create sample agent output files in specified directory')
    
    # Output options
    parser.add_argument('--output', '-o', type=str, default='final_video.mp4', 
                        help='Output video file path')
    parser.add_argument('--save-json', type=str, metavar='FILE',
                        help='Save intermediate editing plan JSON to file')
    
    # Options
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Handle sample creation
    if args.create_samples:
        create_sample_agent_files(args.create_samples)
        print(f"✅ Created sample agent files in: {args.create_samples}")
        return 0
    
    try:
        # Determine input source
        if args.mock:
            logger.info("Using mock agent data")
            # Create temporary sample files
            producer_file, director_file, pe_file = create_sample_agent_files("temp_samples")
            cleanup_samples = True
        elif args.producer and args.director and args.prompt_engineer:
            producer_file = args.producer
            director_file = args.director
            pe_file = args.prompt_engineer
            cleanup_samples = False
            
            # Validate files exist
            for file_path in [producer_file, director_file, pe_file]:
                if not os.path.exists(file_path):
                    print(f"❌ Error: File not found: {file_path}")
                    return 1
        else:
            print("❌ Error: Must specify either --mock or all three agent files")
            print("Use --help for usage information")
            return 1
        
        # Run the pipeline
        result = run_full_pipeline(
            producer_file, director_file, pe_file,
            args.output, args.save_json
        )
        
        # Clean up temporary files
        if cleanup_samples:
            for file_path in [producer_file, director_file, pe_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)
            temp_dir = Path("temp_samples")
            if temp_dir.exists():
                temp_dir.rmdir()
        
        # Print summary
        summary = result["pipeline_summary"]
        print(f"\n🎉 VinVideo Pipeline Complete!")
        print(f"   📁 Output Video: {summary['output_video']}")
        print(f"   ⏱️  Duration: {summary['video_duration']:.1f}s")
        print(f"   🎬 Beats Processed: {summary['total_beats']}")
        print(f"   🎨 Editing Style: {summary['editing_style']}")
        print(f"   📱 Platform: {summary['platform']}")
        
        if summary['intermediate_json']:
            print(f"   📄 Editing Plan: {summary['intermediate_json']}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())