import cv2
import numpy as np


def crop_image(INPUT, kSize: int):
    # ---- Guassian Blur ---- #
    image = cv2.imread(INPUT)  # input/3077207647.jpeg
    image_gray = cv2.imread(INPUT, cv2.IMREAD_GRAYSCALE)
    b, g, r = cv2.split(image)
    image2 = cv2.merge([r, g, b])
    blur = cv2.GaussianBlur(
        image_gray, ksize=kSize, sigmaX=0
    )  # the ksize value dictates the strength of the blur.
    ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
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
    total = 0
    contour_image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    # ---- Find coordinates of closest 4 corners (square) around the outline of the image ---- #
    contours_xy = np.array(contours)
    contours_xy.shape

    x_min, x_max = 0, 0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(
                contours_xy[i][j][0][0]
            )  # Value of x when fourth parenthesis is 0
            x_min = min(value)
            x_max = max(value)
    # print(x_min)
    # print(x_max)

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
    # print(y_min)
    # print(y_max)

    x = x_min
    y = y_min
    w = x_max - x_min
    h = y_max - y_min

    img_trim = image[y : y + h, x : x + w]
    # cropped = cv2.imwrite("cropped.jpg", img_trim)
    # cv2.imshow("cropped", cropped)
    return img_trim
