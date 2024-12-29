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
fps = 60.0
out = cv2.VideoWriter(output, fourcc, fps, SCREEN_SIZE)

# Duration of recording (in seconds)
record_seconds = 10

with mss.mss() as sct:
    monitor = {"top": 0, "left": 0, "width": SCREEN_SIZE[0], "height": SCREEN_SIZE[1]}
    
    print("Recording started...")
    start_time = time.time()
    while time.time() - start_time < record_seconds:
        # Capture the screen
        img = sct.grab(monitor)
        # Convert to a NumPy array
        frame = np.array(img)
        # Convert BGRA to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        # Write the frame
        out.write(frame)

# Release the VideoWriter
out.release()
print(f"Recording saved to {output}")
