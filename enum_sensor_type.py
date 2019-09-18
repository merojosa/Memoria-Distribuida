import enum

class Sensor_Type(enum.Enum):
    KEEP_ALIVE = 0
    MOVEMENT = 1
    BIG_SOUND = 2
    FOTORESISTOR = 3
    SHOCK = 4
    TOUCH = 5
    HUMIDITY = 6
    BIG_SOUND_INT = 7
    TEMPERATURE = 8
    ULTRASONIC = 9
