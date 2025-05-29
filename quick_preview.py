#!/usr/bin/env python3
"""
Quick Preview Generator
Simple script for testing different text with subtitle styles
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def main():
    print("🎬 VinVideo Style Preview Generator")
    print("=" * 40)
    
    # Get text input
    text = input("Enter text to preview (or press Enter for 'SAMPLE TEXT'): ").strip()
    if not text:
        text = "SAMPLE TEXT"
    
    print(f"\n📝 Generating previews for: '{text}'")
    print("⏳ Please wait...")
    
    # Run the preview generator
    try:
        result = subprocess.run([
            "python3", "style_preview_generator.py", 
            "--text", text
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Previews generated successfully!")
            print("\n" + result.stdout)
            
            # Ask if user wants to open the preview page
            open_page = input("📱 Open preview page in browser? (y/N): ").strip().lower()
            if open_page in ['y', 'yes']:
                html_path = Path(__file__).parent / "accurate_style_preview.html"
                webbrowser.open(f"file://{html_path.absolute()}")
                print("🌐 Preview page opened in browser")
        else:
            print("❌ Error generating previews:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n📋 Commands you can use:")
    print("  • python3 style_preview_generator.py --text 'YOUR TEXT'")
    print("  • python3 style_preview_generator.py --style simple_caption --text 'TEST'") 
    print("  • Open accurate_style_preview.html in browser to view results")

if __name__ == "__main__":
    main()