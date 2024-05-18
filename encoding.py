import cv2
import face_recognition
import pickle
import os

# Path to the folder containing images
folderPath = "images"
modePathList = os.listdir(folderPath)
imgList = []
EmIds = []
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    EmIds.append(os.path.splitext(path)[0])
    # print(os.path.splitext(path)[0])

def yuztanima(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encode = encodes[0]
            encodeList.append(encode)
        else:
            print(f"No face found in image {os.path.basename(path)}")
    return encodeList

# Encode known faces
encodelistKnown = yuztanima(imgList)
encodelistKnownWithIds = [encodelistKnown, EmIds]

with open("encode.p", "wb") as file:
    pickle.dump(encodelistKnownWithIds, file)
    file.close()
print("Encoding complete")
print(EmIds)