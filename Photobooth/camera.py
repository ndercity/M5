import cv2
import numpy as np

class Camera:
    def __init__(self):
        self.capture = None
        self.active_stream = False

    #SET THE NATIVE CAM RESO
    def start(self):
        if self.capture is None or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            self.active_stream = True

    def stop(self):
        if self.capture and self.capture.isOpened():
            self.capture.release()
            self.capture = None
            self.active_stream = False

    def is_active(self):
        return self.active_stream

    #SET THE TARGET RESO MUST BE ROUNDED UP OR DOWN OR ELSE MAY ERROR (INTEGER ONLY)
    def get_frame(self, target_width=853, target_height=480):
        if self.capture:
            ret, frame = self.capture.read()
            if not ret:
                return None

            frame = self._crop_and_resize_to_custom_16_9(frame, target_width, target_height)

            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None

    #SET THE TARGET RESO MUST BE ROUNDED UP OR DOWN OR ELSE MAY ERROR (INTEGER ONLY)
    def capture_snapshot(self, target_width=853, target_height=480):
        """Capture a snapshot with custom 16:9 resolution."""
        return self.get_frame(target_width, target_height)

    def _crop_and_resize_to_custom_16_9(self, frame, target_width, target_height):
        height, width, _ = frame.shape
        target_aspect = 16 / 9

        # Calculate crop dimensions maintaining 16:9 inside original frame
        crop_height = int(width / target_aspect)
        crop_width = width

        if crop_height > height:
            crop_height = height
            crop_width = int(height * target_aspect)

        # Calculate top-left corner for center crop
        x_start = (width - crop_width) // 2
        y_start = (height - crop_height) // 2

        cropped = frame[y_start:y_start + crop_height, x_start:x_start + crop_width]

        # Resize cropped image to target resolution
        resized = cv2.resize(cropped, (target_width, target_height), interpolation=cv2.INTER_AREA)

        return resized
