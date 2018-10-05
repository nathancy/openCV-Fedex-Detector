import argparse
import imutils
import cv2

image = cv2.imread("../images/shapes.jpg")
grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(grey, (5,5),0)
#threshold = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY_INV)[1]
threshold = cv2.threshold(blurred, 70, 255, cv2.THRESH_BINARY)[1]
#threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,2)


#cv2.imshow('image', image)
#cv2.imshow('gray', grey)
#cv2.imshow('blurred', blurred)
#cv2.imshow('threshold', threshold)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
# Find outlines of the shapes
cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

for c in cnts:
    # Find center of shape
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.drawContours(image, [c], -1, (0,255,0), 2)
    cv2.circle(image, (cX, cY), 7, (255,255,255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

    cv2.imshow("image", image)
    cv2.waitKey(0)
