import struct
import random

# unsigned char, string of 3 bytes, unsigned char, string of 3 bytes, unsigned char, float.
FORMAT = 'B3sB3sBf'

# Pending: dealing with date.
def create(date, team_id, sensor_id, sensor_type, data):
    return struct.pack(FORMAT, random.randint(0, 200), date, team_id, sensor_id, sensor_type, data)
    pass