import cv2 as cv
from time import time
from statistics import mean
cap_times = []
feed = cv.VideoCapture(0)
for i in range(300):
    loop_start = time()
    _, frame = feed.read()
    elapsed = time() - loop_start
    cap_times.append(elapsed)
average = mean(cap_times)
fps = 1/average
print(f'Avg cap time: {average}')
print(f'FPS: {fps}')