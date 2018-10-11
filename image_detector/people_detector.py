from __future__ import print_function
import cv2
import numpy as np
from imutils import paths
import argparse
import imutils
from image_detector import imageDetector

imageDetector = imageDetector()
imageDetector.getIPAddress()
imageDetector.initializeStream()

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Malisiewicz method for Non-Maximum suppression
def non_max_suppression_fast(boxes, overlapThresh=0.35):
    # If there are no boxes, return empty list
    if len(boxes) == 0:
        return []
    # If the bounding boxes are integers, convert them to float
    if boxes.dtype.kind == 'i':
        boxes = boxes.astype('float')
    # Initialize the list of picked indexes
    pick = []

    # Grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # Compute the area of the bounding boxes and sort by 
    # the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # Keep looping while some indexes still remain in the list
    while len(idxs) > 0:
        # Grab the last index in the list and add the index value to
        # the list of picked indexes
        last = len(idxs) -1
        i = idxs[last]
        pick.append(i)

        # Find the largest (x,y) coordinates for the start of the bounding box 
        # and the smallest (x,y) coordinates for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # Delete all indexes from the list
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    # Return only the bounding boxes that were picked using the integer data type
    return boxes[pick].astype('int')

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
    pick = non_max_suppression_fast(rects, overlapThresh=0.35)

    # Draw the final bounding boxes
    for(xA, yA, xB, yB) in pick:
        cv2.rectangle(image, (xA, yA), (xB, yB), (0,255,0), 2)
    imageDetector.showFrame(image)

