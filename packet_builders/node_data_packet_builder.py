import struct

# unsigned char, unsigned char, unsigned int, 3 bytes, 3 bytes, unsigned int.
FORMAT = 'BBIIII'

# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, page_id, size, creation_date, modification_date, data_position):
    return struct.pack(FORMAT, operation_id, page_id, size, creation_date, modification_date, data_position)
