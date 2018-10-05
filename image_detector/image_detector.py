import numpy as np
import playsound
import cv2
from time import sleep

# Class to read and process IP camera frames
class imageDetector:
    # Initialize color thresholds
    def initializeThresholds(self):
        # HSV color thresholds (low, high) 
        self.colors = {
                'purple': ([120,45,45], [150,255,255]),
                'red': ([0,130,0], [15,255,255]) 
                }
        self.image_name = "frame"
    # Initialize IP camera stream
    def initializeStream(self):
        self.stream = 'rtsp://admin:sagnac808@192.168.1.46:554/cam/realmonitor?channel=1&subtype=0'
        self.capture = cv2.VideoCapture(self.stream)
        cv2.namedWindow(self.image_name, 0)
        cv2.resizeWindow(self.image_name, 1600,900)

    # Check if stream is online
    def isOpened(self):
        return self.capture.isOpened()
   
    # Return most recent frame from stream
    def getFrame(self):
        ret, frame = self.capture.read()
        return frame

    # Return color threshold (low, high)
    def getColorThreshold(self, color):
        return self.colors[color]
        
    # Returns the bounding box coordinates and center coordinates of the largest 
    # contour found for a given color threshold (x,y,w,h,cX,cY). If no bounding box is found, returns None
    def findBoundingBox(self, color, frame):
        lower = np.array(color[0], np.uint8)
        upper = np.array(color[1], np.uint8)

        try:
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
        except cv2.error:
            return None

        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
        if len(contour_sizes) > 0:
            largest_contour = max(contour_sizes, key=lambda x: x[0])[1]
            x,y,w,h = cv2.boundingRect(largest_contour)
            # Returns top left (x,y) coordinates, width, height, and center (x,y) coordinates of contour
            return (x,y,w,h,(x+w/2),(y+h/2),largest_contour)
        else:
            return None

    # Given two contours, creates a single bounding box
    # Returns top left x and y coordinates, width, and height
    # 
    # (x1,y1)       w1                           (x3,y3)         w3
    #   ._____________________.                    .____________________________.
    #   |                     |                    |                            | 
    #   |                     |  h1                |                            |
    #   |   (x2,y2)           |                    |                            |
    #   |     ._______________|_______.      -->   |                            |
    #   |     |               |       |            |                            |  h3
    #   ._____|_______________.       |            |                            |
    #         |                       |  h2        |                            |
    #         |                       |            |                            |
    #         |           w2          |            |                            |
    #         ._______________________.            .____________________________.
    #
    def combineBoundingBox(self, box1, box2):
        x = min(box1[0], box2[0])
        y = min(box1[1], box2[1])
        w = box2[0] + box2[2] - box1[0]
        h = max(box1[1] + box1[3], box2[1] + box2[3]) - y
        return (x, y, w, h)
   
    # Given the contour coordinates (x,y,w,h) and the frame, draws a rectangular bounding box
    def showBoundingBox(self, x, y, w, h, frame, color):
        outlined_image = cv2.rectangle(frame, (x, y), (x + w, y + h), color,3)
        cv2.putText(outlined_image, 'Fedex', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)
        self.showFrame(outlined_image)
    
    # Given two contours, determines if boxes are adjacent based on their relative proximity
    # Creates three points to check if the right contour has at least one point within its countour
    # Also compares the two contours to ensure they are within a certain similar range
    # 
    #                       box2
    #                 ._____________.
    #      box1       |             |
    # .___________.   |             |
    # |           |   |    1 *      |
    # |           |   |             |
    # |           |   |             |
    # |  (cX,cY)  |   |             |
    # |     *     |   |    2 *      |
    # |           |   ._____________.             
    # |           |                
    # |           |             
    # |           |        3 *
    # .___________.
    # 
    def boxesAdjacent(self, box1, box2, contour1, contour2, frame):
        x = box1[4] + box1[2]/2 + box2[2]/4
        y = box1[5]
        coordinate_low = (x, y - box2[3]/2)
        coordinate_mid = (x, y)
        coordinate_high = (x, y + box2[3]/2)
        coordinates = [coordinate_low, coordinate_mid, coordinate_high]

        #cv2.circle(frame, coordinate_mid, 2, (100,255,100),2)
        #cv2.circle(frame, coordinate_low, 2, (100,255,100),2)
        #cv2.circle(frame, coordinate_high, 2, (100,255,100),2)
        cv2.circle(frame, (box1[4],box1[5]), 2, (255,255,255), 20)
        cv2.circle(frame, (box2[4],box2[5]), 2, (0,255,0), 20)

        #box1 = self.showBoundingBox(box1[0], box1[1], box1[2], box1[3], frame.copy(), (255,255,255))
        #self.showBoundingBox(box2[0], box2[1], box2[2], box2[3], box1, (0,255,0))

        shape_comparison = cv2.matchShapes(contour1, contour2, 1, 0)
        #print(shape_comparison)
        if shape_comparison <= 10:
            for coordinate in coordinates:
                if cv2.pointPolygonTest(contour2, coordinate, False) >= 0:
                    return True
        return False

    # Additional checks to ensure identification is not a false positive
    def errorChecker(self, box1, box2):
        print("Possible match...")
        # Ensure width of box is greater than a certain amount
        if box1[2] < 30 or box2[2] < 30:
            return False
        # Ensure the truck is not moving (doesn't move more than a certain pixel range)
        initial_point = box1[0]
        sleep(3)
        ret, frame = self.capture.read()
        new_box = self.findBoundingBox(self.colors['purple'], frame)
        new_point = abs(new_box[0] - initial_point)
        return True if new_point < 50 else False 

    # Show the frame to the screen
    def showFrame(self, frame):
        cv2.imshow(self.image_name, frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)
    
    # Play sound notification
    def playNotification(self):
        for num in range(5):
            playsound.playsound('sounds/graceful.mp3')

