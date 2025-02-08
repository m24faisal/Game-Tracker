import cv2
import numpy as np
import mss
import time
import subprocess
import os

def stretch_video(input_file, output_file, target_duration):
    """
    Stretches a video to a fixed length using FFmpeg.
    """
    try:
        # Resolve absolute paths
        input_file = os.path.abspath(input_file)
        output_file = os.path.abspath(output_file)

        # Check if input file exists
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file '{input_file}' not found.")
        
        # Get the original duration of the video using FFprobe
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
        
        if result.returncode != 0:
            raise RuntimeError(f"FFprobe error: {result.stderr}")
        
        # The main issue here is that FFMPEG does not recognize the fact that a screen recording is happening.
        # @TODO: Fix this issue
        original_duration = result.stdout.strip()
        # original_duration = float(result.stdout.strip())
        print(f"Original video duration: {original_duration} seconds.")
        
        # Calculate the stretch factor
        stretch_factor = target_duration / original_duration

        # Check valid stretch factor
        if stretch_factor <= 0:
            raise ValueError("Target duration must be greater than 0.")

        # Run the FFmpeg command
        command = [
            "ffmpeg",
            "-i", input_file,
            "-vf", f"setpts={1/stretch_factor}*PTS",
            "-af", f"atempo={stretch_factor}",
            output_file
        ]
        print(f"Running command: {' '.join(command)}")  # Debugging output
        subprocess.run(command, check=True)
        
        # Check if output file was created
        if not os.path.exists(output_file):
            raise RuntimeError("FFmpeg failed to create the output file.")
        
        print(f"Video successfully stretched to {target_duration} seconds.")
        return True
    
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
record_seconds = 5

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


"""
# Configurable parameters
RECORD_OUTPUT = "../saves/" + f"record_temp_{time.time()}.mp4"
FINAL_OUTPUT = "../saves/" + f"output_{time.time()}.mp4"
DURATION = 60  # seconds
FPS_TARGET = 60  # Frames per second

def record_screen(output_file, duration, fps):
    screen_recorder = mss.mss()
    monitor = screen_recorder.monitors[1]  # Capture primary screen

    width, height = monitor["width"], monitor["height"]
    
    # Use imageio to write video (imageio-ffmpeg handles encoding)
    writer = imageio.get_writer(output_file, fps=fps, codec="libx264")

    print(f"Recording {duration} seconds at {fps} FPS...")
    start_time = time.time()

    while (time.time() - start_time) < duration:
        frame_start = time.time()
        
        # Capture screen
        screenshot = screen_recorder.grab(monitor)
        frame = np.array(screenshot)[:, :, :3]  # Convert BGRA to RGB

        # Write frame to video
        writer.append_data(frame)

        # Maintain FPS
        elapsed = time.time() - frame_start
        #time.sleep(max(0, (1 / fps) - elapsed))

    writer.close()
    print(f"Recording saved as {output_file}")


def get_video_fps(input_file):
    try:
        # Run FFprobe to get FPS information
        cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", 
            "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", input_file
        ]
        result = subprocess.check_output(cmd)
        
        # FFprobe gives the frame rate as num/den (e.g., 30000/1001)
        frame_rate = result.decode().strip()
        
        # Handle "num/den" frame rates like "30000/1001" and calculate FPS
        num, den = map(int, frame_rate.split('/'))
        fps = num / den
        
        return fps

    except subprocess.CalledProcessError as e:
        print(f"Error retrieving FPS: {e.stderr.decode()}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def correct_video_duration(input_file, output_file, target_duration):
    try:
        # Get the video duration using ffprobe
        cmd_probe = [
            "ffprobe", "-v", "error", "-select_streams", "v:0", 
            "-show_entries", "stream=duration", "-of", "default=noprint_wrappers=1:nokey=1", input_file
        ]
        #original_duration = float(subprocess.check_output(cmd_probe).decode().strip())
        original_duration = get_video_fps(input_file)
        print("original", original_duration)
        # If no audio stream, we don't set audio options
        cmd = [
            "ffmpeg", "-i", input_file, 
            "-filter:v", f"setpts={(original_duration / target_duration)}*PTS",  # Adjust video speed
            "-c:v", "libx264", "-r", "30", "-y", output_file
        ]

        # Check if the file has an audio stream
        cmd_check_audio = [
            "ffprobe", "-v", "error", "-select_streams", "a", 
            "-show_entries", "stream=codec_type", "-of", "csv=p=0", input_file
        ]
        audio_streams = subprocess.check_output(cmd_check_audio).decode().strip()

        if audio_streams:  # If there are audio streams, we need to handle them too
            cmd.extend(["-c:a", "aac", "-b:a", "128k"])

        subprocess.run(cmd, check=True)
        print(f"Video saved as {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

# Run the screen recorder
#record_screen(RECORD_OUTPUT, DURATION, FPS_TARGET)
#time.sleep(10)
#correct_video_duration(RECORD_OUTPUT, FINAL_OUTPUT, DURATION)


#import subprocess
"""