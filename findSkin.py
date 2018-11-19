import imutils
import numpy as np
import argparse
import cv2

#lower = np.array([0, 48, 80], dtype="uint8")
#upper = np.array([20, 255, 255], dtype="uint8")
lower = np.array([0, 48, 80])
upper = np.array([20, 255, 255])

img = cv2.imread('img/0.JPG')
height,width = img.shape[:2]

if height>width:
    img = cv2.resize(img, (1280, 1920))
else:
    img = cv2.resize(img, (1920, 1280))

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
skinMask = cv2.inRange(hsv, lower, upper)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations = 5)
skinMask = cv2.dilate(skinMask, kernel, iterations = 5)
#cv2.imwrite('result/skinmask.jpg',skinMask)
image, contours, h = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
maximumArea = 0
bestContour = None
for contour in contours:
    if cv2.contourArea(contour) > 2000:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        #cv2.drawContours(img, [approx], -1, (0, 0, 255), 2)

cv2.imwrite('result/skinmask1.jpg',skinMask)# alpha

skinMask2= cv2.bitwise_not(skinMask)
cv2.imwrite('result/skinmask2.jpg',skinMask2)

re = cv2.bitwise_and(img,img,mask=skinMask)
fore= cv2.medianBlur(re,5)
cv2.imwrite('result/fore.jpg',fore)

#skinMask2 = cv2.dilate(skinMask2, kernel, iterations = 2)
back = cv2.bitwise_and(img,img,mask=skinMask2)
cv2.imwrite('result/back.jpg',back)

####################


#result = cv2.addWeighted(back,0.1,fore,1, 0)#delete
result = cv2.add(fore, back)
cv2.imwrite('result/reslut.jpg',result)
'''
#tmp = np.hstack([img, skin])
#cv2.imwrite('result/r.jpg',tmp)

'''