#!/usr/bin/env python

import os

from PIL import Image, ImageChops, ImageStat


def is_different(image1, image2, threshold=30):
    """Check if two images are different based on a threshold."""
    diff = ImageChops.difference(image1, image2)
    stat = ImageStat.Stat(diff)
    # Calculate the root-mean-square (RMS) difference
    diff_rms = sum(stat.mean) / len(stat.mean)

    return diff_rms > threshold


def extract_unique_frames(gif_path, output_folder, threshold=30):
    """Extract frames from a GIF that are different from the previous frame based on a threshold."""
    gif = Image.open(gif_path)
    previous_frame = None
    frame_index = 0

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    while True:
        # Convert the current frame to RGB (ignoring transparency)
        current_frame = gif.convert("RGB")
        if previous_frame is None or is_different(
            previous_frame, current_frame, threshold
        ):
            current_frame.save(f"{output_folder}/frame_{frame_index:04d}.png")
            previous_frame = current_frame
            frame_index += 1

        # Move to the next frame
        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break


# Usage
gif_path = "ridi.gif"
output_folder = "output_frames"
threshold = 1  # Adjust the threshold value as needed
extract_unique_frames(gif_path, output_folder, threshold)
