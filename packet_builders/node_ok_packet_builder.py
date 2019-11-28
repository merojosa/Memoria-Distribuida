import struct

# unsigned char, unsigned int.
FORMAT = '=BB'

# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, page_id, size_left):
    return struct.pack(FORMAT, operation_id, page_id, size_left)
