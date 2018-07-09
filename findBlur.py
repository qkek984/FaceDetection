# import the necessary packages
from imutils import paths
import argparse
import cv2
import glob
import os

class Blur:
    def __init__(self, fileDirectory):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-i", "--images", required=False,
                        help="path to input directory of images", default=fileDirectory)
        self.ap.add_argument("-t", "--threshold", type=float, default=200.0,
                        help="focus measures that fall below this value will be considered 'blurry'")

    def findBlur(self):
        args = vars(self.ap.parse_args())
        imageList=[]
        for i, imagePath in enumerate(paths.list_images(args["images"])):
            # load the image, convert it to grayscale, and compute the
            # focus measure of the image using the Variance of Laplacian
            # method
            #print(imagePath)
            image = cv2.imread(imagePath)
            try:
                height, width = image.shape[:2]
            except:
                print("except file name : ",imagePath)
            #print(height, width)
            if height > width:
                image = cv2.resize(image, (1280, 1920))
            else:
                image = cv2.resize(image, (1920, 1280))
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
                cv2.imwrite('result/blur/' + str(i) + '.jpg', image)
                print(imagePath+"P")
            else:
                #cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 200),cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
                cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)
                #cv2.imwrite('result/' + str(i) + '.jpg', image)
                imageList.append(image)
                print(imagePath + "N")
            # show the image
            key = cv2.waitKey(0)
        return imageList

# construct the argument parse and parse the arguments

if __name__=='__main__':
    blur = Blur("img")
    imgList = blur.findBlur()
    for i, imagePath in enumerate(imgList):
        image = imagePath
        cv2.imwrite('result/good2/' + str(i) + '.jpg', image)