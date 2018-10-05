# Screen record the VLC stream and apply image detection
from image_detector import imageDetector
import mss
import numpy as np
import cv2

imageDetector = imageDetector()
imageDetector.initializeThresholds()
with mss.mss() as sct:
    while(True):
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        frame = np.array(sct.grab(monitor))
        box1 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('purple'), frame)
        box2 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('red'), frame)
        if box1 and box2:
            if imageDetector.boxesAdjacent(box1, box2, box1[6], box2[6], frame):
                if imageDetector.errorChecker(box1,box2):
                    points = imageDetector.combineBoundingBox(box1, box2)
                    imageDetector.showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
                    print("Fedex Arrived")
                    cv2.waitKey(0)
            else:
                imageDetector.showFrame(frame)
        else:
            imageDetector.showFrame(frame)

