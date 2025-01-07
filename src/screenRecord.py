import cv2
import numpy as np
import mss
import time
import subprocess
import os

def stretch_video(input_file, output_file, target_duration):
    """
    Stretches a video to a fixed length using FFmpeg.
    
    Args:
        input_file (str): Path to the input video file.
        output_file (str): Path to the output video file.
        target_duration (float): Desired duration of the output video in seconds.
    
    Returns:
        bool: True if the operation is successful, False otherwise.
    """

    print("input:", os.path.exists(input_file),", output:",os.path.exists(output_file))
    input_file, output_file = os.path.abspath(input_file), os.path.abspath(output_file) # uptdates to absolute path for both input and output
    print("input:", os.path.exists(input_file),", output:",os.path.exists(output_file))
    try:
        # Get the original duration of the video using FFmpeg
        result = subprocess.run(
            [
                "ffprobe", 
                "-v", "error", 
                "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", 
                input_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        original_duration = float(result.stdout.strip())
        
        # Calculate the stretch factor
        stretch_factor = target_duration / original_duration
        
        # Run the FFmpeg command to stretch the video
        command = [
            "ffmpeg",
            "-i", input_file,  # Input file
            "-vf", f"setpts={1/stretch_factor}*PTS",  # Adjust playback speed
            "-af", f"atempo={stretch_factor}",  # Adjust audio speed
            output_file  # Output file
        ]
        
        subprocess.run(command, check=True)
        
        return os.path.exists(output_file)  # Check if the output file was created
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Screen resolution (adjust to your screen size)
SCREEN_SIZE = (1920, 1080)  # Replace with your screen resolution

# Output file
output = "../saves/" + f"screen_record{time.time()}.avi"

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 60.0  # Set the desired FPS
frame_delay = 1.0 / fps  # Time delay between frames to control FPS

# Create the video writer object
out = cv2.VideoWriter(output, fourcc, fps, SCREEN_SIZE)

# Duration of recording (in seconds)
record_seconds = 20

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": SCREEN_SIZE[0], "height": SCREEN_SIZE[1]}
    
    print("Recording started...")
    start_time = time.time()
    last_frame_time = time.time()

    while time.time() - start_time < record_seconds:
   
        
        # Calculate elapsed time since the last frame
        elapsed_time = time.time() - last_frame_time
        
      
        if elapsed_time >= frame_delay:
            # Capture the screen
            img = sct.grab(monitor)
            # Convert the screenshot to a NumPy array
            frame = np.array(img)
            # Convert BGRA to BGR (OpenCV format)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            out.write(frame)
        # Write the frame to the video file
          # If the time elapsed is less than the desired frame delay, wait
        #if elapsed_time < frame_delay:
        #    time.sleep(frame_delay - elapsed_time)  # Sleep for the remaining time to control FPS
        #out.write(frame)
        
        # Update the time of the last frame
        last_frame_time = time.time()

# Release the VideoWriter object
out.release()


stretch_video(output, output, record_seconds)
print(f"Recording saved to {output}")
