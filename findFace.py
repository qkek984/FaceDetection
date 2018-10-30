# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

import multiFileInput


class FindFace:
    def __init__(self, imageList):
        ap = argparse.ArgumentParser()
        ap.add_argument("-p", "--shape-predictor", required=False, default="./shape_predictor_68_face_landmarks.dat",
                        help="path to facial landmark predictor")
        ap.add_argument("-i", "--imageList", required=False,
                             help="image and path", default=imageList)
        self.args = vars(ap.parse_args())

    def rect_to_bb(rect):
        # take a bounding predicted by dlib and convert it
        # to the format (x, y, w, h) as we would normally do
        # with OpenCV
        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        # return a tuple of (x, y, w, h)
        return (x, y, w, h)

    def shape_to_np(shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coords

    def run(self):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.args["shape_predictor"])
        # load the input image, resize it, and convert it to grayscale
        nextImageList = []

        for i,image in enumerate(self.args["imageList"]):
            fileName = image[1]
            image = image[0]
            height, width = image.shape[:2]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # detect faces in the grayscale image
            rects = detector(gray, 1)
            # loop over the face detections
            for (j, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                # convert dlib's rectangle to a OpenCV-style bounding box
                # [i.e., (x, y, w, h)], then draw the face bounding box
                (x, y, w, h) = face_utils.rect_to_bb(rect)

            # show the output image with the face detections + facial landmarks
            try:
                roi = image[y:y + h, x: x + w]
            except:
                roi = image[0:int(height/2), 0: int(width/2)]
                print("1")
            nextImageList.append([roi, fileName])
            x=y=None
            #cv2.imshow("Output"+str(i), roi)
        #cv2.waitKey(0)
        return nextImageList


if __name__=='__main__':
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    list = ['./img/b0.JPG', './img/d0.JPG', './img/n0.JPG']
    #list = ['C:/Users/Sea/Desktop/jp/samplimg/b0.JPG', 'C:/Users/Sea/Desktop/jp/samplimg/d0.JPG']
    mFileInput = multiFileInput.multiFileInput(list)
    imageList = mFileInput.filesInput()

    findFace = FindFace(imageList=imageList)
    imageList = findFace.run()
    for i, image in enumerate(imageList):
        fileName = image[1]
        image = image[0]
        cv2.imwrite('result/' + fileName + '.jpg', image)

