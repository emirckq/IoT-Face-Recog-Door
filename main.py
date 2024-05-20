import wiringpi as wp
from time import sleep
import cv2
import pickle
import cvzone
import face_recognition

# USE sudo -E /usr/bin/python3 /home/orangepi/Desktop/New-folder-3-/main.py TO RUN THIS SCRIPT.



# GPIO pinlerini tanımla
PIN1 = 3  # WiringPi pin 14 (BCM GPIO 11)
PIN2 = 4  # WiringPi pin 13 (BCM GPIO 27)
PIN3 = 6  # WiringPi pin 15 (BCM GPIO 14)
PIN4 = 9  # WiringPi pin 16 (BCM GPIO 10)

# Röle pinlerini tanımla
RELAY_PIN1 = 16
RELAY_PIN2 = 15
RELAY_PIN3 = 13
RELAY_PIN4 = 10

# GPIO pinlerini çıkış olarak ayarla
wp.wiringPiSetup()
wp.pinMode(PIN1, wp.OUTPUT)
wp.pinMode(PIN2, wp.OUTPUT)
wp.pinMode(PIN3, wp.OUTPUT)
wp.pinMode(PIN4, wp.OUTPUT)

wp.pinMode(RELAY_PIN1, wp.OUTPUT)
wp.pinMode(RELAY_PIN2, wp.OUTPUT)
wp.pinMode(RELAY_PIN3, wp.OUTPUT)
wp.pinMode(RELAY_PIN4, wp.OUTPUT)

# Röleleri açma fonksiyonu
def relay_open(pin):
    wp.digitalWrite(pin, wp.LOW)  # Röle açmak için LOW sinyal gönder

# Röleleri kapama fonksiyonu
def relay_close(pin):
    wp.digitalWrite(pin, wp.HIGH)  # Röle kapatmak için HIGH sinyal gönder

# Röleleri kontrol etme fonksiyonu
def control_relays(open_duration):
    # Röleleri aç
    relay_open(RELAY_PIN1)
    relay_open(RELAY_PIN2)
    relay_open(RELAY_PIN3)
    relay_open(RELAY_PIN4)

    # Belirtilen süre boyunca bekleyin
    sleep(open_duration)

    # Röleleri kapat
    relay_close(RELAY_PIN1)
    relay_close(RELAY_PIN2)
    relay_close(RELAY_PIN3)
    relay_close(RELAY_PIN4)

# Adım dizileri
wave_drive = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]
reverse_wave_drive = list(reversed(wave_drive))

# Adımları ayarlayan fonksiyon
def set_step(pins):
    wp.digitalWrite(PIN1, pins[0])
    wp.digitalWrite(PIN2, pins[1])
    wp.digitalWrite(PIN3, pins[2])
    wp.digitalWrite(PIN4, pins[3])

# Adım motorunu sürmek için fonksiyon
def step_motor(steps, delay, mode):
    for _ in range(steps):
        for step in mode:
            set_step(step)
            sleep(delay)

            # 5 saniye bekleyin
            sleep(5)

# Kamera başlatma
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# Arkaplan resmini yükleme
imgBackground = cv2.imread('resources/background.png')

# Tanınan yüz kodlamalarını yükleme
with open("encode.p", "rb") as file:
    encodeWithId = pickle.load(file)
    file.close()
encodeListKnown, EmIds = encodeWithId

while True:
    success, img = cap.read()
    if not success:
        break

    # Kareyi yeniden boyutlandırma ve RGB'ye dönüştürme
    imgSmall = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)

    # Mevcut karedeki yüz konumlarını ve kodlamalarını bulma
    faceCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurrentFrame = face_recognition.face_encodings(imgSmall, faceCurFrame)

    # Kameranın çerçevesini arkaplan resmi üzerine ekleyin
    imgBackground[162:162 + 480, 55:55 + 640] = img

    for encodeFace, faceLoc in zip(encodeCurrentFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = matches.index(True) if True in matches else -1
        print(matches, faceDis)

        if matchIndex != -1:
            # Eşleşme bulunduğunda röleleri kontrol et
            step_motor(200, 0.005, wave_drive)
            control_relays(5)  # Röleleri 5 saniye boyunca açık tut
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            bbox = 55 + x1, 162 + y1, x2 - x1 , y2 - y1
            cvzone.cornerRect(imgBackground, bbox, rt=0)
            print(EmIds[matchIndex])
        else: 
            step_motor(200, 0.005, reverse_wave_drive)

    # Görüntüleri gösterme
    cv2.imshow("Face Recognition", img)
    cv2.imshow("Background Image", imgBackground)

    # 'q' tuşuna basarak çıkış yapma
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırakma
cap.release()
cv2.destroyAllWindows()
