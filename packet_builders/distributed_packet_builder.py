import struct
from enum_operation_code import Operation_Code


# ML-ID-NM
INITIAL_FORMAT = 'BB'   # operation code, page id


def create_read_packet(operation_code, page_id):
    return struct.pack(INITIAL_FORMAT, operation_code, page_id)

def create_save_packet(operation_code, page_id, data_size, data):
    return struct.pack(get_save_format(data_size), operation_code, page_id, data_size, data)

def create_ok_broadcast_packet():
    return struct.pack('B', Operation_Code.OK.value)

def create_ok_local_packet(page_id):
    return struct.pack("BB", Operation_Code.OK.value, page_id)

def get_save_format(data_size):
    return INITIAL_FORMAT + 'I' + str(data_size) + 's'