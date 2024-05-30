import cv2
import numpy as np
from PIL import Image


def rembg(input_image_path, kSize: tuple[int, int]):
    # Load the image using OpenCV directly
    image = cv2.imread(input_image_path)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Adjustable Gaussian blur
    blur = cv2.GaussianBlur(image_gray, kSize, sigmaX=0)

    # Enhanced edge detection using Canny
    edged = cv2.Canny(blur, 50, 150)

    # Improved morphological closing
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

    # Fill in the contours on the original image
    contours, _ = cv2.findContours(
        closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(image)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Convert mask to boolean and use it to create the final transparent image
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # Where mask is white, transparency should be applied
    pixels_to_change = mask == 255

    # Convert the original OpenCV image to PIL for final output with transparency
    final_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGBA))
    datas = final_image.getdata()

    newData: list[tuple[int, int, int, int]] = []
    for item, change in zip(datas, np.nditer(pixels_to_change)):
        if change:
            newData.append((255, 255, 255, 0))  # Making pixel transparent
        else:
            newData.append(item)  # Retaining original pixel

    final_image.putdata(newData)
    final_image.save("output.png")  # Save the final image with transparency

    return final_image
