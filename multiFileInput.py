import argparse
import cv2
from imutils import paths
import re

class multiFileInput:
    def __init__(self,filesList):
        ap = argparse.ArgumentParser()
        ap.add_argument("-i", "--imageFiles", required=False,
                        help="path to input directory of images", default=filesList)
        self.args = vars(ap.parse_args())
    def findFileName(self,fileDir):
        pattern = "[\\\\,/]"
        result = re.split(pattern, fileDir)
        result = re.split('\.', result[len(result) - 1])
        return result[0]

    def filesInput(self):
        imageList = []
        for i, imagePath in enumerate(self.args["imageFiles"]):
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
'''
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
'''
if __name__=='__main__':
    mFileInput = multiFileInput(list)
    imageList = mFileInput.filesInput()
    for i, image in enumerate(imageList):
        path = image[1]
        image = image[0]
        height, width = image.shape[:2]
        cv2.imwrite('result/' + path + '.jpg', image)
