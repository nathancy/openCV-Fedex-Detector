import numpy as np
import cv2
import mss 
from time import sleep

# HSV Values
#purple = ([118,45,25], [154,255,255])
purple = ([120,45,45], [150,255,255])
red = ([0,130,0], [15,255,255])

# Returns the bounding box coordinates of the largest contour found for a given color threshold (x,y,w,h)
# If no bounding box is found, returns None
def findBoundingBox(color, frame):
    lower = np.array(color[0], np.uint8)
    upper = np.array(color[1], np.uint8)

    blurred = cv2.GaussianBlur(frame, (5,5), 0)
    kernel = np.ones((5,5), np.uint8)
    erosion = cv2.erode(blurred, kernel, iterations = 1)
    dilation = cv2.dilate(erosion, kernel, iterations = 1)
    frame_hsv = cv2.cvtColor(dilation, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame_hsv, lower, upper)
    #cv2.imshow("images", mask)
    #cv2.waitKey(0)
    #return

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    if len(contour_sizes) > 0:
        largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
        x,y,w,h = cv2.boundingRect(largest_contour)
        return (x,y,w,h,(x+w/2),(y+h/2),largest_contour)
    else:
        return None

# Finds top left x and y coordinates, width, and heights from those coordinates
# since cv2.rectangle takes (x, y, w, h) as parameter
def combineBoundingBox(box1, box2):
    top_left_x = min(box1[0], box2[0])
    #print('top_left_x is ' + str(top_left_x))
    top_left_y = min(box1[1], box2[1])
    w = box2[0] + box2[2] - box1[0]
    h = max(box1[1] + box1[3], box2[1] + box2[3])- top_left_y
    return (top_left_x, top_left_y, w, h)

def showBoundingBox(x, y, w, h, frame, color):
    #(0,255,0)
    detected_image = cv2.rectangle(frame, (x, y), (x + w, y + h), color,3)
    cv2.putText(detected_image, 'Fedex', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
    showFrame(detected_image)
    return detected_image

def boxesAdjacent(box1, box2, contour1, contour2, frame):
    x = box1[4] + box1[2]/2 + box2[2]/4
    y = box1[5]
    coordinate_low = (x, y - box2[3]/2)
    coordinate_mid = (x, y)
    coordinate_high = (x, y + box2[3]/2)
    coordinates = [coordinate_low, coordinate_mid, coordinate_high]

    cv2.circle(frame, coordinate_mid, 2, (100,255,100),2)
    cv2.circle(frame, coordinate_low, 2, (100,255,100),2)
    cv2.circle(frame, coordinate_high, 2, (100,255,100),2)
    cv2.circle(frame, (box1[4],box1[5]), 2, (255,255,255), 20)
    cv2.circle(frame, (box2[4],box2[5]), 2, (0,255,0), 20)

    box1 = showBoundingBox(box1[0], box1[1], box1[2], box1[3], frame.copy(), (255,255,255))
    showBoundingBox(box2[0], box2[1], box2[2], box2[3], box1, (0,255,0))

    shape_comparison = cv2.matchShapes(contour1, contour2, 1, 0)
    print(shape_comparison)
    if shape_comparison <= 10:
        for coordinate in coordinates:
            if cv2.pointPolygonTest(contour2, coordinate, False) >= 0:
                return True
    return False
        
def errorChecker(box1):
    initial_point = box1[0]
    sleep(2)
    with mss.mss() as sct:
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        frame = np.array(sct.grab(monitor))
        new_box = findBoundingBox(purple, frame)
        new_point = abs(new_box[0] - initial_point)
        return True if new_point < 50 else False 

def showFrame(frame):
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit(1)
    
    
with mss.mss() as sct:
    while(True):
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        frame = np.array(sct.grab(monitor))
        cv2.circle(frame, (0,0), 2, (100,255,100),2)
        cv2.circle(frame, (50,0), 2, (100,255,100),2)
        box1 = findBoundingBox(purple, frame)
        box2 = findBoundingBox(red, frame)
        if box1 and box2:
            if boxesAdjacent(box1, box2, box1[6], box2[6], frame):
                #box1 = showBoundingBox(box1[0], box1[1], box1[2], box1[3], frame, (288,80,36))
                #showBoundingBox(box2[0], box2[1], box2[2], box2[3], box1, (175,150,150))
                if errorChecker(box1):
                    points = combineBoundingBox(box1, box2)
                    showBoundingBox(points[0], points[1], points[2], points[3], frame, (0,255,0))
                    print("fedex here")
                    cv2.waitKey(0)
            else:
                showFrame(frame)
        else:
            showFrame(frame)

