# Dynamic Karaoke System

## Overview
This system generates dynamic, style-driven karaoke videos using Python and the `movis` library. It leverages per-word transcription data (e.g., from Nvidia Parakeet) and allows for highly customizable visual styles defined in a JSON configuration file. The primary script for this system is `examples/dynamic_karaoke.py`.

## Core Components
-   **`examples/dynamic_karaoke.py`**: The main Python script responsible for loading styles, processing inputs, and generating the karaoke video.
-   **`subtitles_style.json`**: A JSON file where different visual styles for the karaoke text (animations, fonts, colors, layouts, backgrounds) are defined.
-   **Transcription File (e.g., `parakeet_output.json`)**: A JSON input file containing the transcript of the audio and precise start/end timestamps for each word.
-   **Audio File (e.g., `got_script.mp3`)**: The audio track that the karaoke text will be synchronized with.

## How it Works
1.  The `examples/dynamic_karaoke.py` script is executed with paths to the transcription data, audio file, a chosen style name, and an output file path.
2.  It loads the specified style's configuration from `subtitles_style.json`.
3.  It reads the word timings from the transcription file.
4.  Using `movis`, it creates a video composition, adding the audio track.
5.  For each word or segment of words (depending on the style's layout settings), it generates text layers.
6.  These text layers are animated (e.g., color change, size change on highlight) and positioned according to the rules defined in the loaded style.
7.  The background of the video is also determined by the style configuration (e.g., solid color, image, or video). If no complex background is specified, it often defaults to a black video layer, which is useful for testing text animations.

## Creating and Using Styles
-   Visual styles are defined as individual JSON objects within the main JSON structure in `subtitles_style.json`.
-   Each style must have a unique key (its name) and can include detailed configurations for:
    -   **`format`**: Video resolution, aspect ratio, target platforms.
    -   **`layout`**: Text positioning (e.g., lower_third, dynamic), words per window, vertical/horizontal positions. Some styles like "Cinematic_Dual_Style" support multi-mode layouts.
    -   **`typography`**: Font family, size, alignment, colors for normal and highlighted states. Multi-mode styles can have separate typography for different modes.
    -   **`animation`**: Type of animation (e.g., color_change), highlight method, transition types.
    -   **`background`**: Type of background (e.g., solid_color, text_boxes, or none).
-   New styles can be easily added by defining a new JSON object in `subtitles_style.json`.

## Basic Usage / Running the System
To generate a karaoke video, run the `dynamic_karaoke.py` script from the command line:

```bash
python3 examples/dynamic_karaoke.py <path_to_transcription.json> <path_to_audio.mp3> --style <style_name> --output <output_video_filename.mp4>
```

**Example:**
```bash
python3 examples/dynamic_karaoke.py parakeet_output.json got_script.mp3 --style Cinematic_Dual_Style --output output_test/karaoke_cinematic_dual_style_video.mp4
```
This command would use the `parakeet_output.json` transcription, `got_script.mp3` audio, apply the `Cinematic_Dual_Style` from `subtitles_style.json`, and save the result to `output_test/karaoke_cinematic_dual_style_video.mp4`.

## Testing Styles
-   Testing is primarily done by running the `examples/dynamic_karaoke.py` script with different `--style` arguments, pointing to styles defined in `subtitles_style.json`.
-   Many styles, if they don't define a specific image or video background, will render text over a black background by default. This is convenient for quickly iterating on and previewing text animations and typography without needing complex background assets.

## Key Files Summary
-   **Main Script**: `examples/dynamic_karaoke.py`
-   **Style Definitions**: `subtitles_style.json`
-   **Typical Inputs**:
    -   Transcription: `*.json` (e.g., `parakeet_output.json`)
    -   Audio: `*.mp3`, `*.wav`, etc. (e.g., `got_script.mp3`)
-   **Typical Output**: `*.mp4` (video file)
