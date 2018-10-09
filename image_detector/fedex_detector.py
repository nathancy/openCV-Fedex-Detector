from image_detector import imageDetector
import numpy as np
import cv2

imageDetector = imageDetector()
imageDetector.initializeThresholds()
imageDetector.initializeStream()
while(imageDetector.isOpened()):
    frame = imageDetector.getFrame()
    box1 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('purple'), frame)
    box2 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('red'), frame)
    if box1 and box2:
        if imageDetector.boxesAdjacent(box1, box2, box1[6], box2[6], frame):
            print("Checking if adjacent")
            if imageDetector.errorChecker(box1,box2):
                print("Passed error checker")
                points = imageDetector.combineBoundingBox(box1, box2)
                print("Combining bounding boxes")
                imageDetector.showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
                imageDetector.playNotification()
                print("Played notification")
                print("Fedex Arrived")
        else:
            imageDetector.showFrame(frame)
