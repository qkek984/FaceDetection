# import the necessary packages
from imutils import paths
import argparse
import cv2
import dirInput
import re

class Blur:
    def __init__(self, imageList,threshold):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-i", "--imageList", required=False,
                             help="image and path", default=imageList)
        self.ap.add_argument("-t", "--threshold", type=float, default=threshold,
                             help="focus measures that fall below this value will be considered 'blurry'")

    def findBlur(self):
        args = vars(self.ap.parse_args())
        nextImageList=[]
        for i, image in enumerate(args["imageList"]):
            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method

            fileName = image[1]
            image = image[0]

            try:
                height, width = image.shape[:2]
            except:
                print("except file name : ",fileName)

            # image = cv2.bilateralFilter(image,10,200,200)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            text = ""#Not Blurry

            # if the focus measure is less than the supplied threshold,
            # then the image should be considered "blurry"
            if fm < args["threshold"]:
                text = "Blurry"
                cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
                cv2.imwrite('result/blur/' + fileName + '.jpg', image)
                print(fileName+"\tP")
            else:
                #cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 200),cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
                cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
                #cv2.imwrite('result/' + str(i) + '.jpg', image)
                nextImageList.append([image,fileName])
                print(fileName + "\tN")

        return nextImageList

# construct the argument parse and parse the arguments

if __name__=='__main__':
    dirIn = dirInput.DirInput("img")
    imageList = dirIn.dirInput()

    blur = Blur(imageList=imageList, threshold=150)
    imageList = blur.findBlur()

    for i, image in enumerate(imageList):
        fileName = image[1]
        image = image[0]
        cv2.imwrite('result/good/' + fileName + '.jpg', image)
