import cv2
import threading
import time

class Camera:
    def __init__(self):
        self.capture = None
        self.frame = None
        self.active_stream = False
        self.thread = None
        self.lock = threading.Lock()
        self.stopped = False

    def start(self):
        if self.capture is None or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
            self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            self.active_stream = True
            self.stopped = False

            self.thread = threading.Thread(target=self._update_frame, daemon=True)
            self.thread.start()

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()
            self.thread = None

        if self.capture and self.capture.isOpened():
            self.capture.release()
            self.capture = None
            self.active_stream = False

    def is_active(self):
        return self.active_stream

    def _update_frame(self):
        while not self.stopped:
            if self.capture:
                ret, frame = self.capture.read()
                if not ret:
                    continue
                with self.lock:
                    self.frame = frame
            time.sleep(0.01)  # Small delay to prevent 100% CPU usage

    def get_frame(self):
        with self.lock:
            if self.frame is None:
                return None
            ret, jpeg = cv2.imencode('.jpg', self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            return jpeg.tobytes()

    def capture_snapshot(self):
        return self.get_frame()
