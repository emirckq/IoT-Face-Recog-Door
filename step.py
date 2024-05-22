import wiringpi as wp
import time

# WiringPi pin numaralarını tanımla
PIN1 = 3  # BCM GPIO 11
PIN2 = 4  # BCM GPIO 27
PIN3 = 6  # BCM GPIO 14
PIN4 = 9  # BCM GPIO 10

# GPIO pinlerini ayarla
wp.wiringPiSetup()
wp.pinMode(PIN1, wp.OUTPUT)
wp.pinMode(PIN2, wp.OUTPUT)
wp.pinMode(PIN3, wp.OUTPUT)
wp.pinMode(PIN4, wp.OUTPUT)


seq = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

step_count = len(seq)
wait_time = 0.01  # Adımlar arası bekleme süresi (saniye)

def set_step(w1, w2, w3, w4):
    wp.digitalWrite(PIN1, w1)
    wp.digitalWrite(PIN2, w2)
    wp.digitalWrite(PIN3, w3)
    wp.digitalWrite(PIN4, w4)

def forward(steps):
    for i in range(steps):
        for j in range(step_count):
            set_step(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            time.sleep(wait_time)

def backward(steps):
    for i in range(steps):
        for j in reversed(range(step_count)):
            set_step(seq[j][0], seq[j][1], seq[j][2], seq[j][3])
            time.sleep(wait_time)

try:
    while True:
        steps = int(input("Kaç adım ileri gitmek istiyorsunuz? "))
        forward(steps)
        steps = int(input("Kaç adım geri gitmek istiyorsunuz? "))
        backward(steps)
except KeyboardInterrupt:
    print("Program durduruldu.")
finally:
    wp.digitalWrite(PIN1, 0)
    wp.digitalWrite(PIN2, 0)
    wp.digitalWrite(PIN3, 0)
    wp.digitalWrite(PIN4, 0)
    wp.pinMode(PIN1, wp.INPUT)
    wp.pinMode(PIN2, wp.INPUT)
    wp.pinMode(PIN3, wp.INPUT)
    wp.pinMode(PIN4, wp.INPUT)
