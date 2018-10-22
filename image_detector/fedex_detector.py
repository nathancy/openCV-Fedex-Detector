from image_detector import imageDetector
import numpy as np
import cv2

def saveImage(frame, count):
    cv2.imwrite("photos/" + str(count) + ".png", frame)

imageDetector = imageDetector()
imageDetector.getIPAddress()
imageDetector.initializeThresholds()
imageDetector.initializeStream()
imageDetector.start()
count = 0
while(imageDetector.isOpened()):
    frame = imageDetector.getFrame()
    box1 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('purple'), frame)
    box2 = imageDetector.findBoundingBox(imageDetector.getColorThreshold('red'), frame)
    if box1 and box2:
        if imageDetector.boxesAdjacent(box1, box2, box1[6], box2[6], frame):
            #print('------------------')
            #print("Entering error checker")
            status,box1,box2 = imageDetector.errorChecker(box1,box2)
            if status:
                points = imageDetector.combineBoundingBox(box1, box2)
                imageDetector.showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
                imageDetector.playNotification()
                saveImage(frame, count)
                count += 1
                print('Fedex arrived')
        else:
            imageDetector.showFrame(frame)
    else:
        imageDetector.showFrame(frame)
