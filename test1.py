import time
import cv2
import pickle
import cvzone
import face_recognition
import numpy
import os

# Initialize the camera
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
imgBackground = cv2.imread('resources/background.png')

# Load the known face encodings
with open("encode.p", "rb") as file:
    encodeWithId = pickle.load(file)
    file.close()
    encodeListKnown, EmIds = encodeWithId

while True:
    success, img = cap.read()
    if not success:
        break

    # Resize and convert the frame to RGB
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Find face locations and encodings in the current frame
    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    # Overlay the camera frame onto the background image
    imgBackground[162:162 + 480, 55:55 + 640] = img

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = matches.index(True) if True in matches else -1
        print(matches, faceDis)

        if matchIndex != -1:
            # If a match is found, handle it here (e.g., display name, draw box)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox =  55 + x1, 162 + y1, x2 - x1 , y2 - y1
            cvzone.cornerRect(imgBackground,bbox, rt=0)
            print(EmIds[matchIndex])
            pass


    # Display the images
    cv2.imshow("Face Recognition", img)
    cv2.imshow("Background Image", imgBackground)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
