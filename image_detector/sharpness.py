# Blur detection using the variance of Laplacian method to give a floating point
# value to represent the 'blurryness' of an image. Convolve the input image with the
# Laplacian operator and compute the variance. If the variance falls below a threshold,
# mark the image as blurry
import cv2
import numpy as np
import argparse

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

img = 'images/logo.PNG'
img = 'images/plane.PNG'
#img = 'images/andrew.PNG'
#img = 'images/tight.PNG'

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--threshold", type=float, default = 100.0, help="Focus measures that fall below this value will be considered blurry")
args = vars(ap.parse_args())


image = cv2.imread(img)
blur = cv2.GaussianBlur(image, (5,5),0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
text = "Not Blurry"
variance = variance_of_laplacian(gray)
if variance < args["threshold"]:
    text = "Blurry"

cv2.putText(image, text + ": " + str(variance), (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)
cv2.imshow('image', image)
cv2.waitKey(0)

