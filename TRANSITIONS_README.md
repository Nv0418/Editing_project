# Custom Video Transition System

## Overview
This project includes a Python-based framework for defining, managing, and applying custom video transitions using the `movis` library. The system is designed to be extensible, allowing users to add new transitions by providing configuration files and image assets (masks).

## Core Components
-   **`scripts/transitions/registry.py`**: Contains the `TransitionRegistry` class, which is responsible for discovering and loading transition definitions.
-   **`transitions/` directory**: The designated root directory where all custom transition packages are expected to be stored. (Currently, this directory appears to be empty, so no transitions would be loaded by default).
-   **Transition Package Structure**: Each transition is expected to reside in its own subdirectory within a category under `transitions/`. For example: `transitions/distortion/my_custom_transition/`.
    -   **`config.json`**: A JSON file within each transition's folder, defining its properties (name, type, asset filenames, duration, description).
-   **Effect Implementation Scripts** (e.g., `scripts/transitions/proper_distortion_transition.py`, `scripts/transitions/distortion_transition_test.py`): These Python scripts define `movis` effect classes that utilize the loaded transition assets to create visual effects.

## How it Works
1.  **Registry Initialization**: The `TransitionRegistry` is initialized, pointing to the `transitions/` directory. It scans this directory for category folders and their `index.json` files, then loads individual transition `config.json` files and notes their assets.
2.  **Transition Definition**: Users define new transitions by:
    *   Creating a category folder in `transitions/` (e.g., `transitions/my_category/`).
    *   Adding an `index.json` in the category folder listing its transitions.
    *   For each transition, creating a subfolder (e.g., `transitions/my_category/cool_effect/`).
    *   Placing a `config.json` in the transition's folder with its details.
    *   Adding necessary asset images (e.g., `mask_a.jpg`, `mask_b.jpg`) to this folder.
3.  **Effect Logic**: Custom `movis` effect classes are written in Python (like `ProperDistortionTransitionEffect` in `proper_distortion_transition.py`). These classes:
    *   Are initialized with a path to a specific transition's assets.
    *   Load the asset images (masks).
    *   Implement a `__call__(self, frame, time, **kwargs)` method that processes video frames to create the visual transition. The current examples show simplified implementations (e.g., basic displacement or alpha masking) with comments indicating they are placeholders for more sophisticated techniques.
4.  **Application**: In a video editing script:
    *   The `TransitionRegistry` is used to get a specific transition's configuration.
    *   The custom effect class is instantiated with the path to the transition's assets.
    *   This effect is added to a `movis` layer.
    *   The example scripts often combine these custom effects with opacity animations on the video layers to achieve the transition between clips.

## Current Status & Example Implementations
-   The framework for managing transitions via a registry and configuration files is in place.
-   The example scripts (`proper_distortion_transition.py` and `distortion_transition_test.py`) demonstrate how to structure effects that use image masks.
    -   `proper_distortion_transition.py`: Attempts a basic pixel displacement effect using one mask.
    -   `distortion_transition_test.py`: Blends two masks and uses the result for a simple multiplicative masking effect.
-   **Important**: The actual visual effect logic in these examples is explicitly marked as simplified. Advanced techniques like optical flow or complex blending between masks over time are mentioned as future improvements.
-   **The `transitions/` directory is currently empty.** To use this system, you need to populate this directory with your own transition packages (folders, `config.json` files, and image mask assets). Without these, the registry will not load any transitions.

## Using the Transition System
1.  **Populate `transitions/`**: Create your transition packages as described under "Transition Package Structure".
2.  **Utilize in Scripts**:
    *   Import and initialize `TransitionRegistry`.
    *   Retrieve a desired transition using `registry.get_transition("category_name/transition_name")`.
    *   Instantiate your custom `movis` effect class (similar to those in the example scripts) using the path to the transition's assets.
    *   Apply this effect to video layers in your `movis` composition.

## GLSL Transitions
-   A `glsl_transitions/` directory exists, suggesting an intent or past work with GLSL-based transitions. However, this directory is also currently reported as empty. The Python-based framework described above does not directly reference or use GLSL shaders.
