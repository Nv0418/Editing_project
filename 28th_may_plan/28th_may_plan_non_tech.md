# VinVideo MVP Editing Pipeline — Non-Technical Overview

**Updated: May 28, 2025 (15-Day Sprint)**

Welcome, Vibe Coder! Here’s the simple, jargon-free roadmap for our 15-day push to build the core editing flow for VinVideo:

---

## What We’re Building
A super-lean web tool that:
- Takes AI-generated clips and captions.
- Lets users pick or swap background music.
- Automatically stitches everything together into a short video.
- Shows a quick preview when you hit “Generate.”

No fancy timeline scrubbing or deep color magic—just click, watch, share.

---

## The 15-Day Countdown
We split work into two squads working side by side:

| Days   | Backend Team (Server & Logic)                           | Frontend Team (UI & UX)                     |
|--------|---------------------------------------------------------|----------------------------------------------|
| 1–3    | Set up the project data structure and simple APIs       | Build the edit page shell and connect APIs   |
| 4–6    | Plug in clip sequencing and subtitle overlay logic      | Show clip thumbnails and subtitle toggle     |
| 7–9    | Wire up audio layering and video export service         | Add music-change/remove buttons + regenerate |
| 10–12  | Create a basic “preview” endpoint for quick samples     | Display preview and download link            |
| 13–14  | Hook up “regenerate” flow and run smoke tests           | Polish UI, add error messages                |
| 15     | Final end-to-end check and deploy                       | Final QA and handoff                         |

---

## Key Features in Plain English
- **Clip Line-Up**: We’ll line up clips in order with simple hard cuts or quick fades.
- **Subtitles**: We burn in captions using timestamps we already have.
- **Music Control**: A single music track that you can swap out or mute.
- **Regenerate**: Change your prompt, hit regenerate, and your clip updates in place.
- **One-Click Render**: Hit “Generate” and we build your video on the server, then show it back to you.

---

## Why This Works
- **No Drag & Drop**: Fixed sequence saves days of complexity.
- **API-Driven**: Frontend just calls our endpoints—no browser-side video engine.
- **Movis + FFmpeg**: We reuse proven code for assembly and encoding.
- **Parallel Streams**: Devs work on server and UI at the same time to hit 15 days.

---

## How You Can Help
- Keep the page light: minimal animations, clear buttons.
- Use placeholder loaders for preview until it’s wired up.
- Test flows fast—no deep test suite yet, just smoke tests.
- Share feedback daily so we can tweak on the fly.

Let’s ship this MVP fast, get real users playing, and then dial in the sparkle!

---

## How It Works Under the Hood
1. We upload all AI-generated clips to an S3 bucket.
2. The frontend asks our API to build the edit.
3. A job goes into a queue, and a backend worker (a container/VM) grabs the clips from S3.
4. The worker uses Movis+FFmpeg to stitch the clips, subtitles, and music into one video.
5. The final video is stored back in S3, and the frontend gets the link to play it.
6. Users see the updated video and can make light changes (swap music, toggle subtitles, regenerate) with one click.