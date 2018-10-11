import argparse
import cv2
from imutils import paths
import re

class DirInput:
    def __init__(self,fileDirectory):
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-i", "--images", required=False,
                        help="path to input directory of images", default=fileDirectory)

    def findFileName(self,fileDir):
        pattern = "[\\\\,/]"
        result = re.split(pattern, fileDir)
        result = re.split('\.', result[len(result) - 1])
        return result[0]

    def dirInput(self):
        args = vars(self.ap.parse_args())
        imageList = []
        for i, imagePath in enumerate(paths.list_images(args["images"])):
            image = cv2.imread(imagePath)
            fileName=self.findFileName(imagePath)
            try:
                height, width = image.shape[:2]
            except:
                print("except file name : ", imagePath)
            if height > width:
                image = cv2.resize(image, (1280, 1920))
            else:
                image = cv2.resize(image, (1920, 1280))
            height, width = image.shape[:2]
            #print(height, width)
            imageList.append([image,fileName])
        print("open success")
        return imageList

if __name__=='__main__':
    dirIn = DirInput("img")
    imageList = dirIn.dirInput()
    for i, image in enumerate(imageList):
        path = image[1]
        image = image[0]
        height, width = image.shape[:2]
        cv2.imwrite('result/' + path + '.jpg', image)
