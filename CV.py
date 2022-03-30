import cv2
import numpy as np
from matplotlib import pyplot as plt


drawing = False
drawingBg = False
top_left_x, top_left_y = 0, 0
bottom_right_x, bottom_right_y = 0, 0
mouse_image = cv2.imread("image/messi1.jpg")
new_mask = np.zeros((mouse_image.shape[0], mouse_image.shape[1]), np.uint8)
rect_done = False
def mouse_callback(e, x, y, flags, param):
 if not rect_done:
  global top_left_x, top_left_y, bottom_right_x, bottom_right_y, drawing, drawingBg, mouse_image
  if e == cv2.EVENT_LBUTTONDOWN:
   drawing = True
   top_left_x, top_left_y = x, y
  elif e == cv2.EVENT_MOUSEMOVE:
   if drawing:
    mouse_image = cv2.imread("image/messi1.jpg")
    cv2.rectangle(mouse_image, (top_left_x, top_left_y), (x, y), (255,0,0), 1)
  elif e == cv2.EVENT_LBUTTONUP:
   bottom_right_x, bottom_right_y = x, y
   drawing = False
 else:
  if e == cv2.EVENT_LBUTTONDOWN:
   drawing = True
  elif e == cv2.EVENT_MOUSEMOVE:
   if drawing:
    cv2.circle(new_mask, (x,y), 5, 255, -1)
   if drawingBg:
    cv2.circle(new_mask, (x,y), 5, 127, -1)
  elif e == cv2.EVENT_LBUTTONUP:
   drawing = False
  elif e == cv2.EVENT_RBUTTONDOWN:
   drawingBg = True
  elif e == cv2.EVENT_RBUTTONUP:
   drawingBg = False


cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)
mask = np.zeros((mouse_image.shape[0], mouse_image.shape[1]), np.uint8)

while True:
 cv2.imshow('Image', mouse_image)
 cv2.imshow('Mask', new_mask)
 pressed_key = cv2.waitKey(30)

 if pressed_key == 32:
  mouse_image = cv2.imread("image/messi1.jpg")
  rect = (top_left_x, top_left_y, bottom_right_x - top_left_x, bottom_right_y - top_left_y)
  bgdModel = np.zeros((1, 65), np.float64)
  fgdModel = np.zeros((1, 65), np.float64)
  if not rect_done:
   cv2.grabCut(mouse_image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
   rect_done = True
  else:
   mask[new_mask == 127] = 0
   mask[new_mask == 255] = 1
  cv2.imshow('mask_new', mask * 255)
  print(mask.shape)
  mask, bgdModel, fgdModel = cv2.grabCut(mouse_image, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
 mask2 = mask & 1
 img = mouse_image * mask2[:, :, np.newaxis]

 sea = cv2.imread("image/sea.jpg")
 if sea.shape != mask2.shape:
  sea = cv2.resize(sea, mask2.shape[:2][::-1])
 sea2 = sea * (1 - mask2[:, :, np.newaxis])
 mask2 = cv2.cvtColor(mask2, cv2.COLOR_GRAY2BGR)
 mouse_image = mouse_image * mask2
 if mouse_image.shape != sea2.shape:
  sea2 = cv2.resize(sea2, mouse_image.shape[:2][::-1])
 img3 = cv2.add(sea2, mouse_image)
 cv2.imshow("img3", img3)
 cv2.imshow('sea2', sea2)
if pressed_key == 27:
 break