import struct

# unsigned char (operation code), unsigned int (page id)
INITIAL_FORMAT = 'BB"

def create_to_node(operation_code, page_id, space, data):

    if(operation_code == Operation_Code.READ.value):
        return struct.pack(INITIAL_FORMAT, operation_code, page_id)
    else:
        data_size = len(data)
        packet_format = get_write_format(data_size)
        return struct.pack(packet_format, operation_code, page_id, data_size, space, data)


def get_write_format(size):
    return INITIAL_FORMAT + 'I' + str(size) + 's'
