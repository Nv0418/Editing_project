# Movis Technical Overview (README_4.md)

This document provides a detailed technical overview of the Movis library, based on an analysis of its codebase, examples, and supporting files. Movis is a Python library designed for programmatic video creation and editing.

## 1. Core Philosophy and Architecture

Movis enables "video editing as code," allowing users to define video compositions, layers, animations, and effects through Python scripting. This approach offers precision, automation capabilities, and the flexibility to integrate with other Python libraries and external tools.

The architecture is centered around:
*   **Compositions**: The primary containers for video scenes, analogous to sequences or timelines in traditional NLEs. Compositions have a defined size and duration and can contain multiple layers. They can also be nested.
*   **Layers**: Represent visual and audio elements within a composition. Movis provides various layer types for images, videos, audio, text, and procedural graphics.
*   **Attributes**: Properties of layers (e.g., position, scale, opacity, color) that can be static or animated over time.
*   **Motion & Animation**: A keyframe-based animation system with easing functions allows for dynamic changes to attributes.
*   **Effects**: Visual effects that can be applied to layers to modify their appearance.
*   **Modularity**: The library is structured into distinct modules for different functionalities (layers, effects, operations, image processing, etc.).

## 2. Key Dependencies

Movis leverages several external Python libraries:

*   **NumPy**: Fundamental for numerical operations, especially for representing and manipulating image pixel data as arrays.
*   **Pillow (PIL)**: Used for basic image loading, manipulation, and saving tasks.
*   **Librosa**: Provides tools for audio analysis, such as loading audio, calculating duration, and performing STFT for frequency analysis (seen in examples like audio visualization).
*   **imageio & imageio-ffmpeg**: Essential for reading various media formats and, critically, for writing the final video output, typically using FFmpeg as the backend encoder.
*   **OpenCV-Python (`opencv-python`)**: Used for more advanced image processing tasks, including color space conversions (e.g., RGB to HSV for chroma keying) and potentially other computer vision tasks if extended by the user.
*   **PySide6 (Qt)**: Utilized in some examples (e.g., `audio_visualization`) for custom 2D drawing directly onto QImage objects, which are then converted to NumPy arrays for Movis. This suggests an avenue for creating highly custom visual layers.
*   **Pandas**: Employed in several application examples (`image_gallery`, `zundamon_commentary`, `video_summary_and_extraction`) for managing timelines, dialogue scripts, and other structured data that drives video content.
*   **DiskCache**: Used for caching intermediate rendering results to potentially speed up subsequent renders if parts of the composition have not changed.
*   **tqdm**: For displaying progress bars during long operations like video rendering.
*   **ONNX Runtime (`onnxruntime`)**: An optional dependency for the `RobustVideoMatting` effect in `movis.contrib.segmentation`, allowing inference with deep learning models in ONNX format.
*   **pdf2image**: An optional dependency for the `Slide` layer in `movis.contrib.presentation`, used to convert PDF pages to images.
*   **SoundFile (`soundfile`)**: Used in the `video_summary_and_extraction` example for writing WAV audio files.
*   **ffmpeg-python**: Used in `movis.util` for muxing operations (e.g., adding audio/subtitles to a video file).

## 3. Core Library Modules (`movis/movis/`)

### 3.1. `__init__.py`
Serves as the main public API entry point, re-exporting key classes and functions from submodules for easier access (e.g., `mv.layer.Composition`, `mv.effect.GaussianBlur`).

### 3.2. `attribute.py`
*   **`Attribute` Class**: Represents an animatable property of a layer or effect (e.g., `position`, `opacity`, `color`). It holds an initial value, type (`AttributeType`), optional range constraints, and can be associated with a `Motion` object for keyframe animation and/or custom procedural functions.
*   **`AttributesMixin` Class**: A mixin to help layers/effects expose their `Attribute` instances for caching purposes (generating a hashable key based on current attribute values).
*   **`transform_to_hashable`**: Utility to convert attribute values (often NumPy arrays) to hashable types for cache keys.

### 3.3. `motion.py`
*   **Easing Functions**: Defines various mathematical easing functions (`linear`, `EaseIn`, `EaseOut`, `EaseInOut`, `flat`, and powered variants like `EaseIn2` to `EaseIn35`) that control the rate of change between keyframes.
*   **`Motion` Class**: The core animation engine. It stores keyframes (time points), corresponding values for an attribute, and the easing functions to apply between keyframes. Its `__call__` method interpolates the value of an attribute at any given time.
*   **`transform_to_numpy`**: Utility to convert various input types (scalars, sequences) into consistently shaped NumPy arrays suitable for animation values.

### 3.4. `transform.py`
*   **`TransformValue` (NamedTuple)**: A data structure holding a snapshot of all transformation properties (anchor_point, position, scale, rotation, opacity, origin_point, blending_mode) at a specific time.
*   **`Transform` Class**: Encapsulates the standard geometric transformations for a layer. Each transform property (`position`, `scale`, `rotation`, `opacity`, `anchor_point`) is an `Attribute` instance, making them individually animatable. It also holds static `origin_point` and `blending_mode`.
    *   `from_positions()`: A class method to conveniently define a transform based on edge-relative positioning and object fitting (contain/cover).
    *   `get_current_value(time)`: Returns a `TransformValue` for the given time.
*   Helper functions (`transform_to_1dscalar`, `transform_to_2dvector`, `transform_to_3dvector`) for normalizing transform value types.

### 3.5. `layer/` Sub-package
Defines the various types of layers that can be added to a composition.
*   **`__init__.py`**: Exports key layer classes.
*   **`protocol.py`**: Defines base protocols/interfaces like `Layer` and `BasicLayer` that other layer types should adhere to (e.g., must have a `duration` and a `__call__(time)` method that returns an image or `None`).
*   **`composition.py`**:
    *   `Composition` Class: The primary container for scenes. Manages a list of `LayerItem`s, overall size, and duration. Handles rendering by compositing its layers. Can be nested.
    *   `LayerItem` Class: Represents a layer when added to a composition, holding its specific `offset`, `start_time`, `end_time`, `name`, and its own `Transform` object.
*   **`media.py`**: Layers for external media:
    *   `Image`: For still images.
    *   `Video`: For video files (uses `imageio`).
    *   `Audio`: For audio files (uses `librosa`).
    *   `ImageSequence`, `AudioSequence`: For handling sequences of images or audio files as a single layer.
*   **`drawing.py`**: Layers for procedural drawing:
    *   `Rectangle`, `Ellipse`, `Line`: For basic geometric shapes. These can have `FillProperty` and `StrokeProperty`.
    *   `Text`: For rendering text with specified font, size, color, alignment, etc. (uses Pillow for rendering).
*   **`texture.py`**: Layers for generating procedural textures:
    *   `Gradient`: Creates color gradients.
    *   `Stripe`: Creates striped patterns.
*   **`layer_ops.py`**: Special layer types that operate on other layers:
    *   `AlphaMatte`: Uses one layer's alpha channel to mask another.
    *   `LuminanceMatte`: Uses one layer's luminance to mask another.
*   **`mixin.py`**:
    *   `TimelineMixin`: Provides common functionality for layers that have a timeline defined by multiple start/end segments (e.g., `Slide`, `Character` in contrib).

### 3.6. `effect/` Sub-package
Defines visual effects that can be applied to layers.
*   **`__init__.py`**: Exports key effect classes.
*   **`protocol.py`**: Defines an `Effect` protocol (likely a `__call__(prev_image, time)` method).
*   **`blur.py`**: `GaussianBlur`, `Glow`.
*   **`color.py`**: `FillColor` (overlays a color), `HSLShift` (adjusts Hue, Saturation, Lightness).
*   **`style.py`**: `DropShadow`.

### 3.7. `ops.py`
Provides higher-level functions for common video editing operations, typically returning new `Composition` or specialized layer-like objects.
*   `concatenate`: Joins layers sequentially.
*   `trim`: Extracts specified time segments from a layer and concatenates them.
*   `crop`: Extracts a rectangular region from a layer.
*   `repeat`: Repeats a layer multiple times.
*   `tile`: Arranges multiple layers in a grid.
*   `switch`: Cuts between different layers at specified times.
*   `insert`: Inserts one layer into another at a specific time.
*   `fade_in`, `fade_out`, `fade_in_out`: Convenience functions to create fade transitions by animating opacity and audio levels.

### 3.8. `imgproc.py`
Handles low-level image processing, primarily for compositing and blending.
*   **Blending Mode Functions**: Implements the mathematics for various blending modes (Normal, Multiply, Screen, Overlay, etc.) using NumPy operations on pixel data.
*   **`alpha_composite`**: The main function for overlaying a foreground RGBA image onto a background RGBA image. It handles position, opacity, and applies the selected blending mode. It intelligently uses Pillow's faster `alpha_composite` for normal blending without mattes, and its own NumPy-based implementation for other modes or when mattes are involved.
*   **`qimage_to_numpy`**: Converts a PySide6 `QImage` (ARGB32 format) to an RGBA NumPy array.

### 3.9. `enum.py`
Defines various `Enum` types used throughout the library for named constants, enhancing readability and type safety.
*   `AttributeType`: (SCALAR, VECTOR2D, VECTOR3D, ANGLE, COLOR)
*   `Easing`: (LINEAR, EASE_IN, EASE_OUT, EASE_IN_OUT, FLAT, and many powered variants)
*   `BlendingMode`: (NORMAL, MULTIPLY, SCREEN, etc.)
*   `MatteMode`: (NONE, ALPHA, LUMINANCE)
*   `Direction`: (BOTTOM_LEFT, CENTER, TOP_RIGHT, etc.) for anchor/origin points.
*   `TextAlignment`: (LEFT, CENTER, RIGHT)
*   `CacheType`: (COMPOSITION, LAYER)

### 3.10. `subtitle.py`
Provides functionality for generating subtitle files.
*   **`ASSStyleType` (NamedTuple)**: Defines styling options for ASS subtitles.
*   **`rgb_to_ass_color`**: Converts standard color representations to the ASS color format.
*   **`write_ass_file`**: Generates Advanced SubStation Alpha (.ass) subtitle files, supporting rich styling.
*   **`write_srt_file`**: Generates SubRip Text (.srt) subtitle files.

### 3.11. `util.py`
Contains miscellaneous utility functions.
*   **`add_materials_to_video`**: Uses `ffmpeg-python` to mux (combine) separate video, audio, and optional subtitle files into a single output video file.
*   **`to_rgb`**: A flexible color parsing function that converts CSS color names or hex strings into RGB integer tuples.

## 4. Contributed Modules (`movis/movis/contrib/`)

These modules provide more specialized, higher-level functionalities.
*   **`presentation.py`**:
    *   `Slide`: A layer to display pages from a PDF file as timed slides, using `pdf2image`.
    *   `Character`: A layer to display and animate 2D characters with changing expressions and blinking, based on a directory of image assets.
*   **`segmentation.py`**:
    *   `ChromaKey`: An effect for traditional green/blue screen keying (uses OpenCV for HSV conversion and masking).
    *   `RobustVideoMatting`: An effect using an ONNX deep learning model to perform foreground segmentation (typically for people) without a key color. Downloads a default model if not provided.
*   **`voicevox.py`**: Utilities for integrating with VOICEVOX (Japanese TTS software).
    *   `make_voicevox_dataframe`: Creates a Pandas DataFrame with audio file paths and their calculated start/end times for sequential playback.
    *   `make_timeline_from_voicevox`: Creates a Pandas DataFrame from VOICEVOX `.txt` files, extracting character, text (with line breaks for subtitles), and a content hash.
    *   `merge_timeline`: Merges an old timeline DataFrame with a new one, highlighting changes based on content hashes, useful for script revisions.

## 5. Examples (`examples/`)

The `examples/` directory is crucial for understanding practical usage.
*   **`basic/`**: Contains simple, focused demonstrations of core features:
    *   `alpha_matte`: Demonstrates `mv.layer.AlphaMatte`.
    *   `custom_transition`: Shows how to create a user-defined procedural effect for transitions.
    *   `luminance_matte`: Demonstrates `mv.layer.LuminanceMatte`.
    *   `motion_graphics`: A more complex animation with multiple layers, timed sequences, and reveal effects.
    *   `poptext`: Synchronizes text animations to audio timings loaded from a JSON file.
    *   `rectangle_animation`: Basic keyframe animation of a rectangle's size and rotation.
*   **`application/`**: Showcases more complex, real-world style applications:
    *   `audio_visualization`: Creates a music visualizer with linear or circular waveforms, involving custom layer drawing with PySide6/Qt and audio analysis with Librosa.
    *   `image_gallery`: Generates a slideshow video from a list of images with animated titles, managed by a Pandas DataFrame.
    *   `shader_art`: Procedurally generates animated abstract visuals (shader-like effects) using NumPy. Includes a JAX version for potential GPU acceleration.
    *   `video_summary_and_extraction`: A multi-step CLI tool to remove silences from a video, transcribe the audio using OpenAI Whisper, and re-render the video with the silences cut and subtitles added.
    *   `zundamon_commentary`: A full pipeline for creating "Zundamon" style commentary videos, integrating VOICEVOX audio, PDF slides, animated characters, and subtitles, all driven by a central timeline TSV file.

## 6. Supporting Directories and Files

*   **`docs/`**: Contains source files (reStructuredText) for the project's official documentation, likely built using Sphinx. Includes configuration (`conf.py`), individual pages (`.rst`), and static assets.
*   **`tests/`**: Contains unit tests for various modules, ensuring code correctness and stability.
*   **`images/` (root)**: Contains the main Movis logo.
*   **`.gitignore`**: Specifies intentionally untracked files for Git.
*   **`LICENSE`**: Contains the MIT License terms.
*   **`pyproject.toml`**: Primarily used for build system configuration (e.g., Ruff linter settings).
*   **`requirements.txt`**: Lists runtime dependencies.
*   **`setup.cfg`**, **`setup.py`**: Standard Python packaging files for distributing the library.

## 7. Overall Technical Impression

Movis is a well-structured and comprehensive library for programmatic video editing in Python. It provides a good balance of high-level abstractions (like `Composition`, `Layer`, common `ops`) and low-level control (direct attribute animation, custom effect functions, procedural layer generation). The use of NumPy for image data and the integration with FFmpeg for I/O are standard and robust choices. The `contrib` modules and application examples demonstrate its capability to handle complex, real-world video generation tasks, including integration with AI services and other specialized tools. The design emphasizes extensibility, allowing users to create custom layers and effects to suit specific needs.
