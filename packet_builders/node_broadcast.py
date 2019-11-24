import struct

# unsigned char, unsigned int.
FORMAT = 'BI'
sequence = 0

# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, size):
    return struct.pack(FORMAT, operation_id, size)
