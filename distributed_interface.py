import threading
import queue
import socket
import time
import struct
import packet_builders.local_distributed_packet_builder as local_packet_builder
from enum_operation_code import Operation_Code

NODES_PORT = 6000

page_location = {}
current_size_nodes = {}

LOCAL_PORT = 5000
LOCAL_IP = '10.1.138.62'


# To a node
def save_page_node(save_packet_queue, ip_node_queue):

    socket_node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        page_id, data_size, data = save_packet_queue.get()
        node_ip = choose_node()
        ip_node_queue.put(node_ip)

        # send message with socket_node...


# From a node
def receive_packet_node(ip_node_queue):
    while True:
        ip_node = ip_node_queue.get()
        # receive size
    pass


# To local memory
def send_packet_local(packet, connection):
    connection.sendall(packet)

# From local memory
def receive_local_packet(local_packet_queue):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_local:

        socket_local.bind(("10.1.139.25", LOCAL_PORT))
        socket_local.listen()

        while True:
            connection, address = socket_local.accept()
            data = connection.recv(1024)
            print(data)
            if(data):
                # To process_local_packet
                local_packet_queue.put(data)
                send_packet_local(b"jeje", connection)


# To distributed interfaces
def broadcast_interfaces(metadata_queue):
	while True:
	    metadata = metadata_queue.get()
	pass

def choose_node():
    biggest_size = -1
    big_ip = None

    for node_id in current_size_nodes:

        if(current_size_nodes[node_id] > biggest_size):
            biggest_size = current_size_nodes[node_id]
            big_ip = node_id

    return big_ip

def process_local_packet(local_packet_queue, save_packet_queue):
    while True:
        packet = local_packet_queue.get()
        data_size = struct.unpack_from(local_packet_builder.INITIAL_FORMAT, packet)[2]
        actual_format = local_packet_builder.get_format(data_size)
        data_tuple = struct.unpack(actual_format, packet)

        if(data_tuple[0] == Operation_Code.SAVE.value):
            save_packet_queue.put( (data_tuple[1], data_tuple[2], data_tuple[3].decode()) )


def main():

    current_size_nodes["127.0.0.1"] = 100

    save_packet_queue = queue.Queue()
    ip_node_queue = queue.Queue()
    local_packet_queue = queue.Queue()

    save_page_node_thread = threading.Thread(target=save_page_node, args=(save_packet_queue, ip_node_queue,))
    receive_size_node_thread = threading.Thread(target=receive_packet_node, args=(ip_node_queue,))
    receive_local_packet_thread = threading.Thread(target=receive_local_packet, args=(local_packet_queue,))
    process_local_packet_therad = threading.Thread(target=process_local_packet, args=(local_packet_queue,save_packet_queue,))

    save_page_node_thread.start()
    receive_size_node_thread.start()
    receive_local_packet_thread.start()
    process_local_packet_therad.start()

    save_page_node_thread.join()
    receive_size_node_thread.join()
    receive_local_packet_thread.join()
    process_local_packet_therad.join()

main()
