import numpy as np
import playsound
import cv2
import argparse
import imutils
from threading import Thread
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
        self.error_iteration_check = 35
        self.error_pixel_movement = 75
        self.shape_comparison_ratio = 10

    # Initialize IP camera stream
    def initializeStream(self):
        self.image_name = "frame"
        self.stream = 'rtsp://admin:sagnac808@192.168.1.' + str(self.ip_address) + ':554/cam/realmonitor?channel=1&subtype=0'
        self.capture = cv2.VideoCapture(self.stream)
        (self.status, self.raw_frame) = self.capture.read()
        self.frame = self.raw_frame
        self.stopped = False
        self.image_width = 900
        self.image_height = 500
    
    def getIPAddress(self):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-s", "--stream", required=False, help="Stream number IP address")
        args = vars(self.ap.parse_args())
        if not args['stream']:
            self.ip_address = '46'
        else:
            self.ip_address = args['stream']
    def start(self):
        Thread(target=self.captureFrames, args=()).start()
        return self

    # Check if stream is online
    def isOpened(self):
        return self.capture.isOpened()
   
    # Return most recent frame from stream
    def getFrame(self):
        return self.frame

    # Constantly capture frames
    def captureFrames(self):
        while True:
            if self.stopped:
                return
            (self.status, self.raw_frame) = self.capture.read()
            while not self.status:
                (self.status, self.raw_frame) = self.capture.read()
            self.frame = imutils.resize(self.raw_frame, width=min(self.image_width, self.raw_frame.shape[1]))
    
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
        #cv2.circle(frame, (box1[4],box1[5]), 2, (240, 0,159), 20)
        #cv2.circle(frame, (box2[4],box2[5]), 2, (0,0,255), 20)

        #box1 = self.showBoundingBox(box1[0], box1[1], box1[2], box1[3], frame.copy(), (255,255,255))
        #self.showBoundingBox(box2[0], box2[1], box2[2], box2[3], box1, (0,255,0))

        # Check for shape ratio. Lower value = higher chance two contours are rectangles
        shape_comparison = cv2.matchShapes(contour1, contour2, 1, 0)
        if shape_comparison <= self.shape_comparison_ratio:
            # Iterate through the three coordinates, cv2.pointPolygonTest returns 1 if given
            # coordinate is within the given contour
            for coordinate in coordinates:
                if cv2.pointPolygonTest(contour2, coordinate, False) >= 0:
                    return True
        return False

    # Additional checks to ensure identification is not a false positive
    def errorChecker(self, box1, box2):
        initial_point = box1[0]
        average = []
        for num in range(self.error_iteration_check):
            frame = self.getFrame()
            box1 = self.findBoundingBox(self.colors['purple'], frame)
            box2 = self.findBoundingBox(self.colors['red'], frame)
            if box1 and box2:
                if self.boxesAdjacent(box1, box2, box1[6], box2[6], frame):
                    # Ensure width of box is greater than a certain amount
                    if box1[2] < 30 or box2[2] < 30:
                        self.showFrame(frame)
                        #print("False box width")
                        return (False, box1, box2)
                    else:
                        self.showFrame(frame)
                        average.append(box1[0])
                else:
                    self.showFrame(frame)
                    #print("Not adjacent")
                    return (False,box1,box2)
            else:
                self.showFrame(frame)
                #print("Not valid boxes")
                return (False,box1,box2)
            self.showFrame(frame)
            if num == self.error_iteration_check - 1:
                new_point = abs(sum(average)/len(average) - initial_point)
                return (True,box1,box2) if new_point < self.error_pixel_movement else (False,box1,box2)

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

