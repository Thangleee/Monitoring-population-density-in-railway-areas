import numpy as np
import cv2

def get_roi():
    return np.array([
        (854, 512),
        (1071, 508),
        (1416, 803),
        (285, 760)
    ], np.int32)

def draw_roi(frame, roi):
    cv2.polylines(frame, [roi], True, (0, 255, 255), 2)

#def draw_line(frame):
    #cv2.line(frame, (400, 300), (1400, 300), (0, 0, 255), 2)
