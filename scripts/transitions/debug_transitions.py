#!/usr/bin/env python3
"""
Debugging script for custom transitions
"""

import os
import sys
from pathlib import Path

# Add the modified movis to path
sys.path.insert(0, '/Users/naman/Desktop/movie_py/movis')

# Check if movis import works
try:
    import movis as mv
    print("✅ Successfully imported Movis")
except ImportError as e:
    print(f"❌ Failed to import Movis: {e}")
    sys.exit(1)

# Check if transition registry import works
try:
    sys.path.insert(0, '/Users/naman/Desktop/movie_py')
    from scripts.transitions.registry import TransitionRegistry
    print("✅ Successfully imported TransitionRegistry")
    
    # Initialize registry and check transitions
    registry = TransitionRegistry()
    transitions = registry.list_transitions()
    print(f"📋 Available transitions: {transitions}")
    
    # Check if specific transitions exist
    for t_id in ["distortion/transition_01", "distortion/transition_02", "distortion/transition_03"]:
        transition = registry.get_transition(t_id)
        if transition:
            print(f"✅ Found transition: {t_id}")
            print(f"   Path: {transition['path']}")
            print(f"   Assets: {transition.get('assets', {})}")
        else:
            print(f"❌ Transition not found: {t_id}")
    
except ImportError as e:
    print(f"❌ Failed to import TransitionRegistry: {e}")
    sys.exit(1)

# Check media files
media_dir = Path("/Users/naman/Desktop/movie_py/media")
print(f"\n📁 Checking media directory: {media_dir}")
if media_dir.exists():
    videos = list(media_dir.glob("*.mp4"))
    audios = list(media_dir.glob("*.mp3"))
    print(f"✅ Found {len(videos)} videos and {len(audios)} audio files")
    
    for i, video in enumerate(videos[:3]):
        print(f"   Video {i+1}: {video.name}")
    for i, audio in enumerate(audios):
        print(f"   Audio {i+1}: {audio.name}")
else:
    print(f"❌ Media directory not found: {media_dir}")

print("\n✅ Debug script completed successfully")
