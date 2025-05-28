#!/usr/bin/env python3
"""
Dynamic Karaoke System - Configurable Input and Style System
Supports multiple animation styles defined in subtitles_style.json
"""

import movis as mv
from movis.layer.drawing import Text
from movis.enum import TextAlignment
import random
from pathlib import Path
import json
import argparse
import sys
import os # Added for os.path.join, though Path.glob is better

def load_karaoke_styles(styles_file):
    """Load karaoke styles from configuration file"""
    try:
        with open(styles_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Styles file not found: {styles_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in styles file: {e}")
        return None

def load_parakeet_data(json_path):
    """Load parakeet transcription data"""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        words = []
        for item in data["word_timestamps"]:
            words.append({
                "word": item["word"],
                "start": item["start"],
                "end": item["end"]
            })
        return data["transcript"], words
    except FileNotFoundError:
        print(f"ERROR: Transcription file not found: {json_path}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in transcription file: {e}")
        return None, None

def create_dynamic_karaoke(transcription_path, audio_path, style_name="Basic_karaoke_animation_draft_1", image_dir=None):
    """Create karaoke video with dynamic inputs and configurable style"""
    
    # Load styles configuration
    styles_file = Path(__file__).resolve().parent.parent / "subtitles_style.json"
    styles = load_karaoke_styles(styles_file)
    
    if not styles:
        return None
        
    if style_name not in styles:
        print(f"ERROR: Style '{style_name}' not found in styles configuration")
        print(f"Available styles: {list(styles.keys())}")
        return None
    
    style_config = styles[style_name]
    print(f"Using style: {style_config['name']}")
    print(f"Description: {style_config['description']}")
    # Seed randomness for deterministic highlight selection
    random.seed(42)
    
    # Verify input files exist
    transcription_file = Path(transcription_path)
    audio_file = Path(audio_path)
    
    if not transcription_file.exists():
        print(f"ERROR: Transcription file not found: {transcription_file}")
        return None
        
    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_file}")
        return None
    
    # Load transcription data
    print("Loading transcription and audio data...")
    transcript, words = load_parakeet_data(transcription_file)
    
    if not words:
        return None
        
    audio_layer = mv.layer.Audio(str(audio_file))
    composition_duration = audio_layer.duration
    
    print(f"Audio duration: {composition_duration:.2f}s")
    print(f"Total words: {len(words)}")
    
    # Extract style configuration
    resolution = style_config["format"]["resolution"]
    layout = style_config["layout"]
    typography = style_config["typography"]
    
    print(f"Resolution: {resolution[0]}x{resolution[1]} ({style_config['format']['aspect_ratio']})")
    
    # Create composition with style-based resolution
    scene = mv.layer.Composition(size=tuple(resolution), duration=composition_duration)

    # Add image sequence background if image_dir is provided
    if image_dir:
        image_dir_path = Path(image_dir)
        if image_dir_path.is_dir():
            image_files = sorted([f for f in image_dir_path.iterdir() if f.is_file() and f.suffix.lower() in ['.png', '.jpg', '.jpeg']])
            if image_files:
                num_images = len(image_files)
                image_duration = composition_duration / num_images
                current_offset = 0.0
                comp_width, comp_height = resolution
                for idx, img_path in enumerate(image_files):
                    # Create a temporary image layer to get its original dimensions
                    # This assumes mv.layer.Image().size gives original dimensions
                    # If not, we might need to use cv2.imread(str(img_path)).shape to get dims
                    try:
                        temp_img_for_dims = mv.layer.Image(str(img_path))
                        img_original_width, img_original_height = temp_img_for_dims.size
                    except Exception as e:
                        print(f"Warning: Could not get original dimensions for {img_path} using movis: {e}. Skipping this image.")
                        # As a fallback, could try OpenCV if movis fails, e.g.:
                        # import cv2
                        # _img = cv2.imread(str(img_path))
                        # if _img is not None:
                        #     img_original_height, img_original_width = _img.shape[:2]
                        # else: continue # skip if cv2 also fails
                        continue


                    # Calculate scale factor for 'cover' behavior
                    scale_w = comp_width / img_original_width
                    scale_h = comp_height / img_original_height
                    scale_to_use = max(scale_w, scale_h)

                    # Create the actual image layer for the scene
                    img_layer = mv.layer.Image(str(img_path), duration=image_duration)
                    img_layer.scale = (scale_to_use, scale_to_use)
                    img_layer.position = (comp_width / 2, comp_height / 2)  # Center the image

                    scene.add_layer(img_layer, name=f"bg_image_{idx}", offset=current_offset)
                    current_offset += image_duration
                print(f"Added {num_images} images as background from {image_dir}")
            else:
                print(f"No images found in {image_dir}. Proceeding without image background.")
        else:
            print(f"Image directory {image_dir} not found. Proceeding without image background.")

    # Add audio layer
    scene.add_layer(audio_layer, name="audio")

    # Handle multi-mode layout (e.g., Cinematic Dual Style)
    if layout.get("text_positioning") == "multi_mode":
        modes = layout.get("modes", {})
        reg_layout = modes.get("regular", {})
        hig_layout = modes.get("highlight", {})
        reg_typo = style_config.get("typography", {}).get("regular", {})
        hig_typo = style_config.get("typography", {}).get("highlight", {})
        # keywords to trigger highlight mode (optional)
        keywords = set(layout.get("highlight_keywords", []))
        # ratio for random highlighting (approx fraction of windows to stylize)
        ratio = layout.get("highlight_ratio", None)
        # determine window size (use regular mode batch)
        batch = reg_layout.get("words_per_window", 2)
        # process windows sequentially
        for wi, start_idx in enumerate(range(0, len(words), batch)):
            window_words = words[start_idx:start_idx + batch]
            if not window_words:
                continue
            # timing
            t0 = window_words[0]["start"]
            t1 = window_words[-1]["end"]
            dur = t1 - t0
            # choose mode: highlight if keyword present, else based on ratio or fallback alternate
            if keywords and any(w["word"].lower() in keywords for w in window_words):
                is_high = True
            elif ratio is not None:
                is_high = random.random() < ratio
            else:
                # fallback: alternate windows
                is_high = (wi % 2 == 1)
            # collect phrase
            phrase = " ".join(w["word"] for w in window_words)
            if is_high:
                # highlight style: center phrase
                font = hig_typo.get("font_family")
                size = hig_typo.get("font_size")
                color = tuple(hig_typo.get("colors", {}).get("normal", [255, 255, 255]))
                ypos = hig_layout.get("vertical_position", resolution[1] // 2)
            else:
                # regular style: lower third
                font = reg_typo.get("font_family")
                size = reg_typo.get("font_size")
                color = tuple(reg_typo.get("colors", {}).get("normal", [255, 255, 255]))
                ypos = reg_layout.get("vertical_position", resolution[1] - 200)
            # create text layer
            txt = Text(
                text=phrase,
                font_size=size,
                font_family=font,
                color=color,
                text_alignment=TextAlignment.CENTER,
                duration=dur
            )
            # center X
            xpos = resolution[0] // 2
            scene.add_layer(txt, name=f"phrase_{wi}", position=(xpos, ypos), offset=t0)
        print(f"Created {len(scene.layers)-1} phrase layers (multi-mode)")
        return scene
    
    # Default single-mode layout (e.g., lower_third styles)
    # Add background if solid_color, AND if image_dir was not provided or had no images
    if not image_dir or not scene.get_layer(f"bg_image_0"): # Check if image background was added
        bg_config = style_config.get("background", {})
        if bg_config.get("type") == "solid_color":
            background = mv.layer.Rectangle(
                size=tuple(resolution),
                color=tuple(bg_config.get("color", [0, 0, 0])),
                duration=composition_duration
            )
            scene.add_layer(background, name="background")
    # Get positioning from style config
    vertical_pos = layout.get("vertical_position", resolution[1] - 200)
    horizontal_positions = layout.get("horizontal_positions", {})
    POSITIONS = [horizontal_positions.get(k) for k in ("left", "center", "right")]
    # words per window
    words_per_window = layout.get("words_per_window", 3)
    for window_start in range(0, len(words), words_per_window):
        window_words = words[window_start:window_start + words_per_window]
        if not window_words:
            continue
        t0 = window_words[0]["start"]
        t1 = window_words[-1]["end"]
        for i, wdata in enumerate(window_words):
            if i >= len(POSITIONS):
                break
            word = wdata["word"]
            ws = wdata["start"]
            we = wdata["end"]
            word_layer = DynamicWordLayer(
                word=word,
                word_start=ws,
                word_end=we,
                window_start=t0,
                window_end=t1,
                style_config=typography
            )
            xpos = POSITIONS[i] or (resolution[0] // 2)
            scene.add_layer(word_layer, name=f"word_{window_start}_{i}", position=(xpos, vertical_pos))
    print(f"Created {len(scene.layers)-1} word layers (single-mode)")
    return scene

class DynamicWordLayer:
    """Dynamic word layer that uses style configuration"""
    
    def __init__(self, word, word_start, word_end, window_start, window_end, style_config):
        self.word = word
        self.word_start = word_start
        self.word_end = word_end
        self.window_start = window_start
        self.window_end = window_end
        self.style_config = style_config
        self.duration = 30.0
        
        # Extract style properties
        font_family = style_config["font_family"]
        font_size = style_config["font_size"]
        font_size_highlighted = style_config["font_size_highlighted"]
        colors = style_config["colors"]
        alignment = getattr(TextAlignment, style_config["text_alignment"].upper())
        
        # Normal text
        self.normal_text = Text(
            text=word, font_size=font_size, font_family=font_family,
            color=tuple(colors["normal"]), text_alignment=alignment,
            duration=30.0
        )
        
        # Highlighted text
        self.highlighted_text = Text(
            text=word, font_size=font_size_highlighted, font_family=font_family,
            color=tuple(colors["highlighted"]), text_alignment=alignment,
            duration=30.0
        )
    
    def __call__(self, time):
        # Only visible during window
        if time < self.window_start or time > self.window_end:
            return None
        
        # Show highlighted version during word timing
        if self.word_start <= time <= self.word_end:
            return self.highlighted_text(time)
        else:
            return self.normal_text(time)
    
    def get_key(self, time):
        if time < self.window_start or time > self.window_end:
            return None
        is_highlighted = self.word_start <= time <= self.word_end
        return (self.word, is_highlighted, round(time, 2))

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='Dynamic Karaoke Video Generator')
    parser.add_argument('transcription_path', help='Path to transcription JSON file')
    parser.add_argument('audio_path', help='Path to audio file')
    parser.add_argument('--style', default='Basic_karaoke_animation_draft_1', 
                       help='Style name from subtitles_style.json')
    parser.add_argument('--image_dir', help='Path to directory containing background images (optional)')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    print("🎬 DYNAMIC KARAOKE GENERATOR")
    print("=" * 50)
    print(f"Transcription: {args.transcription_path}")
    print(f"Audio: {args.audio_path}")
    print(f"Style: {args.style}")
    if args.image_dir:
        print(f"Image Directory: {args.image_dir}")
    print("=" * 50)
    
    # Create karaoke scene
    scene = create_dynamic_karaoke(args.transcription_path, args.audio_path, args.style, args.image_dir)
    
    if scene is None:
        print("Failed to create karaoke scene!")
        sys.exit(1)
    
    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_dir = Path(__file__).resolve().parent.parent / "output_test"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"dynamic_karaoke_{args.style}.mp4"
    
    print(f"\n🎥 Rendering karaoke to: {output_file}")
    
    try:
        scene.write_video(str(output_file))
        print("🎉 SUCCESS! Dynamic karaoke created!")
        print(f"📊 Duration: {scene.duration:.2f}s")
        print(f"📊 Total layers: {len(scene.layers)}")
        print(f"📁 File: {output_file}")
        
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
