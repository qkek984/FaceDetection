from scipy.spatial import distance as dist
from imutils import face_utils
from imutils import paths
import argparse
import dlib
import cv2
import time
import dirInput


class Drowsy:
    def __init__(self, imageList,threshold):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--shape-predictor", required=False, default="./shape_predictor_68_face_landmarks.dat",
                        help="path to facial landmark predictor")
        self.ap.add_argument("-i", "--imageList", required=False,
                             help="image and path", default=imageList)
        self.ap.add_argument("-t", "--threshold", required=False,
                             help="eyes threshold", default=threshold)


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
        startTime = time.time()#running time

        args = vars(self.ap.parse_args())
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(args["shape_predictor"])

        # initialize the frame counter as well as a boolean used to
        # indicate if the alarm is going off

        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        for i, image in enumerate(args["imageList"]):
            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method

            fileName = image[1]
            image = image[0]
            height, width = image.shape[:2]
            #print(height, width)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # detect faces in the grayscale frame
            rects = detector(gray, 0)
            if len(rects) == 0:
                for num in range(15, 360, 15):
                    m1 = cv2.getRotationMatrix2D((width / 2, height / 2), num, 1)
                    rotationImg = cv2.warpAffine(gray, m1, (width, height))
                    rotationRects = detector(rotationImg, 0)
                    if len(rotationRects) != 0:#find eyes
                        rects = rotationRects
                        break;
                if len(rects) == 0:# not found eyes
                    cv2.imwrite('result/nonEyes/' + fileName + '.jpg', image)
                    print(fileName + "\tnon")
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
                if ear < args["threshold"]:
                    # if the eyes were closed for a sufficient number of
                    # then sound the alarm
                    #print("bye----------------:" + str(i))
                    cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imwrite('result/drowsy/' + fileName + '.jpg', image)
                    print(fileName + "\tP")
                # otherwise, the eye aspect ratio is not below the blink
                # threshold, so reset the counter and alarm
                else:
                    ALARM_ON = False
                    cv2.putText(image, "EAR: {:.2f}".format(ear), (300, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imwrite('result/good/' + fileName + '.jpg', image)
                    print(fileName + "\tN")
                    key = cv2.waitKey(1) & 0xFF
                    # if the `q` key was pressed, break from the loop
                    if key == ord("q"):
                        break
                # do a bit of cleanup
                cv2.destroyAllWindows()

        #endTime = time.time() - startTime
        #print("running time"+str(endTime))
    ##########
if __name__=='__main__':
    dirIn = dirInput.DirInput("img")
    imageList = dirIn.dirInput()
    drowsy = Drowsy(imageList,threshold=0.33)
    drowsy.findDrowsy()


##########
