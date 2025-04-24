import mediapipe as mp
import cv2
import numpy as np


'''
must store the landmark of the face/s for the stickers
must declare all the landmarks to be used and the faces of the users
hardcode mo yung sticker locations
'''

class Sticker_Filter:
    def __init__(self):

        self.face_mesh = mp.solutions.face_mesh
        self.face_mesh_images = self.face_mesh.FaceMesh(static_image_mode = True, max_num_faces=5, min_detection_confidence=0.5) #hypotetical ang 5
        self.drawing = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles

        #test declarations
        self.face_landmark = mp.solutions.face_detection
        self.face_detection = self.face_landmark.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        self.raw_image = None
        self.face_boxes = []
        self.buffer_image = None

        self.face_landmarks = {
            "left_eye_center": 468,
            "right_eye_center": 473,
            "left_cheek": 234,
            "right_cheek": 454,
            "center_lips": 13,
            "center_chin": 152,
            "center_forehead": 10,
            "center_nose": 1
        }
    #tawagin muna ito para mapagana yung buong class
    #100% pure test pa lang ito
    def get_image_sticker(self, image):
        if image:
            processed_image = np.frombuffer(image.read(), np.uint8)
            processed_image = cv2.imdecode(processed_image, cv2.IMREAD_COLOR)

            image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(image_rgb)

            if results.detections:
                for detection in results.detections:
                    bounding_box = detection.location_data.relative_bounding_box
                    ih, iw, _ = processed_image.shape
                    x = int(bounding_box.xmin * iw)
                    y = int(bounding_box.ymin * ih)
                    w = int(bounding_box.width * iw)
                    h = int(bounding_box.height * ih)
                    self.face_boxes.append({'x': x, 'y': y, 'w': w, 'h': h})
                    cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            _, self.buffer_image = cv2.imencode('.jpg', processed_image)
        else:
            print("no image found")

    #ibabato nito laaht ng mukhang available sa image at ang kanilang bouding boxes
    def set_face_boxes(self):
        return self.face_boxes, self.buffer_image
    
    #must call this para safe ass shit
    def clear_all(self):
        if self.buffer_image is not None:
            self.face_boxes = []
            self.buffer_image = None
            print("boxes cleared")
        else:
            print("nothing to clear here")
