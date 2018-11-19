import requests
import json
import cv2

addr = 'http://localhost:5000'

image_url = addr + '/image'
imageName_url = addr + '/imageName'

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('./img/b0.jpg')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(image_url, data=img_encoded.tostring(), headers=headers)
# decode response
'''

content_type = 'application/json'
headers2 = {'content-type': content_type}

data = {'key':'value'}
response = requests.post(imageName_url, json=data)
print(response.text)

print ("submit!")

# expected output: {u'message': u'image received. size=124x124'}
'''
'''
for item in fileDir:
    files = {'file': open(item, 'rb')}
    r = requests.post(url, files=files)
    print(r.text)
'''
