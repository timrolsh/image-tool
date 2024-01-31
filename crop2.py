import cv2

image = cv2.imread("input/3077207647.jpeg")
edged = cv2.Canny(image, 175, 200)

contours, hierarchy = cv2.findContours(
    edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

cv2.imshow("Show contour", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

for i, c in enumerate(contours):
    rect = cv2.boundingRect(c)
    x, y, w, h = rect
    box = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cropped = image[y : y + h, x : x + w]
    cv2.imshow("Show Boxes", cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("blobby" + str(i) + ".png", cropped)


cv2.imshow("Show Boxes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
