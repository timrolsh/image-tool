from rembg import remove
from PIL import Image
import cv2, sys
from matplotlib import pyplot as plt
import numpy as np

# Store path of the image in the variable input_path
input = Image.open("cosmetic.jpg")

# Removing the background from the given Image
output = remove(input)

# Show image
cv2.imshow("trial", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
