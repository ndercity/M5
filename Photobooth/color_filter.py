import cv2
import numpy as np
from PIL import Image

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

   #for safety reasons lang ito
   def __del__(self):
      self.raw_image = None
      self.edited_image = None

   #dapat tawagin ito every start nung edit mode, magsisilbi itong backup
   def set_image_to_edit(self, image):
      self.raw_image = image

   def grayscale(self):
      if not self.image_raw == None:
         image_copy = self.Image.copy()
         gray_image = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
         ret, jpeg = cv2.imencode('.jpg', gray_image) #ignore the ret
         return jpeg.tobytes()
      else:
         return None

   def sepia_image(self):
      if not self.image_raw == None:
         image_copy = self.Image.copy()
         sepia_filter = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
         
         sepia = cv2.transform(image_copy, sepia_filter)
         sepia = np.clip(sepia, 0, 255).astype(np.uint8)

         ret, jpeg = cv2.imencode('.jpg', sepia)
         return jpeg.tobytes()
      else:
         return None

   def inverted_image(self):
      if not self.image_raw == None:
         image_copy = self.Image.copy()
         inverted = cv2.bitwise_not(image_copy)
         ret, jpeg = cv2.imencode('.jpg', inverted)
         return jpeg.tobytes()
      else:
         return None

   def warm_image(self):
      if not self.image_raw == None:
         image_copy = self.Image.copy()
         image_copy[:,:,2] = cv2.add(image_copy[:,:,2], 50)
         ret, jpeg = cv2.imencode('.jpg', image_copy)
         return jpeg.tobytes()
      else:
         return None

   def cool_blue_image(self):
      if not self.image_raw == None:
         image_copy = self.Image.copy()
         image_copy[:,:,0] = cv2.add(image_copy[:,:,0], 50)
         ret, jpeg = cv2.imencode('.jpg', image_copy)
         return jpeg.tobytes()
      else:
         return None
      
   def sketch_image(self):
      if not self.image_raw == None:
         image_copy =self.Image.copy()
         gray = cv2.cvtColor(image_copy, cv2.COLOR_BGR2GRAY)
         inv = 255 - gray
         blur = cv2.GaussianBlur(inv, (21, 21), 0)
         sketch = cv2.divide(gray, 255 - blur, scale=256.0)
         ret, jpeg = cv2.imencode('.jpg', sketch)
         return jpeg.tobytes()
      else:
         return None

   #gagamitin ito kapag nagapply na si user ng filter per tinaggal nya magkakaroon pa ito ng another shit fix dahil possible na hindi makita ang sticker dito
   def return_raw(self):

      if not self.image_raw == None:
         ret, jpeg = cv2.imencode('.jpg', self.raw_image)
         return jpeg.tobytes()
      else:
         return None
