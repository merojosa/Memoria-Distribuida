import RPi.GPIO as GPIO
import dht11
import time
import datetime

def get_data():

    PIN = 17

    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BCM)

    # Read data
    instance = dht11.DHT11(PIN)

    try:
        result = instance.read()
	    if result.is_valid():
	        print("Temperature: %-3.1f C" % result.temperature)
	        print("Humidity: %-3.1f %%" % result.humidity)
            return result.temperature, result.humidity
        else:
            print("Error del dht11 sensor: 1")

        # Every 1 second get data
	    time.sleep(1)

    GPIO.cleanup()
