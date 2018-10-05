import cv2

class ShapeDetector:
    def __init__(self):
        pass
    def detect(self, contour):
        shape = "unidentified"
        perimeter = cv2.arcLength(contour, True)
        # Find number of verticies
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        # Triangle
        if len(approx) == 3:
            shape = "triangle"
        # Square or rectangle
        elif len(approx) == 4:
            # Find bounding box of contour and use it to compute aspect ratio
            # Aspect ratio = w / h
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # Square will have aspect ratio approximately equal to 1 otherwise its a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # Pentagon
        elif len(approx) == 5:
            shape = "pentagon"
        
        # Else assume it is circle
        else:
            shape = "circle"
        return shape

            

            

