import struct
import random

import datetime
import time

# unsigned char, string of 3 bytes, unsigned char, string of 3 bytes, unsigned char, float.
FORMAT = 'BIB3sBf'

# Pending: dealing with date.
# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(team_id, sensor_id, sensor_type, data):

    # Get current date.
    current_date = datetime.datetime.now()

    # Convert the current date to timestamp.  For getting the datetime again: datetime.datetime.fromtimestamp(timestamp)
    timestamp = int(time.mktime(current_date.timetuple()))

    return struct.pack(FORMAT, random.randint(0, 200), timestamp, team_id, sensor_id, sensor_type, data)
    pass