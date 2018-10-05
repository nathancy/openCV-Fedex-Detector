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
    points = imageDetector.combineBoundingBox(box1, box2)
    imageDetector.showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
    cv2.waitKey(0)

