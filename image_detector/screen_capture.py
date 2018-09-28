'''
import numpy as np
import cv2
from PIL import ImageGrab as ig
import time

last_time = time.time()
while(True):
    screen = ig.grab(bbox=(0,0,1920,1080))
    #screen = ig.grab()
    print('Loop took {} seconds',format(time.time()-last_time))
    cv2.imshow("test", np.array(screen))
    last_time = time.time()
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

'''
import mss
import numpy as np
import cv2

with mss.mss() as sct:
    while(True):
        monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        img = np.array(sct.grab(monitor))
        cv2.imshow("test", img)
        cv2.waitKey(1)

'''

# Colors are distored if you use PIL 





from PIL import ImageGrab
import numpy as np
import cv2
while(True):
    #img = ImageGrab.grab(bbox=(0,0,400,780)) #bbox specifies specific region (bbox= x,y,width,height)
    img = ImageGrab.grab() #bbox specifies specific region (bbox= x,y,width,height)
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("test", frame)
    cv2.waitKey(1)
cv2.destroyAllWindows()
'''
