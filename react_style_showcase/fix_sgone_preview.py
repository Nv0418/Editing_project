#!/usr/bin/env python3
"""Fix sgone_caption preview by extracting from center area"""

import subprocess
from pathlib import Path

# Sgone caption displays in center, not bottom
video_path = '/Users/naman/Desktop/movie_py/output_test/json_test/json_styled_sgone_caption.mp4'
output_path = Path(__file__).parent / "subtitle_preview_app" / "public" / "style_previews" / "sgone_caption.png"

# Extract frame and crop center area (not bottom)
cmd = [
    'ffmpeg',
    '-ss', '3.0',  # Try 3 seconds in
    '-i', str(video_path),
    '-vframes', '1',
    '-vf', 'crop=in_w:in_h*0.4:0:in_h*0.3,scale=320:180',  # Crop middle 40%
    '-q:v', '2',
    '-y',
    str(output_path)
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"✓ Fixed sgone_caption preview: {output_path}")
else:
    print(f"Error: {result.stderr}")