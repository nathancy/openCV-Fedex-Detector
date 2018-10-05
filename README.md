# openCV-Fedex-Detector

IP Camera OpenCV Fedex detector. Uses raw OpenCV, no deep learning or trained neural networks. Mainly uses color thresholding and contour detection. 

## Overall Algorithm 
```
Initialize IP Camera stream
While camera is open
    Grab frame
    Find bounding box for purple
    Find bounding box for red/orange
    If both bounding boxes are valid
        If boxes are adjacent relative to their proximity 
            If contours pass false positive checks
                Combine bounding boxes
                Show bounding box on frame
                Play sound notificaiton
        Else show raw frame
    Else show raw frame
```

## Bounding Box Algorithm
```
Transform BGR lower and upper color thresholds into np.arrays
Gaussian blur the frame
Create a kernel 2D matrix
Use kernel to erode frame
Use kernel to dilate frame
Convert BGR to HSV
Create a mask
Find all contours in the mask
Find largest contour and obtain bounding rectangle coordinates
Return x,y,w,h,cX,cY,and largest contour
```

