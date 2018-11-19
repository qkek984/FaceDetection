# Simple enough, just import everything from tkinter.
from tkinter import filedialog, Frame, Menu, Tk, BOTH, StringVar, Label

import cv2

from findBlur import Blur
from findClosedEyes import ClosedEyes
from findFace import FindFace
from multiFileInput import multiFileInput
import requests
import json

class Window(Frame):
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)
        # reference to the master widget, which is the tk window
        self.master = master
        # with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("GUI")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        # create the file object)
        file = Menu(menu)
        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Upload", command=self.fileUpload)
        file.add_command(label="Exit", command=self.client_exit)
        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)
        # create the file object)

    def fileUpload(self):
        var.set("Wait...")
        files=root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("jpeg files", "*.jpg"), ("jpeg files", "*.jpeg"),("png files", "*.png"),("gif files", "*.gif")), multiple=1)
        self.imageEnhancement(files)

    def imageEnhancement(self,files):
        print(files)
        print("------------------------------------------------------------ dir open")
        mFileInput = multiFileInput(files)
        imageList = mFileInput.filesInput()

        for image in imageList:
            fileName = image[1]
            image=image[0]
            self.putImageRequest(image)
            self.putImageNameRequest(fileName)
        self.doneRequest()


        '''
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
        print(txt2)
        self.printResult(txt1 + txt2)
        '''
    def putImageRequest(self,image):
        addr = 'http://localhost:5000'
        image_url = addr + '/image'

        # prepare headers for http request
        content_type = 'image/jpeg'
        headers = {'content-type': content_type}

        # encode image as jpeg
        _, img_encoded = cv2.imencode('.jpg', image)
        # send http request with image and receive response
        response = requests.post(image_url, data=img_encoded.tostring(), headers=headers)
        #print(response.text)
    def putImageNameRequest(self,fileName):
        addr = 'http://localhost:5000'
        fileName_url = addr + '/fileName'
        data = {'key': fileName}
        response = requests.post(fileName_url, json=data)
        #print(response.text)
    def doneRequest(self):
        addr = 'http://localhost:5000'
        url = addr + '/done'
        data = {'key': 'value'}
        response = requests.post(url, json=data)
        print(response.text)
        var.set(response.text)

    def client_exit(self):
        exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
if __name__=='__main__':
    root = Tk()
    root.geometry("320x240")

    # creation of an instance
    app = Window(root)
    var = StringVar()
    var.set("")
    label = Label(root, textvariable=var, relief='solid',width=320, height=240)
    label.pack()
    # mainloop
    root.mainloop()