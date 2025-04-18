import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.capture = None

    def start(self):
        """Start the webcam feed"""
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            raise Exception("Could not open video device")

    def stop(self):
        """Stop the webcam feed"""
        if self.capture:
            self.capture.release()

    def get_frame(self):
        """Get a frame from the webcam as JPEG byte data"""
        if self.capture:
            ret, frame = self.capture.read()
            if not ret:
                return None
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None

    def capture_snapshot(self):
        """Capture a snapshot (single frame) from the webcam"""
        if self.capture:
            ret, frame = self.capture.read()
            if not ret:
                return None
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None