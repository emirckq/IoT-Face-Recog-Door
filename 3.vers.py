import wiringpi as wp
from time import sleep
import cv2
import pickle
import cvzone
import face_recognition


relayPins = [16, 15, 13, 10]

PIN1 = 3  # WiringPi pin 14 (BCM GPIO 11)
PIN2 = 4  # WiringPi pin 13 (BCM GPIO 27)
PIN3 = 6  # WiringPi pin 15 (BCM GPIO 14)
PIN4 = 9  # WiringPi pin 16 (BCM GPIO 10)

wp.pinMode(pin, 1)
wp.pinMode(pin2, 1)
for p in relayPins:
    wiringpi.pinMode(p, 1)
def relaySequence(pins):
    for pin in pins:
        wiringpi.digitalWrite(pin, 0)
        time.sleep(1)


wp.wiringPiSetup()
wp.pinMode(PIN1, wp.OUTPUT)
wp.pinMode(PIN2, wp.OUTPUT)
wp.pinMode(PIN3, wp.OUTPUT)
wp.pinMode(PIN4, wp.OUTPUT)

wave_drive = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

reverse_wave_drive = list(reversed(wave_drive))

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



    # Pinleri sıfırlama
    wp.digitalWrite(PIN1, 0)
    wp.digitalWrite(PIN2, 0)
    wp.digitalWrite(PIN3, 0)
    wp.digitalWrite(PIN4, 0)

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
            step_motor(200, 0.005, reverse_wave_drive)
            relaySequence(relayPins)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox =  55 + x1, 162 + y1, x2 - x1 , y2 - y1
            cvzone.cornerRect(imgBackground,bbox, rt=0)
            print(EmIds[matchIndex])
        else: 
            step_motor(200, 0.005, wave_drive)
        


    # Display the images
    cv2.imshow("Face Recognition", img)
    cv2.imshow("Background Image", imgBackground)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
