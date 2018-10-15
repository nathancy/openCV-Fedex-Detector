# Blur detection using the variance of Laplacian method to give a floating point
# value to represent the 'blurryness' of an image. Convolve the input image with the
# Laplacian operator and compute the variance. If the variance falls below a threshold,
# mark the image as blurry

from __future__ import division
import cv2
import numpy as np
import argparse

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def nothing(*arg):
        pass

def isOdd(num):
    return True if num % 2 == 1 else False

blur_level = (0,40)

cv2.namedWindow('blurTest')
cv2.createTrackbar('blur', 'blurTest', blur_level[0], blur_level[1], nothing)

#frame= 'images/logo.PNG'
#frame = 'images/plane.PNG'
#frame= 'images/andrew.PNG'
#frame= 'images/tight.PNG'
frame= 'images/dark-red.jpg'

original = cv2.imread(frame)
last_blurred = cv2.GaussianBlur(original.copy(), (1,1), 0)

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--threshold", type=float, default = 100.0, help="Focus measures that fall below this value will be considered blurry")
args = vars(ap.parse_args())


while True:
    # Get blur values from sliders
    blur = cv2.getTrackbarPos('blur', 'blurTest')
    # Display original frame
    if blur == 0:
        frame = original.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        variance = variance_of_laplacian(gray)
        cv2.putText(frame, "Original: " + str(variance), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
        cv2.imshow('blurTest', frame)
        cv2.waitKey(1)
    else:
        # Gaussian blur only works with odd numbered kernels
        if isOdd(blur): 
            blurred = cv2.GaussianBlur(original.copy(), (blur,blur),0)
            gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
            text = "Not Blurry"
            variance = variance_of_laplacian(gray)
            if variance < args["threshold"]:
                text = "Blurry"
            cv2.putText(blurred, text + ": " + str(variance), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
            last_blurred = blurred
            cv2.imshow('blurTest', blurred)
            cv2.waitKey(1)
        else:
            cv2.imshow('blurTest', last_blurred)
            cv2.waitKey(1)

