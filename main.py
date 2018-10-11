import dirInput
import findBlur
import findDrowsy

print("------------------------------------------------------------ dir open")
dirIn = dirInput.DirInput("img")
imageList = dirIn.dirInput()
print("------------------------------------------------------------ find blur")
blur = findBlur.Blur(imageList=imageList, threshold=150)
imageList = blur.findBlur()
print("------------------------------------------------------------ find drowsy")
drowsy = findDrowsy.Drowsy(imageList=imageList, threshold=0.33)
drowsy.findDrowsy()