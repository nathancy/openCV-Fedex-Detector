from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2

class ColorLabeler:
    def __init__(self):
        # Initialize colors dictionary
        colors = OrderedDict({
            "red": (255,0,0),
            "green": (0,255,0),
            "blue": (0,0,255)})

        self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
        self.colorNames = []

        for i, (name, rgb) in enumerate(colors.items()):
            self.lab[i] = rgb
            self.colorNames.append(name)
        # Convert L*a*b* array from RGB to L*a*B*
        self.lab = cv2.cvtColor(self.lab, cv2.COLOR_RGB2LAB)

    def label(self, image, contour):
        # Construct mask for contour then compute average L*a*b* value for masked region
        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mask = cv2.erode(mask, None, iterations = 2)
        mean = cv2.mean(image, mask = mask)[:3]

        # Imitialize the minimum distance found thus far
        minDist = (np.inf, None)

        # Loop over the known L*a*b* values
        for i, row in enumerate(self.lab):
            # Compute distance between current L*a*b* color value and the mean of the image
            d = dist.euclidean(row[0], mean)

            # If distance smaller than current distance, update vairable
            if d < minDist[0]:
                minDist = (d, i)

        # Return name of the color with smallest distance
        return self.colorNames[minDist[1]]

