import cv2

class Camera:
    def __init__(self):
        self.capture = None

    def start(self):
        """ Start the webcam feed if not already running """
        if self.capture is None or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0)  # 0 is the default webcam
            if not self.capture.isOpened():
                raise Exception("Could not open video device")

    def stop(self):
        """ Stop the webcam feed """
        if self.capture and self.capture.isOpened():
            self.capture.release()
            self.capture = None  # Set to None to indicate it's stopped

    def get_frame(self):
        """ Get a frame from the webcam """
        if self.capture is None or not self.capture.isOpened():
            self.start()  # Start the camera if it's not running

        ret, frame = self.capture.read()
        if not ret:
            return None
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
