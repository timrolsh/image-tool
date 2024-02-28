import cv2, os
from PIL import Image


# INPUT = "input/3077207647.jpeg"
# x = 7
# kSize = (x, x)
# y = 7
# guassian_strength = (y, y)
# IMG = Image.open("input/tester.png")
# IMG.save("image.png")
# INPUT = "image.png"


def rembg(INPUT, kSize):
    # ---- Guassian Blur ---- #
    image = cv2.imread(INPUT)  # input/3077207647.jpeg
    image_gray = cv2.imread(INPUT, cv2.IMREAD_GRAYSCALE)
    b, g, r = cv2.split(image)
    image2 = cv2.merge([r, g, b])
    blur = cv2.GaussianBlur(
        image_gray, ksize=kSize, sigmaX=0
    )  # the ksize value dictates the strength of the blur.
    ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    edged = cv2.Canny(blur, 5, 255)

    # ---- Close off the outline ---- #
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    # ---- Contour the outline and fill in based off the original image ---- #
    contours, _ = cv2.findContours(
        closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    total = 0
    contour_image = cv2.drawContours(image, contours, -1, (0, 255, 0), cv2.FILLED)
    cv2.imwrite("contoured.jpg", contour_image)

    # ------------- Remove white space and make transparent, and convert file type -----------------------
    img = Image.open("contoured.jpg")
    org_img = Image.open(
        INPUT
    )  # this opens the highlighted image, and the original as a PIL image

    img = img.convert("RGBA")
    org_img = org_img.convert("RGBA")  # add the alpha color channel (transparency)
    datas = img.getdata()
    org_datas = org_img.getdata()
    # save every pixel in the images as an array of RGBA values into an array for both original and contoured
    # keep original to have the non green version

    newData = []

    for index, item in enumerate(datas):
        if (
            item[0] in range(0, 20)  # give a little leniency for more accuracy
            and item[1] in range(220, 256)  # green
            and item[2] in range(0, 20)
        ):
            newData.append(
                org_datas[index]
            )  # if it's green save the original color from the original image
        else:
            newData.append((255, 255, 255, 0))  # transparent pixel

    img.putdata(newData)

    os.remove("contoured.jpg")
    os.remove("image.png")  # get rid of halfway images
    return img
