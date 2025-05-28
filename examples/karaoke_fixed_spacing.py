#!/usr/bin/env python3
"""
Fixed Karaoke - Proper word spacing with correct color changes
"""

import movis as mv
from movis.layer.drawing import Text
from movis.enum import TextAlignment
from pathlib import Path

def measure_text_width(text, font_size=60):
    """Measure text width for positioning"""
    temp = Text(text=text, font_size=font_size, font_family="Arial", color=(255,255,255), duration=0.1)
    width, height = temp.get_size(0.0)
    return width

def create_word_positions_fixed(words, font_size=60):
    """Calculate exact positions with proper spacing"""
    positions = []
    
    # Create the full text to get total width for centering
    full_text = " ".join(words)
    total_width = measure_text_width(full_text, font_size)
    
    # Start from the left edge (will be centered later)
    start_x = -total_width / 2
    current_x = start_x
    
    for i, word in enumerate(words):
        word_width = measure_text_width(word, font_size)
        
        positions.append({
            'word': word,
            'x_offset': current_x,
            'width': word_width
        })
        
        # Move to next position: current word width + space
        current_x += word_width
        if i < len(words) - 1:  # Add space except for last word
            space_width = measure_text_width(" ", font_size)
            current_x += space_width
    
    return positions

def create_spaced_karaoke_test():
    """Create karaoke with proper word spacing"""
    
    test_words = [
        {"word": "hey", "start": 1.0, "end": 1.5},
        {"word": "hello", "start": 1.6, "end": 2.1},
        {"word": "how", "start": 2.2, "end": 2.7},
        {"word": "are", "start": 2.8, "end": 3.1},
        {"word": "you", "start": 3.2, "end": 3.5},
        {"word": "doing", "start": 3.6, "end": 4.1},
        {"word": "today", "start": 4.2, "end": 4.7},
        {"word": "my", "start": 4.8, "end": 5.0},
        {"word": "friend", "start": 5.1, "end": 5.6},
    ]
    
    scene = mv.layer.Composition(size=(1280, 720), duration=7.0)
    scene.add_layer(mv.layer.Rectangle(size=(1280, 720), color=(0, 0, 0), duration=7.0), name="bg")
    
    center_x, center_y = 640, 360
    
    # Create each 3-word window with proper spacing
    for window_start in range(0, len(test_words), 3):
        if window_start + 3 <= len(test_words):
            window_words = test_words[window_start:window_start + 3]
            word_texts = [w["word"] for w in window_words]
            
            # Calculate proper positions
            word_positions = create_word_positions_fixed(word_texts)
            
            # Window timing
            window_start_time = window_words[0]["start"]
            window_end_time = window_words[-1]["end"]
            
            print(f"Window {window_start//3 + 1}: {' '.join(word_texts)}")
            
            # Create positioned word layers
            for i, (word_data, pos_data) in enumerate(zip(window_words, word_positions)):
                word = word_data["word"]
                word_start = word_data["start"]
                word_end = word_data["end"]
                
                # Calculate absolute position with proper spacing
                word_x = center_x + pos_data["x_offset"]
                
                print(f"  {word}: position {word_x} (offset {pos_data['x_offset']})")
                
                # Create word layer that changes color in-place
                word_layer = SpacedWordLayer(
                    word=word,
                    word_start=word_start,
                    word_end=word_end,
                    window_start=window_start_time,
                    window_end=window_end_time,
                    font_size=60
                )
                
                scene.add_layer(
                    word_layer,
                    name=f"word_{window_start}_{i}_{word}",
                    position=(word_x, center_y)
                )
    
    return scene

class SpacedWordLayer:
    """Word layer with proper spacing and color animation"""
    
    def __init__(self, word, word_start, word_end, window_start, window_end, font_size=60):
        self.word = word
        self.word_start = word_start
        self.word_end = word_end
        self.window_start = window_start
        self.window_end = window_end
        self.font_size = font_size
        self.duration = 10.0
        
        # White version
        self.white_text = Text(
            text=word, font_size=font_size, font_family="Arial",
            color=(255, 255, 255), text_alignment=TextAlignment.LEFT, duration=10.0
        )
        
        # Yellow + bold version
        self.yellow_text = Text(
            text=word, font_size=font_size + 4, font_family="Arial",
            color=(255, 255, 0), text_alignment=TextAlignment.LEFT, duration=10.0
        )
    
    def __call__(self, time):
        # Only visible during window
        if time < self.window_start or time > self.window_end:
            return None
        
        # Yellow during speech, white otherwise
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
    print("Creating karaoke with FIXED SPACING and correct color changes...")
    print("Expected result:")
    print("- 'hey hello how' (with proper spaces)")
    print("- 'are you doing' (with proper spaces)")  
    print("- 'today my friend' (with proper spaces)")
    print("- Words change color in-place (no overlays)")
    
    scene = create_spaced_karaoke_test()
    
    output_dir = Path(__file__).resolve().parent.parent / "output_test"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "karaoke_fixed_spacing.mp4"
    
    print(f"\nRendering with fixed spacing to: {output_file}")
    try:
        scene.write_video(str(output_file))
        print("SUCCESS! Fixed spacing karaoke created!")
        print(f"Layers: {len(scene.layers)}")
        print("\nShould now show:")
        print("✅ Proper word spacing: 'hey hello how'")
        print("✅ Color changes in-place")
        print("✅ No overlapping text")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
