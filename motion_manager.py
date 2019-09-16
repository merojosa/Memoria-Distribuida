import time
import RPi.GPIO as GPIO
from gpiozero import MotionSensor

def get_data():
    PIN = 4

    timeout = 0.5   # 0.5 second

    timeout_start = time.time()

    GPIO.setmode(GPIO.BCM)
    pir = MotionSensor(PIN)

    # While with a timeout
    while time.time() < timeout_start + timeout:

        if pir.motion_detected:
            return 1.0

    return 0.0
