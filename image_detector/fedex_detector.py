import numpy as np
import cv2

#image = cv2.imread('pokemon.png')
#image = cv2.imread('light-red.jpg')
#image = cv2.imread('dark-red.jpg')
#image = cv2.imread('fedex-tunnel.jpg')
#image = cv2.imread('fedex-logo.PNG')
#image = cv2.imread('plane.PNG')
image = cv2.imread('fedex-car.PNG')
boundaries = [
    # hsv
    # Real life purple
    #([112,131,13], [145,255,255]),
    #([112,25,13], [165,255,255]),
    ([118,45,25], [154,255,255]),

    # original red
    #([0,150,20], [13,255,255])
    #([0,170,20], [13,255,255])
    ([0,130,0], [15,255,255])
        ]

for (lower, upper) in boundaries:
    '''
    lower = np.array(lower, np.uint8)
    upper = np.array(upper, np.uint8)

    blurred = cv2.GaussianBlur(image, (5,5), 0)
    image_hsv_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    frame_treshold = cv2.inRange(image_hsv_blurred, lower, upper)

    #output = cv2.bitwise_and(image, image, mask = mask)
    cv2.imshow("images", frame_treshold)
    cv2.waitKey(0)
    '''
    lower = np.array(lower, np.uint8)
    upper = np.array(upper, np.uint8)

    blurred = cv2.GaussianBlur(image, (5,5), 0)
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(blurred, kernel, iterations = 1)
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    image_hsv = cv2.cvtColor(dilation, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image_hsv, lower, upper)
    #cv2.imshow("images", mask)
    #cv2.waitKey(0)

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
        cv2.putText(detected_image, 'c', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100 ,255,100), 2)

        cv2.imshow("images", detected_image)
    else:
        cv2.imshow("images", image)

    cv2.waitKey(0)
