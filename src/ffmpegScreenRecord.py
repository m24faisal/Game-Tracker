import os
import time
import subprocess
import imageio_ffmpeg as ffmpeg

FINAL_OUTPUT = "../saves/" + f"output_{time.time()}.mp4"
DURATION = 60  # seconds
FPS_TARGET = 60  # Frames per second

def record_screen(output_file="output.mp4", duration=10, fps=60):
    ffmpeg_cmd = [
        "ffmpeg",
        "-f", "gdigrab",  # Windows capture method
        "-framerate", str(fps),  # Capture at desired FPS
        "-i", "desktop",  # Capture the entire desktop
        "-t", str(duration),  # Duration of the recording
        "-vcodec", "libx264",  # Use the x264 codec for compression
        "-preset", "fast",  # Encoding speed (trade-off for size and quality)
        output_file
    ]
    subprocess.run(ffmpeg_cmd)

# Example usage: record for 10 seconds at 60 FPS
record_screen(FINAL_OUTPUT, duration=DURATION, fps=FPS_TARGET)
# we are testing to see if 60fps and 60 seconds match the final output video generated. often the video has a different
# size due to bad screen recording and dropped frames, final test , prev had a file that was corrupted and it sucked.
# target 60fps and 60 but less than 60fps 