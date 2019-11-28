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

import packet_builders.distributed_packet_builder as distributed_packet_builder
import packet_builders.node_broadcast as node_broadcast
import packet_builders.node_data_packet_builder as node_data_packet_builder
import packet_builders.node_ok_packet_builder as node_ok_packet_builder
import packet_builders.node_DI_packet_builder as node_DI_packet_builder

from enum_operation_code import Operation_Code

active_interface_ip = ''
node_id = 0
max_size = 1000+8
size_left = 1000
metadata_pos = 8
data_pos = max_size-1
metadata_size = 18
byte_table = [0 for x in range(max_size)]
count_node = 0

BC_PORT = 5000
TCP_PORT = 3114

def set_id():
    global count_node
    node_id = generate_node_id()
    return node_id

def generate_node_id():
    global count_node

    id = hex(count_node)
    count_node += 1
    return id

def save_page(recieved_queue):
    packet = recieved_queue.get()
    print("packffff")
    print(packet)
    op_id = packet[0]
    page_id = packet[1]
    page_size = packet[2]
    data = packet[3]
    global size_left
    global byte_table
    inTable = False
    start_index = 0

    for i in range(8, metadata_pos, metadata_size):
        print(metadata_pos)
        if(op_id == byte_table[i] and page_id == byte_table[i+1]):
            print("f")
            inTable = True
            start_index = i
            print("sta index", start_index)
            break
    if (inTable):
        metadata_array = []
        for i in range(start_index, start_index + metadata_size):
            metadata_array.append(byte_table[i])
        asked_metadata = bytearray(metadata_array)
        processed_metadata = struct.unpack(node_data_packet_builder.FORMAT, asked_metadata)
        #new_size = abs(processed_metadata[2]-page_size)
        #size_left += new_size
        modify_content(op_id, page_id, page_size, data, start_index)
    else:
        size_left += page_size + metadata_size
        add_to_table(op_id, page_id, page_size, data)


def modify_content(op_id, page_id, page_size, data, meta_start):
    global byte_table
    modification_date = datetime.now()
    print(byte_table)
    metadata_array = []
    for i in range(meta_start, meta_start + metadata_size):
        metadata_array.append(byte_table[i])

    asked_metadata = bytearray(metadata_array)
    print("ask meta", asked_metadata)
    processed_metadata = struct.unpack(node_data_packet_builder.FORMAT, asked_metadata)

    print("processed metadata ", processed_metadata)

    data_location = processed_metadata[5]
    mod_date_bytes = int(time.mktime(modification_date.timetuple()))

    new_meta = struct.pack(node_data_packet_builder.FORMAT, op_id, page_id, page_size, processed_metadata[3], mod_date_bytes, data_location)
    #bytes_data = node_data_packet_builder.create(op_id, page_id, page_size, crea_date_bytes, mod_date_bytes, data_pos)
    meta_iter = meta_start
    for meta_byte in new_meta:
        byte_table[meta_iter] = meta_byte
        meta_iter += 1

    data_iter = data_location
    data_bytes = bytearray(data)
    print(data_iter)
    print(data)
    for aByte in data_bytes:
        byte_table[data_iter] = aByte
        data_iter -= 1
    write_to_file()



def add_to_table(op_id, page_id, page_size, data):
    global metadata_pos
    global data_pos
    global byte_table

    creation_date = datetime.now()
    modification_date = datetime.now()

    crea_date_bytes = int(time.mktime(creation_date.timetuple()))
    mod_date_bytes = int(time.mktime(modification_date.timetuple()))
    
    bytes_data = node_data_packet_builder.create(op_id, page_id, page_size, crea_date_bytes, mod_date_bytes, data_pos)
    for meta_byte in bytes_data:
        byte_table[metadata_pos] = meta_byte
        metadata_pos += 1
    #data_bytes = bytearray(data, 'utf-8')

    for aByte in data:
        byte_table[data_pos] = aByte
        data_pos -= 1
    write_to_file()
    read_from_file()


def write_to_file():
    
    global metadata_pos
    global data_pos
    global byte_table
    
    meta_pos_bytes = metadata_pos.to_bytes(4, 'big')
    data_pos_bytes = data_pos.to_bytes(4, 'big')

    for i in range(0,4):
        byte_table[i] = meta_pos_bytes[i]
        byte_table[i+4] = data_pos_bytes[i]
 
    output_file = open('file', 'wb')
    array_to_file = bytes(byte_table)
    output_file.write(array_to_file)
    output_file.close()


def read_from_file():
    global byte_table
    global metadata_pos
    global data_pos
    global size_left
    try:
        input_file = open('file', 'rb')
        try:
            file_array = array("B")
            file_array.fromstring(input_file.read())   
            byte_table = file_array
            meta_pos_bytes = []
            data_pos_bytes = [] 
            for i in range(0,4):
                meta_pos_bytes.append(byte_table[i])
                data_pos_bytes.append(byte_table[i+4])
            metadata_pos = int.from_bytes(meta_pos_bytes, 'big')
            data_pos = int.from_bytes(data_pos_bytes, 'big')
            size_left = data_pos - metadata_pos
            print(byte_table)
        finally:
            input_file.close()
    except:
        print("File not found")

def list_files():
    while True:
        user_input = input()
        type(str(user_input))
        if(user_input == "ls"):
            read_from_file()
            for i in range(8, metadata_pos, metadata_size):
                metadata_array = []
                for j in range(i, i + metadata_size):
                    metadata_array.append(byte_table[j])
                asked_metadata = bytearray(metadata_array)
                processed_metadata = struct.unpack(node_data_packet_builder.FORMAT, asked_metadata)
                print("Codigo de operacion: " + str(processed_metadata[0]) + "  "
                + "Numero de pagina: " + str(processed_metadata[1]) + "  "
                + "Tamanno de pagina: " + str(processed_metadata[2]) + "  "
                + "Fecha de creacion:" + str(datetime.fromtimestamp(processed_metadata[3])) + "  "
                + "Fecha de modificacion:" + str(datetime.fromtimestamp(processed_metadata[4])))


def get_page(op_id, page_id):
    read_from_file()
    begin_meta = 8
    for i in range(begin_meta, metadata_pos, metadata_size):
        print(byte_table[i])
        print(byte_table[i+1])
        if byte_table[i+1] == page_id:
            metadata_array = []
            print (i)
            for j in range(i, i + metadata_size):
                metadata_array.append(byte_table[j])
            asked_metadata = bytearray(metadata_array)
            print(asked_metadata)
            processed_metadata = struct.unpack(node_data_packet_builder.FORMAT, asked_metadata)
            data_size = processed_metadata[2]
            data_array = []
            for k in range(0, data_size):
                data_array.append(byte_table[processed_metadata[5]-k])
            processed_data = bytes(data_array)
            print(processed_metadata[0])
            print(processed_metadata[1])
            node_DI_packet_builder.get_save_format(data_size)
            print("data size", data_size)
            print("format", node_DI_packet_builder.get_save_format(data_size))
            packet_to_send = struct.pack(node_DI_packet_builder.get_save_format(data_size), op_id, processed_metadata[1], processed_data)
            print(struct.unpack(node_DI_packet_builder.get_save_format(data_size),packet_to_send))
            print("sefesgeg", packet_to_send)
            return (packet_to_send)
            

def send_data(op_id, page_id):
    data = node_DI_packet_builder.create(op_id, page_id, "testingYes")
    return data


def send_size(broadcast_queue_packets):
    global size_left
    global byte_table
    my_broadcast  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    my_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    read_from_file()
    while True:
        if not broadcast_queue_packets.empty():
            break
        size_packet = node_broadcast.create(1 , size_left)
        print(size_left)
        print(size_packet)
        my_broadcast.sendto(size_packet, ('10.1.255.255', BC_PORT))
        print("enviado")
        time.sleep(2)


def listen_interface(waiting_queue_packets, ok_queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        s.bind(("10.1.137.45 ",TCP_PORT))
        while True:
            print("breakpoint")
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                
                data = conn.recv(1024)

                print(data)
                initial_values = struct.unpack_from('=B', data)
                print(initial_values[0])
                if(initial_values[0] == 2):

                    ok_queue.put(initial_values[0])
                    
                elif (initial_values[0] == 0):

                    size_array = struct.unpack_from("=BBI", data)
                    print(size_array[2])
                    print(distributed_packet_builder.get_save_format(size_array[2]))
                    new_data = struct.unpack(distributed_packet_builder.get_save_format(size_array[2]) , data)

                    waiting_queue_packets.put((new_data[0],new_data[1],new_data[2],new_data[3])) 
                    save_page(waiting_queue_packets)
                    print(initial_values)

                    ok = node_ok_packet_builder.create(size_array[0], size_array[1], size_left)
                    print(ok)
                    print(addr)
                    print(conn)

                    conn.sendall(ok)
                
                elif (initial_values[0] == 1):
                    print("label ", data)
                    #b'\x01\x01'
                    ok_data = struct.unpack(distributed_packet_builder.INITIAL_FORMAT , data)
                    print(get_page(ok_data[0], ok_data[1]))
                    conn.sendall((get_page(ok_data[0], ok_data[1])))
                    

def main():
    broadcast_queue_packets = queue.Queue()
    save_queue_packets = queue.Queue()
    ok_queue = queue.Queue()

    save_queue_process = threading.Thread(target=listen_interface, args=(save_queue_packets, ok_queue,))
    send_broadcast_process = threading.Thread(target=send_size, args=(ok_queue,))
    listing_process = threading.Thread(target = list_files) 

    send_broadcast_process.start()
    save_queue_process.start()
    listing_process.start()

    send_broadcast_process.join()
    save_queue_process.join()
    listing_process.join()

main()