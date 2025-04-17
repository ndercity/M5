import mediapipe as mp
import cv2
from PIL import Image


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