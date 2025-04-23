import cv2
import numpy as np

'''
Images cannot have 2 or more filter applied to itself

Mga filter na gagawin
1. Grayscale (Black and White)
2. Sepia (Vintage)
3. Inverted (Negative)
4. sketch 
5. Cool Blue
6. Warm Blue

'''
#TODO Test this shit
class Color_Filter:
   def __init__(self):
      self.raw_image = None

   #for safety reasons lang ito. tatawagin ito kapag exit sa edit mode
   def clear_edit (self):
      self.raw_image = None
      self.edited_image = None

   #dapat tawagin ito every start nung edit mode, magsisilbi itong backup
   def set_image_to_edit(self, image):
      decode_img = np.frombuffer(image.read(), np.uint8)
      decode_img = cv2.imdecode(decode_img, cv2.IMREAD_COLOR)
      self.raw_image = decode_img

   def grayscale_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
         ret, jpeg = cv2.imencode('.jpg', gray_image) #ignore the ret
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None

   def sepia_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         sepia_filter = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
         
         sepia = cv2.transform(image_copy, sepia_filter)
         sepia = np.clip(sepia, 0, 255).astype(np.uint8)

         ret, jpeg = cv2.imencode('.jpg', sepia)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None

   def inverted_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         inverted = cv2.bitwise_not(image_copy)
         ret, jpeg = cv2.imencode('.jpg', inverted)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None

   def warm_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         image_copy[:,:,2] = cv2.add(image_copy[:,:,2], 50)
         ret, jpeg = cv2.imencode('.jpg', image_copy)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None

   def cool_blue_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         image_copy[:,:,0] = cv2.add(image_copy[:,:,0], 50)
         ret, jpeg = cv2.imencode('.jpg', image_copy)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None
      
   def sketch_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
         inv = 255 - gray
         blur = cv2.GaussianBlur(inv, (21, 21), 0)
         sketch = cv2.divide(gray, 255 - blur, scale=256.0)
         ret, jpeg = cv2.imencode('.jpg', sketch)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None
   
   # 3 new color filter (adjust na app.py + nailagay narin sa casual)
   def bright_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         hsv = cv2.cvtColor(image_copy, cv2.COLOR_BGR2HSV)
         h, s, v = cv2.split(hsv)
         v = cv2.add(v, 40)  # Increase brightness
         final_hsv = cv2.merge((h, s, v))
         bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
         ret, jpeg = cv2.imencode('.jpg', bright)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None
    
   def cartoon_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
         gray = cv2.medianBlur(gray, 5)
         edges = cv2.adaptiveThreshold(gray, 255,
                                       cv2.ADAPTIVE_THRESH_MEAN_C,
                                       cv2.THRESH_BINARY, 9, 9)
         color = cv2.bilateralFilter(image_copy, 9, 250, 250)
         cartoon = cv2.bitwise_and(color, color, mask=edges)
         ret, jpeg = cv2.imencode('.jpg', cartoon)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None
      
   def green_vibe_image(self):
      if self.raw_image is not None:
         image_copy = self.raw_image.copy()
         image_copy[:, :, 1] = cv2.add(image_copy[:, :, 1], 40)  # Boost green
         image_copy[:, :, 2] = cv2.subtract(image_copy[:, :, 2], 20)  # Lower red
         ret, jpeg = cv2.imencode('.jpg', image_copy)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None



   #gagamitin ito kapag nagapply na si user ng filter per tinaggal nya magkakaroon pa ito ng another shit fix dahil possible na hindi makita ang sticker dito
   def return_raw(self):
      if self.raw_image is not None:
         ret, jpeg = cv2.imencode('.jpg', self.raw_image)
         return jpeg.tobytes()
      else:
         print("No image detected")
         return None
