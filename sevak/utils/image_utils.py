# Objective : To give useful functions for image manipulation or processing: 

import cv2
import json
import numpy as np

class ImageUtils:
    # Image Manipulation algos
    # Takes jpg_bytes and returns decoded bytes : np.ndarray
    def jpg2bgr(self, jpg_bytes):
        frame = np.frombuffer(jpg_bytes, dtype = np.unint8)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        return frame
    
    def jpg2rbg(self, jpg_bytes):
        frame = self.jpg2bgr(jpg_bytes)
        # Convert color
        return self.bgr2rgb(frame)

    # Change colors (bgr <=> rbg)
    def rgb2bgr(self, rgb_array):
        return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    
    def bgr2rgb(self, bgr_array):
        return cv2.cvtColor(bgr_array, cv2.COLOR_BGR2RGB)






