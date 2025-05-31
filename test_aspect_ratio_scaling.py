#!/usr/bin/env python3
"""
Test script to verify aspect ratio scaling logic
"""

def calculate_cover_scale(image_size, target_size):
    """Calculate scale factor to cover entire target area (no black borders)"""
    image_width, image_height = image_size
    target_width, target_height = target_size
    
    # Calculate aspect ratios
    image_aspect = image_width / image_height
    target_aspect = target_width / target_height
    
    # If aspect ratios are very close (within 1% tolerance), just fit the image
    aspect_tolerance = 0.01
    if abs(image_aspect - target_aspect) < aspect_tolerance:
        # Same aspect ratio - scale to fit exactly
        scale = min(target_width / image_width, target_height / image_height)
        print(f"  ✅ Same aspect ratio - FIT scale: {scale:.3f}")
        return scale
    
    # Different aspect ratios - scale to cover (no black borders)
    scale_x = target_width / image_width
    scale_y = target_height / image_height
    
    # Use the larger scale to ensure full coverage
    scale = max(scale_x, scale_y)
    print(f"  📐 Different aspect ratio - COVER scale: {scale:.3f}")
    return scale

# Test cases
target_size = (1080, 1920)  # Instagram 9:16
target_aspect = target_size[0] / target_size[1]

print(f"Target: {target_size} (aspect: {target_aspect:.3f})")
print()

test_cases = [
    # Same aspect ratio (should FIT)
    (1080, 1920, "Perfect Instagram size"),
    (540, 960, "Half Instagram size"),
    (2160, 3840, "Double Instagram size"),
    
    # Different aspect ratios (should COVER)
    (768, 1360, "Game of Thrones images"),
    (1920, 1080, "Landscape 16:9"),
    (1000, 1000, "Square 1:1"),
    (1080, 1350, "4:5 Instagram photo"),
]

for width, height, description in test_cases:
    aspect = width / height
    print(f"{description}: {(width, height)} (aspect: {aspect:.3f})")
    scale = calculate_cover_scale((width, height), target_size)
    final_size = (int(width * scale), int(height * scale))
    print(f"  Result: {final_size} -> {'✅ Fills screen' if scale >= 1.0 else '❌ Too small'}")
    print()