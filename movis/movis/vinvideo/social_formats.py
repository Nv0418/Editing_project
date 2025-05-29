"""
Social Media Format Optimization for VinVideo

Handles platform-specific export settings and optimizations for 
TikTok, Instagram Reels, YouTube Shorts, etc.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, Any, Tuple
from dataclasses import dataclass


class SocialMediaFormat(Enum):
    """Supported social media platforms."""
    TIKTOK = "tiktok"
    INSTAGRAM_REEL = "instagram_reel"
    YOUTUBE_SHORT = "youtube_short"
    INSTAGRAM_STORY = "instagram_story"
    SNAPCHAT = "snapchat"
    TWITTER = "twitter"


@dataclass
class PlatformSettings:
    """Platform-specific video settings."""
    resolution: Tuple[int, int]
    aspect_ratio: str
    max_duration: float
    fps: float
    codec: str
    bitrate_range: Tuple[int, int]  # min, max in kbps
    audio_codec: str
    audio_bitrate: int  # kbps
    safe_area_margins: Tuple[int, int, int, int]  # top, right, bottom, left


# Platform-specific settings database
PLATFORM_SETTINGS = {
    SocialMediaFormat.TIKTOK: PlatformSettings(
        resolution=(1080, 1920),
        aspect_ratio="9:16",
        max_duration=60.0,
        fps=30.0,
        codec="libx264",
        bitrate_range=(1500, 3000),
        audio_codec="aac",
        audio_bitrate=128,
        safe_area_margins=(100, 40, 200, 40)  # Account for UI overlays
    ),
    
    SocialMediaFormat.INSTAGRAM_REEL: PlatformSettings(
        resolution=(1080, 1920),
        aspect_ratio="9:16", 
        max_duration=90.0,
        fps=30.0,
        codec="libx264",
        bitrate_range=(2000, 4000),
        audio_codec="aac",
        audio_bitrate=128,
        safe_area_margins=(150, 40, 250, 40)
    ),
    
    SocialMediaFormat.YOUTUBE_SHORT: PlatformSettings(
        resolution=(1080, 1920),
        aspect_ratio="9:16",
        max_duration=60.0,
        fps=30.0,
        codec="libx264",
        bitrate_range=(2500, 5000),
        audio_codec="aac", 
        audio_bitrate=192,
        safe_area_margins=(80, 40, 160, 40)
    ),
    
    SocialMediaFormat.INSTAGRAM_STORY: PlatformSettings(
        resolution=(1080, 1920),
        aspect_ratio="9:16",
        max_duration=15.0,
        fps=30.0,
        codec="libx264",
        bitrate_range=(1500, 3000),
        audio_codec="aac",
        audio_bitrate=128,
        safe_area_margins=(200, 40, 300, 40)
    )
}


def format_for_platform(platform: str | SocialMediaFormat) -> Dict[str, Any]:
    """Get export settings optimized for a specific platform."""
    if isinstance(platform, str):
        try:
            platform = SocialMediaFormat(platform.lower())
        except ValueError:
            raise ValueError(f"Unsupported platform: {platform}")
    
    settings = PLATFORM_SETTINGS.get(platform)
    if not settings:
        raise ValueError(f"No settings defined for platform: {platform}")
    
    return {
        "fps": settings.fps,
        "codec": settings.codec,
        "pixelformat": "yuv420p",
        "output_params": [
            "-b:v", f"{settings.bitrate_range[1]}k",
            "-maxrate", f"{settings.bitrate_range[1]}k", 
            "-bufsize", f"{settings.bitrate_range[1] * 2}k",
            "-preset", "medium",
            "-profile:v", "high",
            "-level", "4.0",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart"
        ],
        "audio_codec": settings.audio_codec,
        "audio": True
    }


def validate_content_for_platform(
    platform: str | SocialMediaFormat,
    duration: float,
    resolution: Tuple[int, int]
) -> Dict[str, Any]:
    """Validate if content meets platform requirements."""
    if isinstance(platform, str):
        platform = SocialMediaFormat(platform.lower())
    
    settings = PLATFORM_SETTINGS.get(platform)
    if not settings:
        return {"valid": False, "reason": f"Unknown platform: {platform}"}
    
    issues = []
    
    # Check duration
    if duration > settings.max_duration:
        issues.append(f"Duration {duration}s exceeds maximum {settings.max_duration}s")
    
    # Check resolution
    if resolution != settings.resolution:
        issues.append(f"Resolution {resolution} doesn't match recommended {settings.resolution}")
    
    # Check aspect ratio
    actual_ratio = resolution[0] / resolution[1]
    expected_w, expected_h = settings.resolution
    expected_ratio = expected_w / expected_h
    
    if abs(actual_ratio - expected_ratio) > 0.01:  # Allow small tolerance
        issues.append(f"Aspect ratio mismatch: got {actual_ratio:.2f}, expected {expected_ratio:.2f}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "platform_settings": settings
    }


def get_safe_area_for_platform(platform: str | SocialMediaFormat) -> Tuple[int, int, int, int]:
    """Get safe area margins for text/important content placement."""
    if isinstance(platform, str):
        platform = SocialMediaFormat(platform.lower())
    
    settings = PLATFORM_SETTINGS.get(platform)
    if settings:
        return settings.safe_area_margins
    return (100, 40, 200, 40)  # Default safe margins
