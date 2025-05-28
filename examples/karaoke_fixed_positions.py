#!/usr/bin/env python3
"""
Fixed-Position Karaoke - Each word assigned to specific screen position
LEFT - CENTER - RIGHT positions with wide spacing
"""

import movis as mv
from movis.layer.drawing import Text
from movis.enum import TextAlignment
from pathlib import Path
import json

def load_parakeet_data(json_path):
    """Load real parakeet transcription data"""
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

def create_fixed_position_karaoke():
    """Create karaoke with fixed positions: LEFT - CENTER - RIGHT"""
    
    project_root = Path(__file__).resolve().parent.parent
    audio_file = project_root / "got_script.mp3"
    transcription_file = project_root / "parakeet_output.json"
    
    # Verify files exist
    if not audio_file.exists():
        print(f"ERROR: Audio file not found: {audio_file}")
        return None
        
    if not transcription_file.exists():
        print(f"ERROR: Transcription file not found: {transcription_file}")
        return None
    
    # Load real data
    print("Loading real audio and transcription data...")
    transcript, words = load_parakeet_data(transcription_file)
    audio_layer = mv.layer.Audio(str(audio_file))
    composition_duration = audio_layer.duration
    
    print(f"Audio duration: {composition_duration:.2f}s")
    print(f"Total words: {len(words)}")
    
    # Create composition
    scene = mv.layer.Composition(size=(1280, 720), duration=composition_duration)
    
    # Black background
    background = mv.layer.Rectangle(
        size=(1280, 720), color=(0, 0, 0), duration=composition_duration
    )
    scene.add_layer(background, name="background")
    
    # Add audio
    scene.add_layer(audio_layer, name="audio")
    
    # FIXED POSITIONS - Wide spacing for long words
    center_y = 360
    LEFT_X = 320    # Left position (25% from left edge)
    CENTER_X = 640  # Center position (50% - screen center)  
    RIGHT_X = 960   # Right position (75% from left edge)
    
    POSITIONS = [LEFT_X, CENTER_X, RIGHT_X]
    POSITION_NAMES = ["LEFT", "CENTER", "RIGHT"]
    
    print(f"\nFixed positions: LEFT={LEFT_X}, CENTER={CENTER_X}, RIGHT={RIGHT_X}")
    print("Creating non-overlapping 3-word windows with fixed positions...")
    
    # Create non-overlapping 3-word windows
    for window_start in range(0, len(words), 3):  # Jump by 3, no overlap
        if window_start + 3 <= len(words):
            window_words = words[window_start:window_start + 3]
            
            # Window timing
            window_start_time = window_words[0]["start"]
            window_end_time = window_words[-1]["end"]
            
            window_text = " | ".join([w["word"] for w in window_words])
            print(f"Window {window_start//3 + 1}: {window_text} ({window_start_time:.1f}s-{window_end_time:.1f}s)")
            
            # Create word layers for each position
            for i, word_data in enumerate(window_words):
                word = word_data["word"]
                word_start = word_data["start"]
                word_end = word_data["end"]
                
                # Assign fixed position
                word_x = POSITIONS[i]  # i=0→LEFT, i=1→CENTER, i=2→RIGHT
                position_name = POSITION_NAMES[i]
                
                print(f"  '{word}' → {position_name} (x={word_x})")
                
                # Create fixed position word layer
                word_layer = FixedPositionWordLayer(
                    word=word,
                    word_start=word_start,
                    word_end=word_end,
                    window_start=window_start_time,
                    window_end=window_end_time,
                    font_size=80  # Larger font for better visibility
                )
                
                scene.add_layer(
                    word_layer,
                    name=f"word_{window_start}_{i}_{word}_{position_name}",
                    position=(word_x, center_y)
                )
    
    print(f"Created {len(scene.layers)} total layers")
    return scene

class FixedPositionWordLayer:
    """Word layer with fixed position and color animation"""
    
    def __init__(self, word, word_start, word_end, window_start, window_end, font_size=80):
        self.word = word
        self.word_start = word_start
        self.word_end = word_end
        self.window_start = window_start
        self.window_end = window_end
        self.font_size = font_size
        self.duration = 30.0
        
        # White version (normal) - CENTER aligned for consistent positioning
        self.white_text = Text(
            text=word, font_size=font_size, font_family="Arial",
            color=(255, 255, 255), text_alignment=TextAlignment.CENTER, 
            duration=30.0
        )
        
        # Yellow version (highlighted + bigger) - CENTER aligned
        self.yellow_text = Text(
            text=word, font_size=font_size + 10, font_family="Arial",
            color=(255, 255, 0), text_alignment=TextAlignment.CENTER, 
            duration=30.0
        )
    
    def __call__(self, time):
        # Only visible during window
        if time < self.window_start or time > self.window_end:
            return None
        
        # Yellow + bold during speech, white otherwise
        if self.word_start <= time <= self.word_end:
            return self.yellow_text(time)
        else:
            return self.white_text(time)
    
    def get_key(self, time):
        if time < self.window_start or time > self.window_end:
            return None
        is_highlighted = self.word_start <= time <= self.word_end
        return (self.word, is_highlighted, round(time, 2))

def main():
    """Create fixed-position karaoke video"""
    print("🎬 Creating FIXED-POSITION KARAOKE!")
    print("=" * 60)
    print("New approach:")
    print("- Each word assigned to FIXED position on screen")
    print("- Position 1 (LEFT): x=320")
    print("- Position 2 (CENTER): x=640") 
    print("- Position 3 (RIGHT): x=960")
    print("- Wide spacing to accommodate long words")
    print("- Words change color in their assigned position")
    print("=" * 60)
    
    scene = create_fixed_position_karaoke()
    
    if scene is None:
        print("Failed to create scene - check file paths!")
        return
    
    # Output file
    output_dir = Path(__file__).resolve().parent.parent / "output_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "karaoke_fixed_positions.mp4"
    
    print(f"\n🎥 Rendering fixed-position karaoke to: {output_file}")
    
    try:
        scene.write_video(str(output_file))
        print("🎉 SUCCESS! Fixed-position karaoke created!")
        print(f"📊 Duration: {scene.duration:.2f}s")
        print(f"📊 Total layers: {len(scene.layers)}")
        print(f"📁 File: {output_file}")
        print("\n✅ New approach implemented:")
        print("✅ Fixed LEFT-CENTER-RIGHT positions")
        print("✅ Wide spacing for any word length")
        print("✅ Words change color in their assigned spots")
        print("✅ No complex positioning calculations")
        
    except Exception as e:
        print(f"❌ Error rendering video: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
