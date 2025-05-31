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
   - Updated import to use `word_highlight_effects_manual_fix`

2. **`subtitle_styles/core/json_style_loader.py`**
   - Updated import to use `word_highlight_effects_manual_fix`

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

## Implementation Date
May 30, 2025