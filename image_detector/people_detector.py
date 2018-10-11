from __future__ import print_function
import cv2
import numpy as np
from imutils.object_detection import non_max_suppression
from imutils import paths
import argparse
import imutils
from image_detector import imageDetector

imageDetector = imageDetector()
imageDetector.getIPAddress()
imageDetector.initializeStream()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

while(imageDetector.isOpened()):
    # Load IP camera and resize frame to reduce detection time and improve detection accuracy
    image = imageDetector.getFrame()
    image = imutils.resize(image, width=min(400, image.shape[1]))

    # Detect people in the images
    # Larger scale evaluates less layers and increases performance but lower accuracy
    (rects, weights) = hog.detectMultiScale(image, winStride=(4,4), padding=(8,8), scale=.95)

    # Apply non-maxima suppression to the bounding boxes using a fairly
    # large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x,y,x+w, y+h] for (x,y,w,h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    # Draw the final bounding boxes
    for(xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0,255,0), 2)
    imageDetector.showFrame(image)

    


    





