import struct

import datetime
import time

# unsigned char, string of 3 bytes, unsigned char, 3 bytes, unsigned char, float.
FORMAT = 'BIB3sBf'
sequence = 0

# Pending: dealing with date.
# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(sensor_id, sequence):
    return struct.pack(FORMAT, sensor_id, sequence)
    pass