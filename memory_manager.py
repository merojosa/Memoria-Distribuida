from page_location import *
from datetime import *
import file_manager
import re
import packet_builders.local_distributed_packet_builder as local_packet_builder
import struct
import socket
import time
from enum_operation_code import Operation_Code


page_location = {}
count_page = 0
pages = {}

FLOAT_SIZE = 4
PAGE_SIZE = 12
MAX_PAGES = 4

INTERFACE_PORT = 2000
INTERFACE_IP = '192.168.0.16'
# When a page is created, it's located in primary memory. Return the new page id.
def create_page():
    global count_page
    global page_location

    page_id = generate_page_id()
    page_location[page_id] = Page_Location.PRIMARY.value

    # Convert hex string to int
    if(int(page_id, 16) + 1 > MAX_PAGES):
        swap_old_page()

    # The new page must be in primary memory.
    pages[page_id] = PageInfo()
    return page_id


def generate_page_id():
    global count_page

    id = hex(count_page)
    count_page += 1
    return id


def write(page_id, data_interface):
    global pages
    global page_location

    # Iterate every word with the format %ONE_LETTER{NUMBERS OR LETTERS}.
    # Omits if there are spaces between ONE_LETTER and {NUMBERS OR LETTERS}
    for expression in re.findall(r"%\w{[\w0-9\.]+}", data_interface):
        data_type = expression[1]
        single_data = expression[3:len(expression) - 1]

        if(data_type == 'f' or data_type == 'i'):
            single_data_size = FLOAT_SIZE
        else:
            raise Exception('Tipo de dato desconocido: ' + data_type)

        if(page_location[page_id] == Page_Location.SECONDARY.value):
            swap_from_secondary_to_primary(page_id)

        write_primary(page_id, single_data, single_data_size)

def swap_from_primary_to_secondary(page_id):
    global pages
    global page_location

    # protocol.save_page
    del pages[page_id]
    page_location[page_id] = Page_Location.SECONDARY.value


# The old page goes to secondary to get 4 pages max.
def swap_from_secondary_to_primary(page_id):
    global pages
    global page_location

    swap_old_page()

    pages[page_id] = get_page_data(page_id)
    page_location[page_id] = Page_Location.PRIMARY.value


def write_primary(page_id, data, size):
    global pages

    pages[page_id].content.append(data)
    pages[page_id].current_size += size
    pages[page_id].date_modification = datetime.now()

    if(pages[page_id].current_size >=  PAGE_SIZE):
        swap_from_primary_to_secondary(page_id)


def get_page_data(page_id):
    global pages
    global page_location

    if(page_location[page_id] == Page_Location.PRIMARY.value):
        return pages[page_id].content
    else:
        return None # protocol.get_page_data


def get_pages(page_id_list):

    page_content_list = []

    for id in page_id_list:
        page_content_list.append(get_page_data(id))

    return page_content_list


def swap_old_page():
    # start with the first id
    old_id = next(iter(pages))
    oldest_date = pages[old_id].date_modification

    for id in pages:
        if(pages[id].date_modification < oldest_date):
            oldest_date = pages[id].date_modification
            old_id = id

    swap_from_primary_to_secondary(old_id)

# To interface distributed
def save_page(page_id):

    data_string = convert_list_to_string(pages[page_id].content).encode()
    packet = local_packet_builder.create_packet_to_distributed_interface(operation_code=Operation_Code.SAVE.value, page_id=int(page_id, 16), data=data_string)
    socket_interface = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            socket_interface.connect((INTERFACE_IP, INTERFACE_PORT))
            socket_interface.sendall(packet)
            data = socket_interface.recv(1024)
            print(data)
            socket_interface.close()
            break
        except socket.error:
            time.sleep(2)
            continue


def convert_list_to_string(list):
    return ' '.join(list)

def convert_string_to_list(string):
    return string.split()


class PageInfo():
    def __init__(self, *args, **kwargs):
        self.current_size = 0
        self.content = []
        self.date_modification = datetime.now()