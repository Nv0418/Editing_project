#!/usr/bin/env python3
import cv2
import os

# Open the final video
video_path = "/Users/naman/Desktop/movie_py/popling_caption_final.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps

print(f"Video duration: {duration:.1f} seconds")
print(f"FPS: {fps}")
print(f"Total frames: {total_frames}")

# Extract frames at key moments to show underline effect
time_points = [1, 3, 6, 9, 12, 15, 18]  # seconds

for time in time_points:
    frame_number = int(fps * time)
    if frame_number < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            output_path = f"/Users/naman/Desktop/movie_py/final_popling_frame_{time}s.png"
            cv2.imwrite(output_path, frame)
            print(f"Saved frame at {time}s to {output_path}")

cap.release()
print("\nFinal popling frames extracted successfully!")