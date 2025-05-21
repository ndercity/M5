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
        self.target_landmarks = {} 

        self.face_index = -1
        self.sticker_type_path = None
        self.raw_image = None
        self.buffer_image = None

        # Landmark indexes
        self.face_landmarks = {
            #for mustache
            "mustache_center": 164,
            "left_mustache": 410,
            "right_mustache": 186,

            #for swag glasses
            "upper_nasal_bone": 168, #might change this to 8
            "lower_left_eyes":230,
            "lower_right_eyes":450,

            #for puppy glasses
            "upper_left_eye": 223,
            "upper_right_eye": 443,
            "left_forehead": 67,
            "right_forehead":297,

            #dog
            "center_nose":1,

            #blue crown
            "center_forehead": 10,
            "left_midline_forehead":104,
            "right_midline_forehead":333,

            #rat
            "upper_center_nose": 5,
            "left_lips": 216,
            "right_lips": 436,

            #anime eyes
            "lower_left_eyebrows": 46,
            "lower_right_eyebrows": 276,

            #bunny
            "upper_right_forehead": 103,
            "upper_left_forehead": 332,

            #neon glasses
            "between_eyebrows": 8,

            #zoro
            "mid_left_eye": 23,
            "mid_right_eye": 253
        }

    #tawagin muna ito para mapagana yung buong class
    #100% pure test pa lang ito
    #look for a way to create a face box and at the same time crop the image
    def get_image_sticker(self, image):
        if image:
            processed_image = np.frombuffer(image.read(), np.uint8)
            processed_image = cv2.imdecode(processed_image, cv2.IMREAD_COLOR)
            self.raw_image = processed_image.copy()

            height, width = self.raw_image.shape[:2]
            print(f"Width: {width}, Height: {height}")

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
           
        else:
            print("No image provided")

    #scans the whole face and saves all the landmark associated to the face position para mamaya
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
        match sticker_type:
            case "blue_crown":
                path = "static/stickers/blue_crown.png"
                crown_c = self.target_landmarks["center_forehead"]
                crown_r = self.target_landmarks["right_midline_forehead"]
                crown_l = self.target_landmarks["left_midline_forehead"]

                self.src_points = [[23,352], [381,121], [724, 352]] # ponts starting from left to right depending on the sticker
                self.dest_points = [crown_l, crown_c, crown_r]

            case "mustache":
                path = "static/stickers/mustache.png"
                mustache_c = self.target_landmarks["mustache_center"]
                mustache_r = self.target_landmarks["right_mustache"]
                mustache_l = self.target_landmarks["left_mustache"]

                self.src_points = [[47, 110], [100, 60], [153, 110]] # ponts starting from left to right depending on the sticker
                self.dest_points = [mustache_l, mustache_c, mustache_r]

            case "puppy": 
                path = "static/stickers/puppy.png"
               
                puppy_center = self.target_landmarks["center_forehead"]
                puppy_lower_left_eye = self.target_landmarks["lower_left_eyes"]
                puppy_lower_right_eye = self.target_landmarks["lower_right_eyes"]

                self.src_points = [[62,178],[100,39],[144,176]] # ponts starting from left to right depending on the sticker
                self.dest_points = [puppy_lower_left_eye, puppy_center, puppy_lower_right_eye]

            case "rat":
                path = "static/stickers/rat.png"

                rat_center = self.target_landmarks["upper_center_nose"]
                rat_left = self.target_landmarks["left_lips"]
                rat_right = self.target_landmarks["right_lips"]

                self.src_points = [[93,172], [149,119], [207,172]]
                self.dest_points = [rat_left, rat_center, rat_right] #left to right again 

            case "swag":
                path = "static/stickers/swag.png"
                swag_center = self.target_landmarks["upper_nasal_bone"]
                swag_left = self.target_landmarks["lower_left_eyes"]
                swag_right = self.target_landmarks["lower_right_eyes"]

                self.src_points = [[50,39], [101,4], [153,31]]
                self.dest_points = [swag_left, swag_center, swag_right] #left to right again 

            case "anime_eyes":
                path = "static/stickers/anime_eyes.png"
                aeyes_center = self.target_landmarks["center_nose"]
                aeyes_right = self.target_landmarks["lower_right_eyebrows"]
                aeyes_left = self.target_landmarks["lower_left_eyebrows"]

                self.src_points = [[276,440], [497,644], [740,440]]
                self.dest_points = [aeyes_left, aeyes_center, aeyes_right] #left to right again 

            case "enderman":
                path = "static/stickers/enderman.png"

                enderman_center = self.target_landmarks["center_forehead"]
                enderman_left = self.target_landmarks["left_lips"]
                enderman_right = self.target_landmarks["right_lips"]

                self.src_points = [[264, 700], [512,140], [768,700]]
                self.dest_points = [enderman_left, enderman_center, enderman_right] #left to right again 

            case "steve":
                path = "static/stickers/steve.png"

                zombie_center = self.target_landmarks["center_forehead"]
                zombie_left = self.target_landmarks["left_lips"]
                zombie_right = self.target_landmarks["right_lips"]

                self.src_points = [[264, 700], [512,140], [768,700]]
                self.dest_points = [zombie_left, zombie_center, zombie_right] #left to right again 

            case "zombie":
                path = "static/stickers/zombie.png"

                zombie_center = self.target_landmarks["center_forehead"]
                zombie_left = self.target_landmarks["left_lips"]
                zombie_right = self.target_landmarks["right_lips"]

                self.src_points = [[264, 700], [512,140], [768,700]]
                self.dest_points = [zombie_left, zombie_center, zombie_right] #left to right again 

            case "neon_glasses":
                path = "static/stickers/neon_glasses.png"

                nglasses_center = self.target_landmarks["between_eyebrows"]
                nglasses_left = self.target_landmarks["lower_left_eyes"]
                nglasses_right = self.target_landmarks["lower_right_eyes"]

                self.src_points = [[152,185], [293,89], [434,185]]
                self.dest_points = [nglasses_left, nglasses_center, nglasses_right] #left to right again 

            case "roblox_face":
                path = "static/stickers/roblox_face.png"

                roblox_center = self.target_landmarks["center_forehead"]
                roblox_left = self.target_landmarks["left_lips"]
                roblox_right = self.target_landmarks["right_lips"]

                self.src_points = [[264, 700], [512,140], [768,700]]
                self.dest_points = [roblox_left, roblox_center, roblox_right] #left to right again 

            case "pink_cat":
                path = "static/stickers/pink_cat.png"
                pink_center = self.target_landmarks["center_nose"]
                pink_left = self.target_landmarks["left_forehead"]
                pink_right = self.target_landmarks["right_forehead"]

                self.src_points = [[161,141], [276,410], [390,141]]
                self.dest_points = [pink_left, pink_center, pink_right] #left to right again 

            case "superhero_mask":
                path = "static/stickers/superhero_mask.png"
                superhero_center = self.target_landmarks["center_forehead"]
                superhero_left = self.target_landmarks["lower_left_eyes"]
                superhero_right = self.target_landmarks["lower_right_eyes"]

                self.src_points = [[146,494], [301,66], [456,494]]
                self.dest_points = [superhero_left, superhero_center, superhero_right] #left to right again 

            case "tiara":
                path = "static/stickers/tiara.png"
                tiara_center = self.target_landmarks["center_forehead"]
                tiara_left = self.target_landmarks["upper_left_forehead"]
                tiara_right = self.target_landmarks["upper_right_forehead"]

                self.src_points = [[2,322], [276,262], [550, 322]]
                self.dest_points = [tiara_left, tiara_center, tiara_right] #left to right again 

            case "zoro":
                path = "static/stickers/zoro.png"

                zoro_center = self.target_landmarks["between_eyebrows"]
                zoro_left = self.target_landmarks["mid_left_eye"]
                zoro_right = self.target_landmarks["mid_right_eye"]

                self.src_points = [[177,182], [304,30], [436,182]]
                self.dest_points = [zoro_left, zoro_center, zoro_right] #left to right again 

            case default:
                print("sticker doesn't exist")
        self.sticker_type_path = path

        print(index, sticker_type)
        # rat_center = self.target_landmarks[""]
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
        warped_image = cv2.merge([warped_rgb[:, :, 0], warped_rgb[:, :, 1], warped_rgb[:, :, 2], warped_alpha])

        _,sticker = cv2.imencode('.png', warped_image)

        return sticker


    def get_overlay_bounding_box(self):
        box = self.face_boxes[self.face_index] 
        x1 = box['x']
        y1 = box['y']
        x2 = box['w']
        y2 = box['h']

        return x1,y1,x2,y2

    #must call this para safe ass shit
    def clear_all(self):
        if self.buffer_image is not None:
            self.face_boxes = []
            self.cropped_faces = []
            self.dest_points = []
            self.src_points = []
            self.target_landmarks = {}

            self.face_index = -1
            self.sticker_type_path = None
            self.raw_image = None
            self.buffer_image = None
            print("boxes cleared")
        else:
            print("nothing to clear here")
