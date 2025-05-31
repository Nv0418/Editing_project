#!/usr/bin/env python3
"""
Crop style preview images to focus on the text area.
Creates cropped versions that show just the caption text.
"""

import os
from PIL import Image
import numpy as np

def find_text_bounds(image_path):
    """Find the bounding box of non-black pixels (text area)."""
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)
    
    # Find non-black pixels (threshold for near-black)
    threshold = 30
    non_black = np.any(img_array > threshold, axis=2)
    
    # Find rows and columns with content
    rows_with_content = np.any(non_black, axis=1)
    cols_with_content = np.any(non_black, axis=0)
    
    if not np.any(rows_with_content) or not np.any(cols_with_content):
        # If no content found, return center crop
        height, width = img_array.shape[:2]
        return (width//4, height//3, 3*width//4, 2*height//3)
    
    # Find bounds
    top = np.argmax(rows_with_content)
    bottom = len(rows_with_content) - np.argmax(rows_with_content[::-1])
    left = np.argmax(cols_with_content)
    right = len(cols_with_content) - np.argmax(cols_with_content[::-1])
    
    # Add padding
    padding = 40
    top = max(0, top - padding)
    bottom = min(img_array.shape[0], bottom + padding)
    left = max(0, left - padding)
    right = min(img_array.shape[1], right + padding)
    
    return (left, top, right, bottom)

def crop_to_fixed_ratio(img, bounds, target_ratio=16/9):
    """Crop to a fixed aspect ratio centered on the text bounds."""
    left, top, right, bottom = bounds
    text_width = right - left
    text_height = bottom - top
    text_center_x = (left + right) // 2
    text_center_y = (top + bottom) // 2
    
    # Calculate dimensions to maintain aspect ratio
    if text_width / text_height > target_ratio:
        # Text is wider than target ratio
        new_width = text_width
        new_height = int(text_width / target_ratio)
    else:
        # Text is taller than target ratio
        new_height = text_height
        new_width = int(text_height * target_ratio)
    
    # Ensure we don't exceed image bounds
    img_width, img_height = img.size
    if new_width > img_width:
        new_width = img_width
        new_height = int(new_width / target_ratio)
    if new_height > img_height:
        new_height = img_height
        new_width = int(new_height * target_ratio)
    
    # Calculate crop bounds centered on text
    crop_left = max(0, text_center_x - new_width // 2)
    crop_top = max(0, text_center_y - new_height // 2)
    crop_right = min(img_width, crop_left + new_width)
    crop_bottom = min(img_height, crop_top + new_height)
    
    # Adjust if we hit image bounds
    if crop_right - crop_left < new_width:
        if crop_left == 0:
            crop_right = new_width
        else:
            crop_left = crop_right - new_width
    if crop_bottom - crop_top < new_height:
        if crop_top == 0:
            crop_bottom = new_height
        else:
            crop_top = crop_bottom - new_height
    
    return (crop_left, crop_top, crop_right, crop_bottom)

def process_style_previews():
    """Process all style preview images."""
    input_dir = "/Users/naman/Desktop/movie_py/react_style_showcase/subtitle_preview_app/public/style_previews"
    output_dir = "/Users/naman/Desktop/movie_py/react_style_showcase/subtitle_preview_app/public/style_previews_cropped"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each image
    for filename in os.listdir(input_dir):
        if filename.endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"Processing {filename}...")
            
            try:
                # Open image
                img = Image.open(input_path)
                
                # Find text bounds
                bounds = find_text_bounds(input_path)
                
                # Crop to fixed aspect ratio
                crop_bounds = crop_to_fixed_ratio(img, bounds, target_ratio=16/10)
                
                # Crop and save
                cropped = img.crop(crop_bounds)
                
                # Resize to consistent dimensions for UI
                cropped = cropped.resize((320, 200), Image.Resampling.LANCZOS)
                
                cropped.save(output_path)
                print(f"  Saved cropped image to {output_path}")
                
            except Exception as e:
                print(f"  Error processing {filename}: {e}")

if __name__ == "__main__":
    process_style_previews()
    print("\nAll style previews have been cropped!")