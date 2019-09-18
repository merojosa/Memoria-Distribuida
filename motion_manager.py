from datetime import *
import RPi.GPIO as GPIO
from gpiozero import MotionSensor

def get_data(timeout):
    PIN = 4
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pir = MotionSensor(PIN)
    
    t1 = datetime.now()
    
    data = 0.0
    
    current_date = datetime.now()

    while (datetime.now() - t1).seconds <= timeout:

        if pir.motion_detected:
            data = 1.0
            current_date = datetime.now()     

    return data, current_date