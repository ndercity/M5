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

        #crucial for the fucking mesh
        self.face_mesh = mp.solutions.face_mesh
        self.face_mesh_images = self.face_mesh.FaceMesh(static_image_mode = True, 
                                                        max_num_faces=5, 
                                                        min_detection_confidence=0.5, #hypotetical ang 5
                                                        refine_landmarks=True) #turn this to false kapag naglag sa raspi
        self.drawing = mp.solutions.drawing_utils
        self.drawing_styles = mp.solutions.drawing_styles
        self.face_landmark = mp.solutions.face_detection
        self.face_detection = self.face_landmark.FaceDetection(model_selection=0, min_detection_confidence=0.5)

        self.raw_image = None
        self.buffer_image = None
        self.face_boxes = []
        self.cropped_faces = []

        self.target_landmarks = {}
        self.face_index = -1
        self.sticker_type_path = None
        self.dest_points = []
        self.src_points = []

        # Landmark indexes
        self.face_landmarks = {
            "left_eye_center": 468, #might remove this
            "right_eye_center": 473, #might remove this
            "left_cheek": 234,
            "right_cheek": 454,
            "center_lips": 13,
            "center_chin": 152,
            "center_forehead": 10,
            "center_nose": 1,
            "mustache_center": 164,
            "left_mustache": 410,
            "right_mustache": 186
        }

    #tawagin muna ito para mapagana yung buong class
    #100% pure test pa lang ito
    def get_image_sticker(self, image):
        if image:
            processed_image = np.frombuffer(image.read(), np.uint8)
            processed_image = cv2.imdecode(processed_image, cv2.IMREAD_COLOR)
            self.raw_image = processed_image.copy()

            image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh_images.process(image_rgb)

            self.face_boxes = []
            self.multi_face_landmarks = []

            if results.multi_face_landmarks:
                ih, iw, _ = processed_image.shape
                for landmarks in results.multi_face_landmarks:
                    self.multi_face_landmarks.append(landmarks)

                    x = int(landmarks.landmark[234].x * iw)
                    y = int(landmarks.landmark[10].y * ih)
                    w = int(landmarks.landmark[454].x * iw)
                    h = int(landmarks.landmark[152].y * ih)

                    self.face_boxes.append({'x': x, 'y': y, 'w': w, 'h': h})
                    cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                _, self.buffer_image = cv2.imencode('.jpg', processed_image)
            else:
                print("No faces detected")
        else:
            print("No image provided")

    def get_all_target_landmarks(self):
        if self.face_index == -1:
            print("Invalid face index")
            return

        face_landmarks = self.multi_face_landmarks[int(self.face_index)]
        ih, iw, _ = self.raw_image.shape

        #self.target_landmarks = {} #duplication prbably the problem
        for name, idx in self.face_landmarks.items():
            x = int(face_landmarks.landmark[idx].x * iw)
            y = int(face_landmarks.landmark[idx].y * ih)
            self.target_landmarks[name] = (x, y)


    #ibabato nito laaht ng mukhang available sa image at ang kanilang bouding boxes
    def set_face_boxes(self):
        return self.face_boxes, self.buffer_image
    
    def set_face_index(self, index, sticker_type):
        self.face_index = index
        path = None

        self.get_all_target_landmarks()
        print(self.target_landmarks)

        match sticker_type:
            case "AoA":
                path = "static/stickers/AoA.png"
            case "blue_crown":
                path = "static/stickers/blue_crown.png"
            case "DoD":
                path = "static/stickers/DoD.png"
            case "dog":
                path = "static/stickers/dog.png"
            case "EoE":
                path = "static/stickers/EoE.png"
            case "IoI":
                path = "static/stickers/IoI.png"
            case "mustache":
                path = "static/stickers/mustache.png"
                mustache_c = self.target_landmarks["mustache_center"]
                mustache_r = self.target_landmarks["right_mustache"]
                mustache_l = self.target_landmarks["left_mustache"]

                self.src_points = [[177, 99],[277, 41], [385, 99]] # ponts starting from left to right depending on the sticker
                self.dest_points = [mustache_c, mustache_r, mustache_l]

            case "OoO":
                path = "static/stickers/OoO.png"
            case "puppy":
                path = "static/stickers/puppy.png"
            case "rat":
                path = "static/stickers/rat.png"
            case "swag":
                path = "static/stickers/swag.png"
            case "UoU":
                path = "static/stickers/UoU.png"
            case default:
                print("sticker doesn't exist")
        self.sticker_type_path = path

        print(index, sticker_type)

    def warp_image(self):

        if not self.sticker_type_path or not self.src_points or not self.dest_points:
            print("Sticker path or points missing")
            return None

        sticker = cv2.imread(self.sticker_type_path, cv2.IMREAD_UNCHANGED)
        h, w, _ = self.raw_image.shape
        
        # Transparent canvas
        overlay = np.zeros((h, w, 4), dtype=np.uint8)

        src = np.float32(self.src_points)
        dst = np.float32(self.dest_points)

        M = cv2.getAffineTransform(src, dst)

        warped = cv2.warpAffine(sticker, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT)

        if warped.shape[2] == 4:
            alpha_s = warped[:, :, 3] / 255.0
            for c in range(3):  # Only BGR channels
                overlay[:, :, c] = (warped[:, :, c] * alpha_s).astype(np.uint8)
            overlay[:, :, 3] = warped[:, :, 3]  # Copy alpha channel

        return overlay
    
    def get_overlay_bounding_box(self, overlay):
        """Returns the bounding box (x, y, width, height) of the non-transparent area of the overlay"""
        if overlay is None or overlay.shape[2] != 4:
            return None

        alpha = overlay[:, :, 3]  # Get alpha channel
        coords = cv2.findNonZero((alpha > 0).astype(np.uint8))

        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)

            print("Bounding box:", x, y, w, h)

            return x, y, w, h
        return None

    
    #must call this para safe ass shit
    def clear_all(self):
        if self.buffer_image is not None:
            self.face_boxes = []
            self.buffer_image = None
            print("boxes cleared")
        else:
            print("nothing to clear here")
