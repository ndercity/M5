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

        self.face_boxes = []
        self.cropped_faces = []
        self.dest_points = []
        self.src_points = []
        self.face_origin = [] #dito ilalagay ang starting point ng cropped image it will contain x and y
        self.target_landmarks = {}

        self.face_index = -1
        self.sticker_type_path = None
        self.raw_image = None
        self.buffer_image = None

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

            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    ih, iw, _ = processed_image.shape

                    x1 = int(landmarks.landmark[234].x * iw) - 10
                    y1 = int(landmarks.landmark[10].y * ih) - 10
                    x2 = int(landmarks.landmark[454].x * iw) + 10
                    y2 = int(landmarks.landmark[152].y * ih) + 10

                    w = x2 - x1
                    h = y2 - y1

                    self.face_boxes.append({'x': x1, 'y': y1, 'w': w, 'h': h})
                    self.face_origin.append({'x': x1, 'y': y1})
                    self.cropped_faces.append(processed_image[y1:y2, x1:x2])                    
                    #cv2.rectangle(processed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                _, self.buffer_image = cv2.imencode('.jpg', processed_image)
            else:
                print("No faces detected")
        else:
            print("No image provided")

    #scans the whole face and saves all the landmark associated to the face
    def get_all_target_landmarks(self):
        if self.face_index == -1:
            print("Invalid face index")
            return
        
        img = self.cropped_faces[self.face_index]
        crop_result = self.face_mesh_images.process(img)

        if crop_result.multi_face_landmarks:
            for crop_landmarks in crop_result.multi_face_landmarks:
                ih,iw,_ = img.shape
                for name, idx in self.face_landmarks.items():
                    self.target_landmarks[name] = (
                        int(crop_landmarks.landmark[idx].x * iw),
                        int(crop_landmarks.landmark[idx].y * ih)
                    )
    '''
        face_landmarks = self.multi_face_landmarks[int(self.face_index)]
        ih, iw, _ = self.raw_image.shape

        #self.target_landmarks = {} #duplication prbably the problem
        for name, idx in self.face_landmarks.items():
            x = int(face_landmarks.landmark[idx].x * iw)
            y = int(face_landmarks.landmark[idx].y * ih)
            self.target_landmarks[name] = (x, y)
    '''

    #ibabato nito laaht ng mukhang available sa image at ang kanilang bouding boxes
    def set_face_boxes(self):
        return self.face_boxes, self.buffer_image
    
    def set_face_index(self, index, sticker_type):
        self.face_index = int(index)
        path = None

        self.get_all_target_landmarks()
        #print(self.target_landmarks)
        #self.size_test()

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

        c_img = self.cropped_faces[self.face_index]
        sticker = cv2.imread(self.sticker_type_path, cv2.IMREAD_UNCHANGED)

        src = np.float32(self.src_points)
        dst = np.float32(self.dest_points)

        M = cv2.getAffineTransform(src, dst)

        sticker_rgb = sticker[:, :, :3]
        sticker_alpha = sticker[:, :, 3]

        warped_rgb = cv2.warpAffine(sticker_rgb, M, (c_img.shape[1], c_img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0))
        warped_alpha = cv2.warpAffine(sticker_alpha, M, (c_img.shape[1], c_img.shape[0]), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

        alpha_mask = warped_alpha / 255.0
        alpha_inv = 1.0 - alpha_mask

        '''
        #di ko alam kung kailangan ito
        for c in range(3):
            c_img[:, :, c] = (alpha_mask * warped_rgb[:, :, c] + alpha_inv * img[:, :, c])
        '''

        _,sticker = cv2.imencode('.png', warped_rgb)

        return sticker


    def get_overlay_bounding_box(self):
        return self.face_boxes[self.face_index]

    def size_test(self):
        h, w, _ = self.raw_image.shape
        print("Width:", w, "Height:", h) #expected result must be 640x480

    
    #must call this para safe ass shit
    def clear_all(self):
        if self.buffer_image is not None:
            self.face_boxes = []
            self.cropped_faces = []
            self.dest_points = []
            self.src_points = []
            self.face_origin = []
            self.target_landmarks = {}

            self.face_index = -1
            self.sticker_type_path = None
            self.raw_image = None
            self.buffer_image = None
            print("boxes cleared")
        else:
            print("nothing to clear here")
