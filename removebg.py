import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image


# ---- Guassian Blur ---- #
image = cv2.imread(r"input/3077207647.jpeg")  # input/3077207647.jpeg
image_gray = cv2.imread(r"input/3077207647.jpeg", cv2.IMREAD_GRAYSCALE)
b, g, r = cv2.split(image)
image2 = cv2.merge([r, g, b])
blur = cv2.GaussianBlur(
    image_gray, ksize=(5, 5), sigmaX=0
)  # the ksize value dictates the strength of the blur.
ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
edged = cv2.Canny(blur, 10, 250)


# ---- Close off the outline ---- #
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(
    edged, cv2.MORPH_CLOSE, kernel
)

# ---- Contour the outline and fill in based off the original image ---- #
contours, _ = cv2.findContours(
    closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
total = 0
contour_image = cv2.drawContours(image, contours, -1, (0, 255, 0), cv2.FILLED)
# cv2.imshow( 'contours_image' , contour_image)
cv2.imwrite("contoured.jpg", contour_image)

img = Image.open("contoured.jpg")
org_img = Image.open("input/3077207647.jpeg")
img = img.convert("RGBA")
org_img = org_img.convert("RGBA")
datas = img.getdata()
org_datas = org_img.getdata()

newData = []
coords = []

for index, item in enumerate(datas):
    if (
        item[0] in range(0, 20)
        and item[1] in range(220, 256)
        and item[2] in range(0, 20)
    ):
        newData.append(org_datas[index])
    else:
        newData.append((255, 255, 255, 0))


img.putdata(newData)
img.save("output/New.png", "PNG")

cv2.waitKey(0)
cv2.destroyAllWindows()
