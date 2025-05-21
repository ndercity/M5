import cv2
import numpy as np
from threading import Thread

class Camera:
    def __init__(self):
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            raise Exception("Could not open video device")
        
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        self.grabbed, self.frame = self.capture.read()
        self.stopped = False
        self.thread = None

    def start(self):
        """Start the thread to read frames"""
        if self.thread is None:
            self.thread = Thread(target=self.update, daemon=True)
            self.thread.start()
        return self

    def update(self):
        """Background thread function to keep reading frames"""
        while not self.stopped:
            self.grabbed, self.frame = self.capture.read()

    def read(self):
        """Return the most recently read frame"""
        return self.frame

    def get_frame(self):
        """Return the frame as JPEG bytes for streaming"""
        if self.frame is not None:
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        return None

    def capture_snapshot(self):
        """Capture a still image"""
        if self.frame is not None:
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        return None

    def stop(self):
        """Stop the video stream thread and release resources"""
        self.stopped = True
        if self.thread is not None:
            self.thread.join()
        if self.capture:
            self.capture.release()
