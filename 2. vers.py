import cv2
import pickle
import cvzone
import face_recognition
# import numpy as np
# import os
import wiringpi as wp
from time import sleep, time

# Initialize the camera
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
imgBackground = cv2.imread('resources/background.png')

# Load the known face encodings
with open("encode.p", "rb") as file:
    encodeWithId = pickle.load(file)
    encodeListKnown, EmIds = encodeWithId

# Define motor control pins
PIN1 = 14  # WiringPi pin 14 (BCM GPIO 11)
PIN2 = 13  # WiringPi pin 13 (BCM GPIO 27)
PIN3 = 15  # WiringPi pin 15 (BCM GPIO 14)
PIN4 = 16  # WiringPi pin 16 (BCM GPIO 10)


# Setup pins as outputs and input for the sensor
wp.wiringPiSetup()
wp.pinMode(PIN1, wp.OUTPUT)
wp.pinMode(PIN2, wp.OUTPUT)
wp.pinMode(PIN3, wp.OUTPUT)
wp.pinMode(PIN4, wp.OUTPUT)
wp.pinMode(WATER_SENSOR_PIN, wp.INPUT)

# Step sequences
wave_drive = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

full_step = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

def set_step(pins):
    wp.digitalWrite(PIN1, pins[0])
    wp.digitalWrite(PIN2, pins[1])
    wp.digitalWrite(PIN3, pins[2])
    wp.digitalWrite(PIN4, pins[3])

def step_motor(steps, delay, mode):
    for _ in range(steps):
        for step in mode:
            set_step(step)
            sleep(delay)

try:
    water_detected = False
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
                cvzone.cornerRect(imgBackground, bbox, rt=0)
                print(EmIds[matchIndex])

                # Run motor when face is recognized
                print("Face recognized! Running motor.")
                run_time = 20  # seconds
                start_time = time()
                while time() - start_time < run_time:
                    step_motor(1, 0.005, wave_drive)  # Perform one step
                break  # Break the loop after running the motor once

        # Display the images
        cv2.imshow("Face Recognition", img)
        cv2.imshow("Background Image", imgBackground)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program stopped")

finally:
    # Reset the pins
    wp.digitalWrite(PIN1, 0)
    wp.digitalWrite(PIN2, 0)
    wp.digitalWrite(PIN3, 0)
    wp.digitalWrite(PIN4, 0)
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
