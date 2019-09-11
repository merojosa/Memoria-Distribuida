import struct

import datetime
import time

# unsigned char, string of 3 bytes, unsigned char, 3 bytes, unsigned char, float.
FORMAT = 'BIB3sBf'
ack = 0

# Pending: dealing with date.
# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(team_id, sensor_id, sensor_type, ack, current_date):
    return struct.pack(FORMAT, team_id, sensor_id, sensor_type)
    pass