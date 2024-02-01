import cv2, sys
from matplotlib import pyplot as plt
import numpy as np


# ---- Guassian Blur ---- #
image = cv2.imread(r"cosmetic.jpg")  # input/3077207647.jpeg
image_gray = cv2.imread(r"cosmetic.jpg", cv2.IMREAD_GRAYSCALE)
b, g, r = cv2.split(image)
image2 = cv2.merge([r, g, b])
blur = cv2.GaussianBlur(
    image_gray, ksize=(5, 5), sigmaX=0
)  # the ksize value dictates the strength of the blur.
ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
edged = cv2.Canny(blur, 10, 250)
# cv2.imshow( 'Edged' , edged)

# ---- Close off the outline ---- #
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(
    edged, cv2.MORPH_CLOSE, kernel
)  # close off any "holes" in the outline
cv2.imshow("closed", closed)

# Show original for reference
cv2.imshow("image", image)


def bgremove1(myimage):
    # Blur to image to reduce noise
    myimage = cv2.GaussianBlur(myimage, (5, 5), 0)

    # We bin the pixels. Result will be a value 1..5
    bins = np.array([0, 51, 102, 153, 204, 255])
    myimage[:, :, :] = np.digitize(myimage[:, :, :], bins, right=True) * 51

    # Create single channel greyscale for thresholding
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)

    # Perform Otsu thresholding and extract the background.
    # We use Binary Threshold as we want to create an all white background
    ret, background = cv2.threshold(
        myimage_grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)

    # Perform Otsu thresholding and extract the foreground.
    # We use TOZERO_INV as we want to keep some details of the foregorund
    ret, foreground = cv2.threshold(
        myimage_grey, 0, 255, cv2.THRESH_TOZERO_INV + cv2.THRESH_OTSU
    )  # Currently foreground is only a mask
    foreground = cv2.bitwise_and(
        myimage, myimage, mask=foreground
    )  # Update foreground with bitwise_and to extract real foreground

    # Combine the background and foreground to obtain our final image
    finalimage = background + foreground

    return finalimage


def bgremove2(myimage):
    # First Convert to Grayscale
    myimage_grey = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)

    ret, baseline = cv2.threshold(myimage_grey, 127, 255, cv2.THRESH_TRUNC)

    ret, background = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY)

    ret, foreground = cv2.threshold(baseline, 126, 255, cv2.THRESH_BINARY_INV)

    foreground = cv2.bitwise_and(
        myimage, myimage, mask=foreground
    )  # Update foreground with bitwise_and to extract real foreground

    # Convert black and white back into 3 channel greyscale
    background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)

    # Combine the background and foreground to obtain our final image
    finalimage = background + foreground
    return finalimage


def bgremove3(myimage):
    # BG Remover 3
    myimage_hsv = cv2.cvtColor(myimage, cv2.COLOR_BGR2HSV)

    # Take S and remove any value that is less than half
    s = myimage_hsv[:, :, 1]
    s = np.where(s < 127, 0, 1)  # Any value below 127 will be excluded

    # We increase the brightness of the image and then mod by 255
    v = (myimage_hsv[:, :, 2] + 127) % 255
    v = np.where(v > 127, 1, 0)  # Any value above 127 will be part of our mask

    # Combine our two masks based on S and V into a single "Foreground"
    foreground = np.where(s + v > 0, 1, 0).astype(
        np.uint8
    )  # Casting back into 8bit integer

    background = np.where(foreground == 0, 255, 0).astype(
        np.uint8
    )  # Invert foreground to get background in uint8
    background = cv2.cvtColor(
        background, cv2.COLOR_GRAY2BGR
    )  # Convert background back into BGR space
    foreground = cv2.bitwise_and(
        myimage, myimage, mask=foreground
    )  # Apply our foreground map to original image
    finalimage = background + foreground  # Combine foreground and background

    return finalimage


# ---- Contour the outline on based off the original image ---- #
contours, _ = cv2.findContours(
    closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)  # save the outside and maybe cover everything inside to save and then just fully remove
total = 0
contour_image = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
# cv2.imshow( 'contours_image' , contour_image)

# ---- Find coordinates of closest 4 corners (square) around the outline of the image ---- #
contours_xy = np.array(contours)
contours_xy.shape

x_min, x_max = 0, 0
value = list()
for i in range(len(contours_xy)):
    for j in range(len(contours_xy[i])):
        value.append(contours_xy[i][j][0][0])  # Value of x when fourth parenthesis is 0
        x_min = min(value)
        x_max = max(value)
# print(x_min)
# print(x_max)

# Find min and max of y
y_min, y_max = 0, 0
value = list()
for i in range(len(contours_xy)):
    for j in range(len(contours_xy[i])):
        value.append(contours_xy[i][j][0][1])  # Value of x when fourth parenthesis is 0
        y_min = min(value)
        y_max = max(value)
# print(y_min)
# print(y_max)

x = x_min
y = y_min
w = x_max - x_min
h = y_max - y_min

img_trim = image[y : y + h, x : x + w]
cv2.imwrite("org_trim.jpg", img_trim)
org_image = cv2.imread("org_trim.jpg")
cv2.imshow("org_image", org_image)
x_image = bgremove1(image)
cv2.imshow("test", x_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
