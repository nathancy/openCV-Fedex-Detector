# Blur detection using the variance of Laplacian method to give a floating point
# value to represent the 'blurryness' of an image. Convolve the input image with the
# Laplacian operator and compute the variance. If the variance falls below a threshold,
# mark the image as blurry

from __future__ import division
from image_detector import imageDetector
import cv2
import numpy as np

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

imageDetector = imageDetector()
imageDetector.getIPAddress()
imageDetector.initializeThresholds()
imageDetector.initializeStream()
imageDetector.start()

while(imageDetector.isOpened()):
    frame = imageDetector.getFrame()
    gray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
    variance = variance_of_laplacian(gray)
    cv2.putText(frame, "Sharpness: " + str(variance), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
    cv2.imshow('blurTest', frame)
    cv2.waitKey(1)
