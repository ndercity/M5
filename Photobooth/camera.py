import cv2

class Camera:
    def __init__(self):
        self.capture = None
        self.image_container = []
        self.temp_image = None #dito muna ilalagay yung pic na waiting for confirmation

    def start(self):
        """ Start the webcam feed if not already running """
        if self.capture is None or not self.capture.isOpened():
            self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 is the default webcam gagawing 1 ito para sa webcam
    
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
    
    def capture_frame(self):
        if self.capture is None or not self.capture.isOpened():
            self.start()
        
        ret, frame = self.capture.read()
        if not ret:
            return None
        
        self.image_container.append(frame)

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            return None
        
        print("current num of images: ", len(self.image_container))
        return jpeg.tobytes()
    
    def delete_image(self): #this will ignore the image that is newly taken, this is for recapuring image
        if(len(self.image_container) > 0):
            self.image_container.pop(len(self.image_container) - 1)
            print("current num of images: ", len(self.image_container))
        else:
            print("no element in the array/list")



