from datetime import *
import dht11
import RPi.GPIO as GPIO

def get_data(timeout):

    PIN = 17

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Read data
    instance = dht11.DHT11(PIN)
    
    temp = 0.0
    hum = 0.0
    
    t1 = datetime.now()
    
    while (datetime.now() - t1).seconds <= timeout:

    
        result = instance.read()
        if result.is_valid():
            current_date = datetime.now()
            temp = result.temperature
            hum = result.humidity
            
    return temp, hum, current_date