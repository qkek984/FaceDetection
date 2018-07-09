import imutils
import numpy as np
import argparse
import cv2

#lower = np.array([0, 48, 80], dtype="uint8")
#upper = np.array([20, 255, 255], dtype="uint8")
lower = np.array([0, 48, 80])
upper = np.array([20, 255, 255])

img = cv2.imread('img/1.JPG')
height,width = img.shape[:2]
print(height, width)
if height>width:
    img = cv2.resize(img, (1280, 1920))
else:
    img = cv2.resize(img, (1920, 1280))
height,width = img.shape[:2]
print(height, width)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
skinMask = cv2.inRange(hsv, lower, upper)
'''
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations = 2)
skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
'''
#skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

image, contours, h = cv2.findContours(skinMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
maximumArea = 0
bestContour = None
for contour in contours:
    if cv2.contourArea(contour) > 2000:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], -1, (0, 0, 255), 2)
        print("zzz")

skin = cv2.bitwise_and(img, img, mask = skinMask)
tmp = np.hstack([img, skin])
cv2.imwrite('resultSkin/r.jpg',tmp)

#img = cv2.bilateralFilter(img,20,200,200)


print("???")