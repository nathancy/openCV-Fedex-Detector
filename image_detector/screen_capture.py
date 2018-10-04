# Screen record 
import mss
import numpy as np
import cv2

with mss.mss() as sct:
    while(True):
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        img = np.array(sct.grab(monitor))
        cv2.imshow("test", img)
        cv2.waitKey(1)

