#!/usr/bin/env python3
"""
Setup script for VinVideo AI-powered video creation platform
Optimized for Codex OpenAI platform deployment
"""

import os
import sys
from pathlib import Path

def install_requirements():
    """Install Python requirements"""
    os.system("pip install -r requirements.txt")

def setup_fonts():
    """Ensure font directories exist"""
    font_dirs = [
        "project_fonts",
        "subtitle_styles/fonts",
        "react_style_showcase/subtitle_preview_app/fonts",
        "react_style_showcase/subtitle_preview_app/public/fonts"
    ]
    
    for font_dir in font_dirs:
        Path(font_dir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Font directory: {font_dir}")

def setup_output_dirs():
    """Create necessary output directories"""
    output_dirs = [
        "output_test",
        "output_test/test_result_single",
        "temp_samples"
    ]
    
    for output_dir in output_dirs:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory: {output_dir}")

def setup_react_app():
    """Setup React preview application"""
    react_dir = Path("react_style_showcase/subtitle_preview_app")
    if react_dir.exists():
        os.chdir(react_dir)
        print("Installing React dependencies...")
        os.system("npm install")
        os.chdir("../..")
        print("✓ React app setup complete")

def main():
    """Main setup function"""
    print("🚀 Setting up VinVideo for Codex OpenAI Platform")
    print("=" * 50)
    
    # Install Python dependencies
    print("\n📦 Installing Python dependencies...")
    install_requirements()
    
    # Setup directories
    print("\n📁 Setting up directories...")
    setup_fonts()
    setup_output_dirs()
    
    # Setup React app (if Node.js is available)
    try:
        setup_react_app()
    except Exception as e:
        print(f"⚠️  React setup skipped: {e}")
    
    print("\n✅ VinVideo setup complete!")
    print("\nNext steps:")
    print("1. Add your audio files to other_root_files/")
    print("2. Run: python3 Finalized_styles/test_v3_styles.py")
    print("3. For React preview: cd react_style_showcase/subtitle_preview_app && npm start")

if __name__ == "__main__":
    main()