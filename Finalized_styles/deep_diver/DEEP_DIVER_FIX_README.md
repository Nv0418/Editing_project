# Deep Diver Centering Fix

## Issue
The Deep Diver caption style had a horizontal centering issue where the gray background box appeared shifted to the right in 9:16 Instagram format videos.

## Solution
Applied a manual horizontal offset to correct the alignment.

## Files Created/Modified

### New Files
1. **`word_highlight_effects_manual_fix.py`** - Main fix implementation
   - Contains the `MANUAL_OFFSET = -40` parameter
   - Wraps the original Deep Diver effect and applies horizontal shift

2. **`generate_deep_diver_video.py`** - Test script for verification
   - Uses Game of Thrones audio and Parakeet transcription
   - Generates test video at `deep_diver_got_test.mp4`

### Modified Files
1. **`subtitle_styles/core/movis_layer.py`**
   - Updated `_render_deep_diver_style` method to import from `word_highlight_effects_manual_fix`
   - Only the Deep Diver style uses the manual fix; other styles use regular implementation

2. **`subtitle_styles/effects/word_highlight_effects_manual_fix.py`** (Corrected)
   - Fixed import issues by copying correct methods from original class
   - Removed non-existent `create_gradient_word_highlight_effect` method reference

## How to Adjust Centering
1. Open `subtitle_styles/effects/word_highlight_effects_manual_fix.py`
2. Find line with `MANUAL_OFFSET = -40`
3. Adjust the value:
   - **Negative values** = shift LEFT
   - **Positive values** = shift RIGHT
   - Current `-40` shifts 40 pixels left

## Testing
Run the test script:
```bash
cd /Users/naman/Desktop/movie_py/30may_test
python3 generate_deep_diver_video.py
```

## Current Status
✅ **FIXED** - Deep Diver style now renders with correct horizontal centering in 9:16 format.

## Implementation Date
May 30, 2025

## Latest Update
Fixed import errors in `word_highlight_effects_manual_fix.py` and applied correct centering fix to Deep Diver style while maintaining regular implementation for other styles.