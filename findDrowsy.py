from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from imutils import paths
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

class Drowsy:
    def __init__(self, fileDirectory, imageList):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--shape-predictor", required=False, default="/home/lab/sea/python/imageEnhancement/shape_predictor_68_face_landmarks.dat",
                        help="path to facial landmark predictor")
        if imageList!=None:
            self.imageList = imageList
        else:
            self.imageList = None
            self.ap.add_argument("-i", "--images", required=False,
                            help="path to input directory of images", default=fileDirectory)

    def eye_aspect_ratio(self,eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])

        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear

    def findDrowsy(self):
        args = vars(self.ap.parse_args())
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(args["shape_predictor"])
        EYE_AR_THRESH = 0.35
        EYE_AR_CONSEC_FRAMES = 48

        # initialize the frame counter as well as a boolean used to
        # indicate if the alarm is going off
        COUNTER = 0
        ALARM_ON = False

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
        if self.imageList !=None:
            for i, imagePath in enumerate(self.imageList):
                # load the image, convert it to grayscale, and compute the
                # focus measure of the image using the Variance of Laplacian
                # method
                image = imagePath
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # detect faces in the grayscale frame
                rects = detector(gray, 0)
                if len(rects) == 0:
                    cv2.imwrite('result/good2/' + str(i) + '.jpg', image)
                for rect in rects:
                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    # extract the left and right eye coordinates, then use the
                    # coordinates to compute the eye aspect ratio for both eyes
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]
                    leftEAR = self.eye_aspect_ratio(leftEye)
                    rightEAR = self.eye_aspect_ratio(rightEye)

                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)
                    # check to see if the eye aspect ratio is below the blink
                    # threshold, and if so, increment the blink frame counter
                    if ear < EYE_AR_THRESH:
                        COUNTER += 1
                        # if the eyes were closed for a sufficient number of
                        # then sound the alarm
                        #print("bye----------------:" + str(i))
                        cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imwrite('result/drowsy/' + str(i) + '.jpg', image)
                    # otherwise, the eye aspect ratio is not below the blink
                    # threshold, so reset the counter and alarm
                    else:
                        COUNTER = 0
                        ALARM_ON = False
                        cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.imwrite('result/good/' + str(i) + '.jpg', image)
                        #print("this:" + str(i))

                    key = cv2.waitKey(1) & 0xFF

                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break

                # do a bit of cleanup
                cv2.destroyAllWindows()
        else:
            for i, imagePath in enumerate(paths.list_images(args["images"])):
                # load the image, convert it to grayscale, and compute the
                # focus measure of the image using the Variance of Laplacian
                # method
                #print(imagePath)
                image = cv2.imread(imagePath)
                height, width = image.shape[:2]
                #print(height, width)
                if height > width:
                    image = cv2.resize(image, (1280, 1920))
                else:
                    image = cv2.resize(image, (1920, 1280))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # detect faces in the grayscale frame
                rects = detector(gray, 0)
                if len(rects) == 0:
                    cv2.imwrite('result/good2/' + str(i) + '.jpg', image)
                    print(imagePath+"\tnon")
                for rect in rects:
                    # determine the facial landmarks for the face region, then
                    # convert the facial landmark (x, y)-coordinates to a NumPy
                    # array
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)

                    # extract the left and right eye coordinates, then use the
                    # coordinates to compute the eye aspect ratio for both eyes
                    leftEye = shape[lStart:lEnd]
                    rightEye = shape[rStart:rEnd]
                    leftEAR = self.eye_aspect_ratio(leftEye)
                    rightEAR = self.eye_aspect_ratio(rightEye)

                    # average the eye aspect ratio together for both eyes
                    ear = (leftEAR + rightEAR) / 2.0
                    leftEyeHull = cv2.convexHull(leftEye)
                    rightEyeHull = cv2.convexHull(rightEye)
                    cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
                    cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)
                    # check to see if the eye aspect ratio is below the blink
                    # threshold, and if so, increment the blink frame counter
                    if ear < EYE_AR_THRESH:
                        cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imwrite('result/drowsy/' + str(i) + '.jpg', image)
                        print(imagePath + "\tP")
                    # otherwise, the eye aspect ratio is not below the blink
                    # threshold, so reset the counter and alarm
                    else:
                        cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imwrite('result/good/' + str(i) + '.jpg', image)
                        print(imagePath + "\tN")
                        #print("this:" + str(i))

                        # show the frame
                    # cv2.imshow("Frame", image)

                    key = cv2.waitKey(1) & 0xFF

                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break
                # do a bit of cleanup
                cv2.destroyAllWindows()

##########
if __name__=='__main__':
    drowsy = Drowsy("img",None)
    drowsy.findDrowsy()


##########
