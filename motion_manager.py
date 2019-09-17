import time
import RPi.GPIO as GPIO
from gpiozero import MotionSensor

def get_data(seconds_timeout):
    PIN = 4

    timeout_start = time.time()

    GPIO.setmode(GPIO.BCM)
    pir = MotionSensor(PIN)

    # While with a timeout
    while time.time() < timeout_start + seconds_timeout:
        time.sleep(0.01) # Not to overwhelm.
        if pir.motion_detected:
            return 1.0

    return 0.0
