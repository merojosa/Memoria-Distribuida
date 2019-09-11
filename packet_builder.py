import struct
import random

import datetime
import time

# unsigned char, string of 3 bytes, unsigned char, string of 3 bytes, unsigned char, float.
FORMAT = 'BIB3sBf'
last_sequence = 0

# Pending: dealing with date.
# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(team_id, sensor_id, sensor_type, data):

    global last_sequence

    # Get current date.
    current_date = datetime.datetime.now()

    # Convert the current date to timestamp.  For getting the datetime again: datetime.datetime.fromtimestamp(timestamp)
    timestamp = int(time.mktime(current_date.timetuple()))

    # Not to repeat a consecutive random number.
    new_sequence = random.randint(0, 200)
    while (new_sequence == last_sequence):
        new_sequence = random.randint(0, 200)
    last_sequence = new_sequence

    return struct.pack(FORMAT, new_sequence, timestamp, team_id, sensor_id, sensor_type, data)
    pass