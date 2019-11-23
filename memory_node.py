import threading
from array import array
from datetime import *
import queue
import socket
import time
import struct
import socket
import packet_builders.local_distributed_packet_builder as local_packet_builder
import node_broadcast
from enum_operation_code import Operation_Code

active_interface_ip = ''
node_id = 0
max_size = 3000000
size_left = 0
metadata_pos = 0
data_pos = max_size
byte_table = []
page_list = []
count_node = 0

def set_id():
    global count_node
    node_id = generate_node_id()
    return node_id


def generate_node_id():
    global count_node

    id = hex(count_node)
    count_node += 1
    return id


def save_page(op_id, page_id, page_size, data):
    global size_left
    added_page = PageData()
    added_page.op_id = op_id
    added_page.page_id = page_id
    added_page.page_size = page_size
    added_page.content = data
    page_list.append(added_page)
    size_left += added_page.page_size

    return size_left

def add_to_table(op_id, page_id, page_size, data):
    global metadata_pos
    global data_pos
    global byte_table
    byte_table[metadata_pos] = op_id
    byte_table[metadata_pos+1] = page_id
    byte_table[metadata_pos+2] = page_size
    byte_table[metadata_pos+3] = data_pos
    metadata_pos += 3
    for aByte in data:
        byte_table[data_pos] = aByte
        data_pos -= 1
  
    metadata_pos += 4

def wrtite_to_file():
    output_file = open('file', 'wb')
    array_to_file = array('d', byte_table)
    array_to_file.tofile(output_file)
    output_file.close()

def read_from_file():
    input_file = open('file', 'rb')
    float_array = array('d')
    float_array.fromstring(input_file.read())

def get_page_content(op_id, page_id):
    for page in page_list:
        if(page.page_id == id and page.op_id == op_id):
            return page

def get_page_size(op_id, page_id):
    for page in page_list:
        if(page.page_id == id and page.op_id == op_id):
            return page.size_left
    return 

class PageData():
    def __init__(self, *args, **kwargs):
        self.op_id = ' '
        self.page_id = 0
        self.page_size = 0
        self.content = []
        self.date_birth = datetime.now()
        self.date_modification = datetime.now()

def start_node():
    HOST = active_interface_ip
    PORT = 5000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen(5)
        size_packet = node_broadcast.create(1,1)
        while True:
            conn, addr = s.accept()
            with conn:
                s.sendto(size_packet, ('<broadcast>', (HOST,PORT)))
                print('Connected by', addr)
                data = conn.recv(1024)
                conn.sendall(data)
                

