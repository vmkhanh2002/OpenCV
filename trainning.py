import cv2
import numpy as np
import os

from PIL import Image

#the following are to do with this interactive notebook code
%matplotlib inline 
from matplotlib import pyplot as plt # this lets you draw inline pictures in the notebooks
import pylab # this allows you to control figure size 
pylab.rcParams['figure.figsize'] = (10.0, 8.0) # this controls figure size in the notebook

img_dir = "/content/drive/MyDrive/lab3/dataset" 

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("/content/drive/MyDrive/lab3/Cascades/haarcascade_frontalface_default.xml")

def getImageAndLabels(img_dir):
    imagePaths = [os.path.join(img_dir, f) for f in os.listdir(img_dir)]
    faceSamples = []
    ids = []
    
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
        
    return faceSamples, ids

print("\nFace training. please wait...")
faces, ids = getImageAndLabels(img_dir)
recognizer.train(faces, np.array(ids))

recognizer.write("/content/drive/MyDrive/lab3/trainer/trainer.yml")
print("\n{0} faces are learned.".format(len(np.unique(ids))))

base_image = cv2.imread('/content/drive/MyDrive/lab3/Test/TEAM.png')
grey = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))

# this is a pre-trained face cascade
test_image = cv2.imread('/content/drive/MyDrive/lab3/Test/TEAM.png')
face_cascade = cv2.CascadeClassifier('/content/drive/MyDrive/lab3/Cascades/haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(grey, 1.3, 5)
for (x,y,w,h) in faces:
     cv2.rectangle(test_image,(x,y),(x+w,y+h),(255,0,0),2)
plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))

# this is a pre-trained face cascade
test_image = cv2.imread('/content/drive/MyDrive/lab3/Test/TEAM.png')
face_cascade = cv2.CascadeClassifier('/content/drive/MyDrive/lab3/Cascades/haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(grey, 1.3, 5)

font = cv2.FONT_HERSHEY_SIMPLEX



id = 0

names = [' ', 'KHANH', 'KIET', 'SON', 'THAI', 'THAO NGUYEN ']

for (x, y, w, h) in faces:
        cv2.rectangle(test_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(grey[y:y+h, x:x+w])
        
        print(str(id) + " => " + str(confidence))
        if (confidence > 70):
            id = names[id]
            confidence = " {0}".format(round(confidence))

        else:
            id = "unknown"
            confidence = " {0}".format(round(confidence))
        
        cv2.putText(test_image, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(test_image, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

plt.imshow(cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB))
