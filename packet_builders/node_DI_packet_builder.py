import struct

# unsigned char, unsigned int.
FORMAT = 'BBIQ'

# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, page_id, size_left, data):
    return struct.pack(FORMAT, operation_id, page_id, size_left, data)
