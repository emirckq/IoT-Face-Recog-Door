import wiringpi as wp
from time import sleep

# GPIO pinlerini tanımla
PIN1 = 16  # WiringPi pin 16 (BCM GPIO 23)
PIN2 = 15  # WiringPi pin 15 (BCM GPIO 22)
PIN3 = 13  # WiringPi pin 13 (BCM GPIO 21)
PIN4 = 10  # WiringPi pin 10 (BCM GPIO 15)

# GPIO pinlerini çıkış olarak ayarla
wp.wiringPiSetup()
wp.pinMode(PIN1, wp.OUTPUT)
wp.pinMode(PIN2, wp.OUTPUT)
wp.pinMode(PIN3, wp.OUTPUT)
wp.pinMode(PIN4, wp.OUTPUT)

# Röle açma fonksiyonu
def relay_open(pin):
    wp.digitalWrite(pin, wp.HIGH)  # Pin değerini yüksek yaparak röleyi aç

# Röle kapatma fonksiyonu
def relay_close(pin):
    wp.digitalWrite(pin, wp.LOW)  # Pin değerini düşük yaparak röleyi kapat

try:
    while True:
        # Röleleri aç
        relay_open(PIN1)
        relay_open(PIN2)
        relay_open(PIN3)
        relay_open(PIN4)
        sleep(0.1)  # 1 saniye bekle

        # Röleleri kapat
        relay_close(PIN1)
        relay_close(PIN2)
        relay_close(PIN3)
        relay_close(PIN4)
        sleep(0.1)  # 1 saniye bekle

except KeyboardInterrupt:
    # Klavyeden Ctrl+C'ye basılınca çalışmayı durdur
    print("Program durduruldu.")
