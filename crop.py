import  cv2, sys
from  matplotlib  import  pyplot as plt
import  numpy as np

image =  cv2.imread(r'cosmetic.jpg' )
image_gray =  cv2.imread(r'cosmetic.jpg' , cv2.IMREAD_GRAYSCALE)

b,g,r =  cv2.split(image)
image2 =  cv2.merge([r,g,b])
 
blur =  cv2.GaussianBlur(image_gray, ksize= ( 5 , 5 ), sigmaX= 0 ) # the ksize value dictates the strength of the blur.
ret, thresh1 =  cv2.threshold(blur,  127 ,  255 , cv2.THRESH_BINARY)

edged =  cv2.Canny(blur,  10 ,  250 )
cv2.imshow( 'Edged' , edged)

kernel =  cv2.getStructuringElement(cv2.MORPH_RECT, ( 7 , 7 ))
closed =  cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) # close off any "holes" in the outline
cv2.imshow( 'closed' , closed)

cv2.imshow( 'image' , image)

contours, _ =  cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
total =  0
contour_image =  cv2.drawContours(image, contours, - 1 , ( 0 , 255 , 0 ),  3 )
cv2.imshow( 'contours_image' , contour_image)


 
cv2.waitKey( 0 )
cv2.destroyAllWindows()