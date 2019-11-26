import threading
import queue
import socket
import time
import struct
import packet_builders.node_broadcast as node_broadcast_builder
import packet_builders.local_distributed_packet_builder as local_packet_builder
from enum_operation_code import Operation_Code

NODES_PORT = 3114
BROADCAST_NODES_PORT = 5000

# page id - node id
page_location = {}

# node id - ip
nodes_location = {}

# node id - size
current_size_nodes = {}


LOCAL_PORT = 2000
MY_IP = '127.0.0.1'

connection_to_local = None


# To a node
def send_packet_node(packet, node_ip):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        node_ip = choose_node()

        socket_node.connect((node_ip, NODES_PORT))
        socket_node.sendall(packet)
    

# From a node
def receive_packet_node():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        socket_node.bind((MY_IP, NODES_PORT))
        socket_node.listen()

        while True:
            conn, addr = socket_node.accept()
            data = conn.recv(1024)

            print(data)

def enroll_node():
    socket_broadcast_node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    socket_broadcast_node.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    socket_broadcast_node.bind(("", BROADCAST_NODES_PORT))
    while True:
        packet, addr = socket_broadcast_node.recvfrom(1024)
        data = struct.unpack(node_broadcast_builder.FORMAT, packet)

        # DEBUGGING
        print('Nodo registrado - id: ' + str(len(nodes_location)) + ' size: ' + str(data[1]) )

        nodes_location[len(nodes_location)] = addr
        current_size_nodes[len(current_size_nodes)] = data[1]


# To local memory
# Note that before it sends a packet, it needs to have a connection_to_local, ie, receive a packet from local.
def send_packet_local(packet):
    global connection_to_local
    print("Enviando a local el paquete ", end='')
    print(packet)
    connection_to_local.sendall(packet)


# From local memory
def receive_local_packet(local_packet_queue):
    global connection_to_local

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_local:

        socket_local.bind((MY_IP, LOCAL_PORT))
        socket_local.listen()

        while True:
            connection_to_local, address = socket_local.accept()

            data = connection_to_local.recv(1024)
            if(data):
                # To process_local_packet
                print(data)
            #    local_packet_queue.put(data)
            #    send_packet_local(local_packet_builder.create_packet_to_local(Operation_Code.OK.value, 1, None))

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
        data_size = struct.unpack_from(local_packet_builder.INITIAL_FORMAT_INTERFACE, packet)[2]
        actual_format = local_packet_builder.get_format(local_packet_builder.INITIAL_FORMAT_INTERFACE, data_size)
        data_tuple = struct.unpack(actual_format, packet)

        print(data_tuple)

        if(data_tuple[0] == Operation_Code.SAVE.value):
            save_packet_queue.put( (data_tuple[1], data_tuple[2], data_tuple[3].decode()) )


def main():
    local_packet_queue = queue.Queue()

    receive_size_node_thread = threading.Thread(target=receive_packet_node)
    receive_local_packet_thread = threading.Thread(target=receive_local_packet, args=(local_packet_queue,))
    process_local_packet_therad = threading.Thread(target=process_local_packet, args=(local_packet_queue,))

    receive_size_node_thread.start()
    receive_local_packet_thread.start()
    process_local_packet_therad.start()

    receive_size_node_thread.join()
    receive_local_packet_thread.join()
    process_local_packet_therad.join()

main()
