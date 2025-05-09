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
    #look for a way to create a face box and at the same time crop the image
    def get_image_sticker(self, image):
        if image:
            processed_image = np.frombuffer(image.read(), np.uint8)
            processed_image = cv2.imdecode(processed_image, cv2.IMREAD_COLOR)
            self.raw_image = processed_image.copy()

            image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            results = self.face_detection.process(image_rgb)

            if results.detections:
                for detection in results.detections:
                    bounding_box = detection.location_data.relative_bounding_box
                    ih, iw, _ = processed_image.shape
                    xmin = int(bounding_box.xmin * iw)
                    ymin = int(bounding_box.ymin * ih)
                    width = int(bounding_box.width * iw)
                    height = int(bounding_box.height * ih)

                    # Expand the box
                    padding_top = int(0.2 * height)
                    padding_sides = int(0.2 * width)
                    padding_bottom = int(0.1 * height)

                    x = max(0, xmin - padding_sides)
                    y = max(0, ymin - padding_top)
                    x2 = min(iw, xmin + width + padding_sides)
                    y2 = min(ih, ymin + height + padding_bottom)

                    w = x2 - x
                    h = y2 - y

                    if w > 0 and h > 0:
                        cropped_face = processed_image[y:y+h, x:x+w]
                        self.cropped_faces.append(cropped_face)
                        self.face_boxes.append({'x': x, 'y': y, 'w': w, 'h': h})            
                _, self.buffer_image = cv2.imencode('.jpg', processed_image)
            else:
                print("No faces detected")
            '''
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

                _, self.buffer_image = cv2.imencode('.jpg', processed_image)
                '''
           
        else:
            print("No image provided")

    #scans the whole face and saves all the landmark associated to the face
    def get_all_target_landmarks(self):
        if self.face_index == -1:
            print("Invalid face index")
            return
        
        cropped_img = self.cropped_faces[self.face_index]
        img_rgb = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
        crop_result = self.face_mesh_images.process(img_rgb)

        if crop_result.multi_face_landmarks:
            for crop_landmarks in crop_result.multi_face_landmarks:
                ih,iw,_ = cropped_img.shape
                print(ih, iw)
                for name, idx in self.face_landmarks.items():
                    self.target_landmarks[name] = (
                        int(crop_landmarks.landmark[idx].x * iw),
                        int(crop_landmarks.landmark[idx].y * ih)
                    )

    #ibabato nito laaht ng mukhang available sa image at ang kanilang bouding boxes
    def set_face_boxes(self):
        return self.face_boxes, self.buffer_image
    
    def set_face_index(self, index, sticker_type):
        self.face_index = int(index)
        path = None

        self.get_all_target_landmarks()
        #print(self.target_landmarks)
        self.size_test()

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

                self.src_points = [[47, 110], [100, 60], [153, 110]] # ponts starting from left to right depending on the sticker
                self.dest_points = [mustache_l, mustache_c, mustache_r]

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
        warped_image = cv2.merge([warped_rgb[:, :, 0], warped_rgb[:, :, 1], warped_rgb[:, :, 2], warped_alpha])

        _,sticker = cv2.imencode('.png', warped_image)

        return sticker


    def get_overlay_bounding_box(self):
        box = self.face_boxes[self.face_index]  # face_index is the index of the face you want
        x1 = box['x']
        y1 = box['y']
        x2 = box['w']
        y2 = box['h']

        return x1,y1,x2,y2

    def size_test(self):
        h1, w1, _1 = self.raw_image.shape
        print("Raw Pic Width:", w1, "Raw Pic Height:", h1) #expected result must be 640x480

        box = self.face_boxes[self.face_index]  # face_index is the index of the face you want
        x1 = box['x']
        y1 = box['y']
        x2 = box['w']
        y2 = box['h']

        print("all points: ", x1,x2,y1,y2)

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
