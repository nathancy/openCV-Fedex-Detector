import numpy as np
import cv2 as cv2

cap = cv2.VideoCapture('fedex.mp4')

boundaries = [
    #([112,131,13], [145,255,255]) # Purple
    ([110,0,13], [145,70,115]) # Purple
    #([0,170,20], [13,255,255])     # Red
    ]

while(cap.isOpened()):
    ret, image = cap.read()

    for (lower, upper) in boundaries:

        lower = np.array(lower, np.uint8)
        upper = np.array(upper, np.uint8)

        blurred = cv2.GaussianBlur(image, (5,5), 0)
        kernel = np.ones((5,5), np.uint8)
        erosion = cv2.erode(blurred, kernel, iterations = 1)
        dilation = cv2.dilate(erosion, kernel, iterations = 1)
        image_hsv = cv2.cvtColor(dilation, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(image_hsv, lower, upper)

        M = cv2.moments(mask)
        if M['m00'] != 0:
            cX = int(M['m10'] / M['m00'])
            cY = int(M['m01'] / M['m00'])
        else:
            cX, cY = 0, 0

        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Outline text
        #cv2.drawContours(image, contours, -1, (0,255,0), 2)
        
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        if len(contour_sizes) > 0:
            largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            x,y,w,h = cv2.boundingRect(largest_contour)
            detected_image = cv2.rectangle(image.copy(), (x, y), (x + w, y + h), (0,255,0),2)
            #cv2.putText(detected_image, 'center', (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100 ,255,100), 2)

            #output = cv2.bitwise_and(image, image, mask = mask)
            cv2.imshow("images", detected_image)
        else:
            cv2.imshow('images', image)

        key = cv2.waitKey(1)
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

