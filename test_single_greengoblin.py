#!/usr/bin/env python3
"""Test just GREENGOBLIN style"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_got_styles_black_bg import create_style_video_simple
from pathlib import Path

# Test GREENGOBLIN style
output_dir = Path("output_test/greengoblin_test")
output_dir.mkdir(parents=True, exist_ok=True)

print("Testing GREENGOBLIN style...")
success = create_style_video_simple("greengoblin", output_dir)

if success:
    print("\n✅ GREENGOBLIN test successful!")
else:
    print("\n❌ GREENGOBLIN test failed!")