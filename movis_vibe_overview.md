# Movis: Video Editing with Python - The Vibe Code Readme

Yo! So you wanna know what Movis is all about? Lemme break it down for ya, vibe code style.

## What's the Big Deal with Movis?

Imagine you're a video wizard, but instead of a magic wand, you use Python code. That's Movis! It's a Python library that lets you **make and edit videos by writing code**.

Think of it like Adobe After Effects or Premiere Pro, but you're typing commands instead of clicking buttons. You can do all sorts of cool stuff:

*   Cut scenes, stick 'em together.
*   Add text, images, shapes.
*   Make things move, fade, spin around (animations!).
*   Slap on effects like blurs, shadows, color changes.
*   Even mix audio and create subtitles.

It's especially neat for complex stuff where doing it by hand would be a pain, or if you want to automate video creation.

## How's it Built? What's Under the Hood?

Movis is a Python project, and it uses some other smart Python libraries to get the job done:

*   **NumPy**: For all the heavy math, especially when dealing with pixels and image data.
*   **Pillow (PIL)**: For basic image handling.
*   **Librosa**: For understanding and processing audio (like finding quiet parts or analyzing frequencies).
*   **imageio & imageio-ffmpeg**: For actually reading video files and, more importantly, *writing* your final MP4. FFmpeg is the workhorse video tool doing the encoding.
*   **OpenCV-Python**: For some advanced image processing and computer vision tricks.
*   **PySide6 (Qt)**: Sometimes used for drawing complex things (like the audio waveforms in one example) or if you wanted to build a GUI for a Movis tool.
*   **Pandas**: Not core, but some examples use it to organize lists of things to show in a video (like a sequence of images or dialogue lines).
*   **OpenCV-Python**: This is a powerhouse for "seeing" and "understanding" video frames. From a filmmaking perspective, this could mean:
    *   **Motion Tracking**: Think of attaching text or graphics to moving objects, or stabilizing shaky footage by tracking points in the scene.
    *   **Optical Flow**: Analyzing pixel movement to create smoother slow-motion (by generating in-between frames) or more realistic motion blur.
    *   **Automated Shot Detection**: Finding cuts in a long clip automatically.
    *   **Advanced Masking/Matting**: While Movis has specific tools like `ChromaKey` (which uses OpenCV for color math) and `RobustVideoMatting` (AI-based), OpenCV itself offers many algorithms that could be used to build custom tools for isolating elements.
    *   **Driving Effects with Analysis**: Imagine an effect that changes based on the brightness or amount of motion in the current frame – OpenCV can provide that analysis.
    Essentially, it's for tasks that require the computer to react to the *content* of the video, not just apply pre-set instructions.
*   **DiskCache**: To be clever and save bits of video it already figured out, so if you render again, it might be faster.

## The Main Hangout: The `movis/movis/` Folder

This is where the magic code lives. Here's the lowdown on the key files:

*   **`__init__.py`**: The bouncer at the club. It says, "Hey, all the important tools from Movis? You can grab 'em right here."
*   **`layer/` (folder)**: Think of layers in Photoshop. This is where Movis defines all the things you can put in your video:
    *   `Composition`: A big one! It's like a mini-video project within your main project. You can put layers in it, and then put *that whole composition* into another one. Nesting doll vibes!
    *   `Image`, `Video`, `Audio`: For bringing in your pictures, video clips, and sounds.
    *   `Rectangle`, `Ellipse`, `Line`, `Text`: For drawing basic shapes and putting words on screen.
    *   `Gradient`, `Stripe`: For cool background patterns.
    *   `AlphaMatte`, `LuminanceMatte`: Fancy ways to use one layer to control the transparency of another (like stencils).
*   **`effect/` (folder)**: This is your box of special effects:
    *   `GaussianBlur`, `Glow`: Make things blurry or shiny.
    *   `FillColor`, `HSLShift`: Mess with colors.
    *   `DropShadow`: Make things look like they're floating.
*   **`attribute.py`**: Super important! Every property of a layer (like its size, position, color, opacity) is an "Attribute." This file defines how these attributes work and, crucially, how they can be *animated*.
*   **`motion.py`**: The animation engine! This is where keyframes and easing functions live. You say, "At 0 seconds, be small. At 1 second, be big. And make it a smooth `ease_in_out` move." This file handles that.
*   **`transform.py`**: All about geometry – where things are (`position`), how big they are (`scale`), how much they're spun (`rotation`), and their `opacity`. It also handles `anchor_point` (the pivot for a layer's own spin/scale) and `origin_point` (which part of the layer lines up with its position on the screen). These are all `Attribute`s, so they can be animated.
*   **`ops.py`**: "Operations." These are shortcut functions for common editing tasks:
    *   `concatenate`: Stick clips end-to-end.
    *   `trim`: Cut out parts of a clip.
    *   `crop`: Cut out a rectangular area of a layer.
    *   `fade_in`, `fade_out`: Smoothly appear/disappear.
    *   `repeat`, `tile`, `insert`, `switch`: More ways to arrange and combine clips.
*   **`imgproc.py`**: "Image Processing." This is where the nitty-gritty pixel math happens, especially for **blending modes** (like "Multiply," "Screen," "Overlay" – how layers mix their colors) and putting semi-transparent images on top of each other (`alpha_composite`).
*   **`enum.py`**: Gives friendly names to settings. Instead of remembering `0` for "linear animation," you use `Easing.LINEAR`. Makes code easier to read. Defines things like `BlendingMode`, `Easing` types, `AttributeType` (is it a single number, a 2D point, a color?), etc.
*   **`subtitle.py`**: Tools for creating subtitle files (`.srt` or the fancier `.ass` format) from your text and timings.
*   **`util.py`**: Utility belt! Helper functions, like one to easily combine a video file, an audio file, and a subtitle file into a final MP4 using FFmpeg. Also has tools for understanding color names (like "red" or "#FF0000").

## The "Contrib" Crew: `movis/movis/contrib/`

This folder has extra, more specialized tools:

*   **`presentation.py`**:
    *   `Slide`: Lets you show pages from a PDF file as slides in your video, timed to your needs.
    *   `Character`: For putting 2D animated characters on screen (like a virtual presenter). It can handle different expressions and even make them blink!
*   **`segmentation.py`**:
    *   `ChromaKey`: Your classic green screen (or blue screen) remover.
    *   `RobustVideoMatting`: Fancy AI stuff! Tries to cut out people from a normal background without needing a green screen, using a deep learning model.
*   **`voicevox.py`**: If you use VOICEVOX (a Japanese text-to-speech app with anime voices), this helps you take its output (audio files and text files) and turn it into a timeline that Movis can use to sync dialogue, subtitles, and character animations.

## Show Me the Vibe! The `examples/` Folder

This is where you see Movis in action.

*   **`basic/`**: Simple demos to teach you the ropes.
    *   `alpha_matte`: Using one layer's transparency as a stencil for another.
    *   `custom_transition`: Making your own cool wipe effect with animating bars.
    *   `luminance_matte`: Using one layer's brightness to fade another (e.g., text fading at the edges).
    *   `motion_graphics`: A little title sequence with expanding circles and text reveals.
    *   `poptext`: Making text "pop" on screen in time with spoken words (uses a JSON file for timings).
    *   `rectangle_animation`: Basic animation of a rectangle's size and rotation.
*   **`application/`**: More real-world, complex stuff.
    *   `audio_visualization`: Creates those cool music visualizer videos with waveforms (lines or circles) that dance to the music. It even makes a custom Movis layer using Qt for drawing!
    *   `image_gallery`: Makes a slideshow video from a list of pictures, with animated titles for each. Uses Pandas to manage the image list.
    *   `shader_art`: For all you math artists! Creates abstract animated visuals by calculating the color of every pixel using formulas. (Think "demoscene" or Shadertoy).
    *   `video_summary_and_extraction`: A multi-step tool to:
        1.  Cut silences out of a presentation video.
        2.  Send the audio to OpenAI Whisper to get a transcript.
        3.  Rebuild the video without the silences and add the transcript as subtitles.
    *   `zundamon_commentary`: A full pipeline for making "Zundamon commentary videos" (a popular Japanese format). It uses VOICEVOX for character voices, shows PDF slides, animates Zundamon and Metan characters with different expressions, and adds subtitles, all driven by a master timeline file.

## Other Important Bits

*   **`docs/`**: Where the official instruction manual (documentation) is made.
*   **`tests/`**: Code that checks if all the bits of Movis are working correctly.
*   **`pyproject.toml`, `setup.py`, `requirements.txt`**: Files that tell Python how to install Movis and what other libraries it needs to run.

## Movis for Filmmakers: Technical Editing Concepts in Code

Okay, so you know filmmaking and editing. How does Movis translate those concepts into code? Pretty directly, actually!

*   **Non-Linear Editing (NLE) Core**:
    *   **Timeline & Compositions**: `Composition` is your main timeline or sequence. You can put layers (clips, graphics, text) onto it. Crucially, you can *nest* compositions inside other compositions. This is exactly like "nested sequences" in Premiere Pro or "pre-comps" in After Effects. It's super powerful for organizing complex scenes or creating reusable animated segments (like a title sequence you use in multiple videos).
    *   **Layers**: Just like in any NLE, you stack layers. Movis handles transparency (`alpha_composite`) and offers a full range of **Blending Modes** (Multiply, Screen, Overlay, etc.) for creative compositing, identical to what you find in Photoshop, Premiere, or After Effects.

*   **Precision Editing & Animation**:
    *   **Keyframing**: Any property of a layer (position, scale, rotation, opacity, even parameters of an effect) is an `Attribute` that can be keyframed. You define values at specific times, and Movis interpolates. This is like setting keyframes in an NLE's effects panel or timeline.
    *   **Easing Functions**: Movis gives you a ton of `Easing` options (linear, ease-in, ease-out, ease-in-out, and many variations). These control the *feel* of your animations – smooth starts and stops, snappy movements, etc., just like adjusting bezier curves for keyframes in GUI software.
    *   **Transform Controls**: `position`, `scale`, `rotation`, `opacity`, `anchor_point`, and `origin_point` give you precise control over how layers look and move, mirroring the transform panels in editing software.

*   **Standard Editing Operations (`ops.py`)**:
    *   `concatenate`, `trim`, `insert`: These are your bread-and-butter editing commands for assembling sequences.
    *   `crop`: Standard video cropping.
    *   `fade_in`, `fade_out`: Basic transitions.

*   **Visual Effects (VFX) & Compositing Building Blocks**:
    *   **Matting & Keying**: Essential for combining elements.
        *   `ChromaKey`: Your green/blue screen tool (uses OpenCV for color math).
        *   `AlphaMatte` & `LuminanceMatte`: Like track mattes in After Effects, using one layer's alpha or luma to control another's transparency.
        *   `RobustVideoMatting` (contrib): AI-powered rotoscoping/matting to cut subjects out without a green screen.
    *   **Effects (`effect/`)**: Standard effects like `GaussianBlur` (for depth of field, motion blur, or stylization), `HSLShift` (for color correction/grading), `DropShadow` are available.

*   **Data-Driven & Procedural Workflows**:
    *   **Automated Edits**: Because it's code, you can write scripts to make editing decisions. The `video_summary_and_extraction` example shows this by removing silences based on audio analysis.
    *   **Generative Content**: The `shader_art` example shows how to create visuals entirely from math. This can be used for abstract backgrounds, motion graphics elements, or unique visual effects.
    *   **Batch Processing & Templating**: If you need to make many similar videos (e.g., social media clips with different text but the same animation), Movis is perfect. You can create a template script and feed it different data. The `poptext` and `zundamon_commentary` examples show this by using external data (JSON, TSV files) to drive animations and content.

*   **Custom Tool Creation**:
    *   If an effect or transition doesn't exist, you can *build it*. The `custom_transition` example shows creating a unique wipe. The `audio_visualization` example builds a whole new layer type that draws waveforms using Qt. This is like building your own plugins directly within your editing environment.

Movis essentially takes the concepts and tools you're familiar with from traditional NLEs and VFX software and exposes them through a Python programming interface. This means less clicking and dragging, and more scripting, logic, and automation for complex or repetitive tasks.

## So, What's the Vibe?

Movis is for coders who want deep control over video creation. It's like having a programmable animation and editing studio. You can:

*   **Automate**: Make lots of similar videos from data.
*   **Get Precise**: Control animations and timings down to the exact frame or millisecond.
*   **Be Creative**: Build totally custom effects, transitions, and visualizers that might be hard or impossible in GUI software.
*   **Integrate**: Connect video creation with other Python libraries or AI services.

It's not for quick, simple edits if you're used to iMovie. But if you want to build something unique, data-driven, or highly customized in the video world, and you're cool with Python, Movis has got the vibes you're looking for!
