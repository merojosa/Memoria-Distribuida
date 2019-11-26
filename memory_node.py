import threading
from array import array
from datetime import *
import queue
import socket
import time
import struct
import socket
import queue
import threading

import packet_builders.local_distributed_packet_builder as local_packet_builder
import packet_builders.node_broadcast as node_broadcast
import packet_builders.distributed_node_packet_builder as distributed_node_packet_builder
import packet_builders.node_data_packet_builder as node_data_packet_builder
import packet_builders.node_ok_packet_builder as node_ok_packet_builder

from enum_operation_code import Operation_Code

active_interface_ip = ''
node_id = 0
max_size = 100
size_left = 0
metadata_pos = 0
data_pos = max_size-1
byte_table = strs = [0 for x in range(max_size)]#bytearray(max_size)#" "*max_size
page_list = []
count_node = 0

BC_PORT = 5000

ID_PORT = 2000

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
    add_to_table(op_id, page_id, page_size, data)
    return size_left

def add_to_table(op_id, page_id, page_size, data):
    global metadata_pos
    global data_pos
    global byte_table
    creation_date = datetime.now()
    modification_date = datetime.now()
    # Convert the current date to timestamp.  For getting the datetime again: datetime.datetime.fromtimestamp(timestamp)
    #timestamp = int(time.mktime(current_date.timetuple()))
    crea_time_bytes = int(time.mktime(creation_date.timetuple()))
    mod_date_bytes = int(time.mktime(modification_date.timetuple()))
    
    bytes_data = node_data_packet_builder.create(op_id, page_id, page_size, crea_time_bytes, mod_date_bytes, data_pos)
    print(bytes_data)
    allThis = struct.unpack(node_data_packet_builder.FORMAT, bytes_data)
    print(allThis) 
    for meta_byte in bytes_data:
        byte_table[metadata_pos] = meta_byte
        metadata_pos += 1
    data_bytes = bytearray(data, 'utf-8')
    for aByte in data_bytes:
        byte_table[data_pos] = aByte
        data_pos -= 1
    print(byte_table)
    wrtite_to_file()

def wrtite_to_file():
    output_file = open('file', 'wb')
    array_to_file = array('B', byte_table)
    array_to_file.tofile(output_file)
    output_file.close()

def read_from_file():
    input_file = open('file', 'rb')
    #file_array = array('b')
    file_array = array("B")
    file_array.fromstring(input_file.read())
    print(file_array)
    byte_table = file_array
    print(byte_table)
    input_file.close()
   


def get_data(op_id, page_id):
    read_from_file()
    for i in range(0, metadata_pos, 20):
        if byte_table[i] == op_id and byte_table[i+1] == page_id:
            dataArray = []
            for j in range(i,i+20):
                dataArray.append(byte_table[j])
            print(dataArray)
            pack = node_data_packet_builder.create(dataArray[0],dataArray[1],dataArray[2],dataArray[3],dataArray[4],dataArray[5])
            print (pack)
            print (struct.unpack(node_data_packet_builder.FORMAT, pack))
            #print(struct.unpack(node_data_packet_builder.FORMAT, byte_table[i+20]))
            break



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

def send_size():
    global size_left
    conn, addr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    conn.settimeout(0.2)
    conn.bind(("", 5000))

    size_packet = node_broadcast.create(1 , size_left)
    conn.sendall(size_packet)
    print("size sent")



def send_OK(sock, page_queue_packets):
     while True:
        packet, addr = page_queue_packets.get()
        data = struct.unpack(distributed_node_packet_builder.INITIAL_FORMAT, packet)
        #ok = node_ok_packet_builder.create(t=data[2], sensor_id=data[3], sequence=data[0])


def listen_interface(waiting_queue_packets):
    
    packet, addr = socket.socket.recvfrom(1024)
    waiting_queue_packets.put((packet, addr))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("",ID_PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024)
                initial_values = struct.unpack_from('=BB', data, 1)
                if(initial_values[0] == '0x0'):
                    new_data = struct.unpack(distributed_node_packet_builder.INITIAL_FORMAT , data)
                    waiting_queue_packets.put(new_data[0],new_data[1],new_data[2],new_data[3])  
                if(initial_values[0] == '0x1'):
                    get_data(initial_values[0],initial_values[1])              



def main():

    save_queue_packets = queue.Queue()

     #= queue.Queue()

   # listen_interface(sock, save_queue_packets, socket.gethostname())


#save_page(170,171,24,"ewre")
#save_page(177,178,24,'this')
#get_data(177,178)
#read_from_file()
#save_page(179,180,24,'what')
#read_from_file()

#listen_interface()

add_to_table(111,123,6,'gsdgseg')
read_from_file()
get_data(111,123)