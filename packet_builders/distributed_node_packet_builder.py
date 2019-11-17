import struct

# unsigned char (operation code), unsigned int (page id), unsigned int (page size), space, pending data
INITIAL_FORMAT = 'BIIQ'

def create(operation_code, page_id, space, data):

    data_size = len(data)
    packet_format = get_format(data_size)

    return struct.pack(packet_format, operation_code, page_id, data_size, space, data)


def get_format(size):
    return INITIAL_FORMAT + str(size) + 's' 
