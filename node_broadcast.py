import struct


# unsigned char, string of 3 bytes, unsigned char, 3 bytes, unsigned char, float.
FORMAT = 'BB'
sequence = 0

# Pending: dealing with date.
# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, size):
    return struct.pack(FORMAT, operation_id, size)
