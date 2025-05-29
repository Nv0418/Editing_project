#!/usr/bin/env python3
"""
Extract a frame from video to check subtitle positioning
"""

import cv2
import sys

def extract_frame(video_path, time_seconds, output_path):
    """Extract a single frame from video at specified time"""
    
    # Open video
    cap = cv2.VideoCapture(video_path)
    
    # Get FPS
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate frame number
    frame_number = int(fps * time_seconds)
    
    # Set frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read frame
    ret, frame = cap.read()
    
    if ret:
        # Save frame
        cv2.imwrite(output_path, frame)
        print(f"Frame extracted to: {output_path}")
    else:
        print("Error extracting frame")
    
    cap.release()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_frame.py <video_path> <time_in_seconds>")
        sys.exit(1)
    
    video_path = sys.argv[1]
    time = float(sys.argv[2])
    output_path = f"frame_at_{time}s.png"
    
    extract_frame(video_path, time, output_path)