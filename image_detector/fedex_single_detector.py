from image_detector import imageDetector
import numpy as np
import cv2

#frame = cv2.imread('images/dark-red.jpg')
#frame = cv2.imread('images/fedex-logo.PNG')
#frame = cv2.imread('images/fedex-tunnel.jpg')
#frame = cv2.imread('images/light-red.jpg')
#frame = cv2.imread('images/area.PNG')
#frame = cv2.imread('images/area.PNG')
frame = cv2.imread('images/fedex-car.PNG')

imageDetector = imageDetector()
imageDetector.getIPAddress()
imageDetector.initializeThresholds()
imageDetector.initializeStream()

box1 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('purple'), frame)
box2 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('red'), frame)

if box1 and box2:
    if imageDetector.boxesAdjacent(box1, box2, box1[6], box2[6], frame):
        points = imageDetector.combineBoundingBox(box1, box2)
        imageDetector.showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
        key = cv2.waitKey(0)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

