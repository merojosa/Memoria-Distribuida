import struct
from enum_operation_code import Operation_Code

# unsigned char (operation code), unsigned int (page id), unsigned int (page size), pending data
INITIAL_FORMAT = 'BII'

def create(operation_code, page_id, data):

    data_size = len(data)
    packet_format = get_format(data_size)

    return struct.pack(packet_format, operation_code, page_id, data_size, data)

def create_packet_to_local(operation_code, page_id, data):
    if(operation_code == Operation_Code.LOAD.value):
        # PENDING
        return struct.pack("BB", operation_code, page_id, data)
    else:
        return struct.pack("BB", operation_code, page_id)


def get_format(size):
    return INITIAL_FORMAT + str(size) + 's'
