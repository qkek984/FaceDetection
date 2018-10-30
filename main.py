import multiFileInput
import findBlur
import findClosedEyes
list = ['C:/Users/Sea/Desktop/jp/samplimg/b0.JPG', 'C:/Users/Sea/Desktop/jp/samplimg/d0.JPG']
print("------------------------------------------------------------ dir open")

mFileInput = multiFileInput.multiFileInput(list)
imageList = mFileInput.filesInput()
print("------------------------------------------------------------ find blur")
blur = findBlur.Blur(imageList=imageList, threshold=150)
imageList,txt1 = blur.findBlur()
print(txt1)
print("------------------------------------------------------------ find drowsy")
closedEyes = findClosedEyes.ClosedEyes(imageList=imageList, threshold=0.33)
txt2=closedEyes.findClosedEyes()
print(txt2)