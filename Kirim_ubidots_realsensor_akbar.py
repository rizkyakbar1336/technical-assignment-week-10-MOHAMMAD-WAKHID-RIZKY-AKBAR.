import RPi.GPIO as GPIO
from time import sleep
import requests
from hx711 import HX711

# Inisialisasi GPIO
GPIO.setmode(GPIO.BCM)

# Konfigurasi GPIO untuk sensor ultrasonik
TRIG_PIN = 17
ECHO_PIN = 18
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Inisialisasi sensor HX711
hx = HX711(dout_pin=5, pd_sck_pin=6)
hx.set_scale_ratio(10)  # Ganti scale_ratio dengan nilai kalibrasi Anda
hx.reset()

# Token dan label perangkat Ubidots
TOKEN = "BBFF-mst0shdDNZmrl135RtDTvnLRX3Gcy9"
DEVICE_LABEL = "mohammad-wakhid-rizky-akbar"  # Ganti dengan label perangkat Anda di Ubidots

def get_voltage_data():
    # Ganti dengan cara Anda membaca data voltage (misalnya ADC atau sensor eksternal)
    voltage = 13.43  # Contoh, ganti dengan nilai sesungguhnya
    return voltage

def get_berat_data():
    berat = hx.get_raw_data_mean()
    return berat

def get_ultrasonik_data():
    GPIO.output(TRIG_PIN, False)
    sleep(0.2)

    GPIO.output(TRIG_PIN, True)
    sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

def update_ubidots(voltage, berat, ultrasonik):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    payload = {
        "voltage": voltage,
        "berat": berat,
        "ultrasonik": ultrasonik
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Data berhasil dikirim ke Ubidots")
    else:
        print("Gagal mengirim data ke Ubidots. Kode status:", response.status_code)

try:
    while True:
        voltage = get_voltage_data()
        berat = get_berat_data()
        ultrasonik = get_ultrasonik_data()
        
        # Kirim data ke Ubidots
        update_ubidots(voltage, berat, ultrasonik)
        
        sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Program terminated.")