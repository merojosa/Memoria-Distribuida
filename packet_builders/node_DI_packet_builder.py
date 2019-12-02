import struct

# unsigned char, unsigned int.
FORMAT = '=BB'

# Create a packet acording to the parameters, is a struct with a specific format (FORMAT)
def create(operation_id, page_id, data):
    return struct.pack(FORMAT, operation_id, page_id, data)

def get_save_format(data_size):
    return FORMAT + str(data_size) + 's'