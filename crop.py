import cv2
import numpy as np
from PIL import Image
from pil_to_cv import pil_to_cv


def crop_image(INPUT: Image, kSize: tuple[int, int]):
    image = pil_to_cv(INPUT)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(
        image_gray, ksize=kSize, sigmaX=0
    )  # the ksize value dictates the strength of the blur.
    edged = cv2.Canny(blur, 10, 250)

    # ---- Close off the outline ---- #
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(
        edged, cv2.MORPH_CLOSE, kernel
    )  # close off any "holes" in the outline

    # ---- Contour the outline on based off the original image ---- #
    contours, _ = cv2.findContours(
        closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # ---- Find coordinates of closest 4 corners (square) around the outline of the image ---- #
    contours_xy = [np.array(cnt) for cnt in contours]
    # contours_xy.shape

    x_min, x_max = 0, 0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(
                contours_xy[i][j][0][0]
            )  # Value of x when fourth parenthesis is 0
            x_min = min(value)
            x_max = max(value)

    # Find min and max of y
    y_min, y_max = 0, 0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(
                contours_xy[i][j][0][1]
            )  # Value of x when fourth parenthesis is 0
            y_min = min(value)
            y_max = max(value)

    x = x_min
    y = y_min
    w = x_max - x_min
    h = y_max - y_min

    img_trim = image[y: y + h, x: x + w]
    # return a pil image file from this variable img_trim
    return Image.fromarray(cv2.cvtColor(img_trim, cv2.COLOR_BGR2RGB))
