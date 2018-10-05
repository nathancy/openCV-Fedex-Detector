from image_detector import imageDetector
import numpy as np
import cv2

#frame = cv2.imread('images/pokemon.png')
#frame = cv2.imread('images/light-red.jpg')
#frame = cv2.imread('images/dark-red.jpg')
#frame = cv2.imread('images/fedex-tunnel.jpg')
#frame = cv2.imread('images/fedex-logo.PNG')
frame = cv2.imread('images/plane.PNG')
#frame = cv2.imread('images/fedex-car.PNG')
#frame = cv2.imread('images/fedex-separate.PNG')
#frame = cv2.imread('images/black.PNG')

imageDetector = imageDetector()
imageDetector.initializeStream()

box1 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('purple'), frame)
box2 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('red'), frame)
if box1 and box2:
    imageDetector.showBoundingBox(box1[0], box1[1], box1[2], box1[3], frame, (288,80,36))
    imageDetector.showBoundingBox(box2[0], box2[1], box2[2], box2[3], frame, (175,150,150))
    cv2.waitKey(0)

