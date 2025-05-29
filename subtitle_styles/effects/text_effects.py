"""
Text Effects Module
Provides various text effects like glow, shadow, outline using PIL/Pillow
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import Tuple, Optional, Union, List
import os


class TextEffects:
    """Collection of text effect methods"""
    
    @staticmethod
    def create_glow_effect(text: str,
                          font_path: str,
                          font_size: int,
                          text_color: Tuple[int, int, int],
                          glow_color: Tuple[int, int, int],
                          glow_radius: int = 10,
                          glow_intensity: float = 0.8,
                          image_size: Tuple[int, int] = (1080, 1920)) -> np.ndarray:
        """
        Create glowing text effect
        Returns RGBA numpy array
        """
        # Create image with transparent background
        padding = glow_radius * 3
        width, height = image_size
        
        # Create larger canvas for glow effect
        img = Image.new('RGBA', (width + padding*2, height + padding*2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center position
        x = (width + padding*2 - text_width) // 2
        y = (height + padding*2 - text_height) // 2
        
        # Create glow layers
        glow_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        
        # Draw multiple glow layers with decreasing opacity
        for i in range(glow_radius, 0, -1):
            opacity = int(255 * glow_intensity * (i / glow_radius))
            current_glow_color = (*glow_color, opacity)
            
            # Draw text with stroke for glow
            glow_draw.text((x, y), text, font=font, 
                          fill=current_glow_color,
                          stroke_width=i*2, 
                          stroke_fill=current_glow_color)
        
        # Apply gaussian blur to glow
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=glow_radius//2))
        
        # Composite glow onto main image
        img = Image.alpha_composite(img, glow_img)
        
        # Draw main text on top
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, font=font, fill=(*text_color, 255))
        
        # Crop back to original size
        img = img.crop((padding, padding, width + padding, height + padding))
        
        # Convert to numpy array (RGBA)
        return np.array(img)
    
    @staticmethod
    def create_shadow_effect(text: str,
                           font_path: str,
                           font_size: int,
                           text_color: Tuple[int, int, int],
                           shadow_color: Tuple[int, int, int] = (0, 0, 0),
                           shadow_offset: Tuple[int, int] = (5, 5),
                           shadow_blur: int = 3,
                           shadow_opacity: float = 0.7,
                           image_size: Tuple[int, int] = (1080, 1920)) -> np.ndarray:
        """
        Create text with drop shadow effect
        Returns RGBA numpy array
        """
        width, height = image_size
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Create shadow layer
        shadow_img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_img)
        
        # Draw shadow
        shadow_alpha = int(255 * shadow_opacity)
        shadow_draw.text((x + shadow_offset[0], y + shadow_offset[1]), 
                        text, font=font, 
                        fill=(*shadow_color, shadow_alpha))
        
        # Blur shadow
        if shadow_blur > 0:
            shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
        
        # Composite shadow onto main image
        img = Image.alpha_composite(img, shadow_img)
        
        # Draw main text
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, font=font, fill=(*text_color, 255))
        
        return np.array(img)
    
    @staticmethod
    def create_outline_effect(text: str,
                            font_path: str,
                            font_size: int,
                            text_color: Tuple[int, int, int],
                            outline_color: Tuple[int, int, int],
                            outline_width: int = 3,
                            image_size: Tuple[int, int] = (1080, 1920)) -> np.ndarray:
        """
        Create text with outline effect
        Returns RGBA numpy array
        """
        width, height = image_size
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center position
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text with outline
        draw.text((x, y), text, font=font, 
                 fill=(*text_color, 255),
                 stroke_width=outline_width,
                 stroke_fill=(*outline_color, 255))
        
        return np.array(img)
    
    @staticmethod
    def create_gradient_text(text: str,
                           font_path: str,
                           font_size: int,
                           gradient_colors: List[Tuple[int, int, int]],
                           gradient_direction: str = 'vertical',
                           image_size: Tuple[int, int] = (1080, 1920)) -> np.ndarray:
        """
        Create text with gradient fill
        Returns RGBA numpy array
        """
        width, height = image_size
        
        # Create base image
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Create text mask
        mask = Image.new('L', (width, height), 0)
        mask_draw = ImageDraw.Draw(mask)
        
        # Get text position
        bbox = mask_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text on mask
        mask_draw.text((x, y), text, font=font, fill=255)
        
        # Create gradient
        gradient = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        gradient_draw = ImageDraw.Draw(gradient)
        
        if gradient_direction == 'vertical':
            for i in range(height):
                factor = i / height
                color = TextEffects._interpolate_gradient(gradient_colors, factor)
                gradient_draw.line([(0, i), (width, i)], fill=(*color, 255))
        else:  # horizontal
            for i in range(width):
                factor = i / width
                color = TextEffects._interpolate_gradient(gradient_colors, factor)
                gradient_draw.line([(i, 0), (i, height)], fill=(*color, 255))
        
        # Apply mask to gradient
        gradient.putalpha(mask)
        
        # Composite onto main image
        img = Image.alpha_composite(img, gradient)
        
        return np.array(img)
    
    @staticmethod
    def _interpolate_gradient(colors: List[Tuple[int, int, int]], factor: float) -> Tuple[int, int, int]:
        """Helper function to interpolate between multiple colors"""
        if len(colors) < 2:
            return colors[0] if colors else (255, 255, 255)
        
        # Determine which two colors to interpolate between
        segment_size = 1.0 / (len(colors) - 1)
        segment = int(factor / segment_size)
        segment = min(segment, len(colors) - 2)
        
        local_factor = (factor - segment * segment_size) / segment_size
        
        color1 = colors[segment]
        color2 = colors[segment + 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * local_factor)
        g = int(color1[1] + (color2[1] - color1[1]) * local_factor)
        b = int(color1[2] + (color2[2] - color1[2]) * local_factor)
        
        return (r, g, b)
    
    @staticmethod
    def create_animated_glow_pulse(text: str,
                                 font_path: str,
                                 font_size: int,
                                 text_color: Tuple[int, int, int],
                                 glow_color: Tuple[int, int, int],
                                 time: float,
                                 pulse_frequency: float = 0.5,
                                 min_intensity: float = 0.3,
                                 max_intensity: float = 1.0,
                                 image_size: Tuple[int, int] = (1080, 1920)) -> np.ndarray:
        """
        Create animated pulsing glow effect based on time
        """
        # Calculate current intensity based on time and frequency
        pulse_phase = (time * pulse_frequency * 2 * np.pi) % (2 * np.pi)
        intensity = min_intensity + (max_intensity - min_intensity) * (np.sin(pulse_phase) + 1) / 2
        
        # Calculate glow radius based on intensity
        base_radius = 10
        glow_radius = int(base_radius + intensity * 10)
        
        return TextEffects.create_glow_effect(
            text, font_path, font_size, text_color, glow_color,
            glow_radius=glow_radius, glow_intensity=intensity,
            image_size=image_size
        )