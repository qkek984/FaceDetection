# http://flask.pocoo.org/docs/patterns/fileuploads/
from flask import Flask, request, Response
import numpy as np
import cv2
import json
from findBlur import Blur
from findClosedEyes import ClosedEyes
from findFace import FindFace

# Initialize the Flask application


app = Flask(__name__)
global imageenhancement
# route http posts to this method
class imageEnhancement:
    def __init__(self):
        self.image=[]
        self.fileName=[]
        self.imageList=[]
    def getImageList(self):
        return self.imageList
    def removeList(self):
        self.image=[]
        self.fileName=[]
        self.imageList=[]
    def appendImage(self,image):
        self.image.append(image)
        #print("append!",len(self.image))
    def appendFileName(self,fileName):
        self.fileName.append(fileName)
        #print("append F!", len(self.image))
    def veiwImage(self):
        for i,item in enumerate(self.image):
            self.imageList.append([item,self.fileName[i]])
        print(self.imageList)
    def printResult(self,txt2):
        resultTxt=""
        for word in txt2:
            resultTxt += word[0]+" : "+ word[1]+"\n"
        #print(resultTxt)
        return resultTxt
    def runAlgorithm(self,imageList):
        print("------------------------------------------------------------ pre processing")
        findFace = FindFace(imageList=imageList)
        imageList = findFace.run()
        print("------------------------------------------------------------ find blur")
        blur = Blur(imageList=imageList, threshold=150)
        imageList, txt1 = blur.findBlur()
        print(txt1)
        print("------------------------------------------------------------ find drowsy")
        closedEyes = ClosedEyes(imageList=imageList, threshold=0.33)
        txt2 = closedEyes.findClosedEyes()
        #print(txt2)
        return self.printResult(txt1 + txt2)




imageenhancement= imageEnhancement()

@app.route('/image', methods=['POST'])
def getImage():
    global imageenhancement
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    imageenhancement.appendImage(img)
    return "hi"

@app.route('/fileName', methods=['POST'])
def getfileName():
    global imageenhancement
    r = request.json
    #print(r['key'])
    imageenhancement.appendFileName(r['key'])
    return "bye"

@app.route('/done', methods=['POST'])
def getDone():
    global imageenhancement
    imageenhancement.veiwImage()
    resultText = imageenhancement.runAlgorithm(imageenhancement.getImageList())
    imageenhancement.removeList()
    return resultText

# start flask app
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)





'''
import os

import cv2
import numpy as np
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        cvfile = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(cvfile, cv2.IMREAD_COLOR)
        print("h2",img)
        height, width = img.shape[:2]
        print(height, width)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if file and allowed_file(file.filename):
            print ('**found file', file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # for browser, add 'redirect' function on top of 'url_for'
            return url_for('uploaded_file',
                                    filename=filename)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

    return ""

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
'''