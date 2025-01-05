import cv2
import numpy as np
import mss
import time

# Screen resolution (adjust to your screen size)
SCREEN_SIZE = (1920, 1080)  # Replace with your screen resolution

# Output file
output = f"screen_record{time.time()}.avi"

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = 60.0  # Set the desired FPS
frame_delay = 1.0 / fps  # Time delay between frames to control FPS

# Create the video writer object
out = cv2.VideoWriter("../saves/" + output, fourcc, fps, SCREEN_SIZE)

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
print(f"Recording saved to {output}")
