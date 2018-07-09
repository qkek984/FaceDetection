import cv2
import numpy as np

img = cv2.imread("img/1.jpg")
h,w = img.shape[:2]

m1 = cv2.getRotationMatrix2D((w/2, h/2),45,1)
img1 = cv2.warpAffine(img,m1,(w,h))

cv2.imwrite('img1.jpg',img1)
cv2.waitKey(0)
cv2.destroyAllWindows()


