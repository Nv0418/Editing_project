#!/usr/bin/env python3
"""Test a single style to debug"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from test_got_styles_simple import create_got_video_with_style
from pathlib import Path

# Test just SGONE style
output_dir = Path("output_test/single_style_test")
output_dir.mkdir(parents=True, exist_ok=True)

print("Testing SGONE CAPTION style...")
success = create_got_video_with_style("sgone_caption", output_dir)

if success:
    print("\n✅ Test successful!")
else:
    print("\n❌ Test failed!")