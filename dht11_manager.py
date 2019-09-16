import dht11
import RPi.GPIO as GPIO
import time
import datetime

def get_data():

    PIN = 17

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    # Read data
    instance = dht11.DHT11(PIN)


    result = instance.read()
    if result.is_valid():
        return result.temperature, result.humidity
    else:
        print("Error del dht11 sensor: 1")
        return -1.0, -1.0




