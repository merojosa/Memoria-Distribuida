import threading
import queue
import socket
import time
import struct
import packet_builders.node_broadcast as node_broadcast_builder
import packet_builders.distributed_packet_builder as distributed_packet_builder
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
MY_IP = '192.168.1.142'

connection_to_local = None


# To given node
def send_packet_node(packet, node_ip, node_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        node_ip = choose_node()

        socket_node.connect((node_ip, node_port))

        print("[INTERFAZ ACTIVA] Paquete enviado a nodo, ip: " + str(node_ip) + ", paquete: ", end='')
        print(packet)
        socket_node.sendall(packet)
    

# From a node
def receive_packet_node():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        socket_node.bind((MY_IP, NODES_PORT))
        socket_node.listen()

        while True:
            conn, addr = socket_node.accept()
            packet = conn.recv(1024)
            
            # DEBUGGING
            print("[INTERFAZ ACTIVA] Paquete recibido desde NM, ip: " + addr + ", paquete: ", end='')
            print(packet)

            data_tuple = struct.unpack_from(distributed_packet_builder.INITIAL_FORMAT, packet)

            operation_code = data_tuple[0]
            page_id = data_tuple[1]

            if(operation_code == Operation_Code.OK.value):

                # Update size
                size = struct.unpack_from(distributed_packet_builder.INITIAL_FORMAT + "I", packet)[2]
                node_id = page_location[page_id]
                current_size_nodes[node_id] = size

                new_packet = distributed_packet_builder.create_ok_local_packet(page_id=page_id)
                send_packet_local(new_packet)

            elif(operation_code == Operation_Code.SEND.value):

                send_packet_local(packet)


def enroll_node():
    socket_broadcast_node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    socket_broadcast_node.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    socket_broadcast_node.bind(("", BROADCAST_NODES_PORT))

    while True:
        packet, addr = socket_broadcast_node.recvfrom(1024)
        data = struct.unpack(node_broadcast_builder.FORMAT, packet)

        # DEBUGGING
        print('[INTERFAZ ACTIVA] Nodo registrado, ip: ' + addr + ', tamanno: ' + str(data[1]) )

        nodes_location[len(nodes_location)] = addr
        current_size_nodes[len(current_size_nodes)] = data[1]

        send_packet_node(distributed_packet_builder.create_ok_broadcast_packet(), addr , BROADCAST_NODES_PORT)        


# To local memory
# Note that before it sends a packet, it needs to have a connection_to_local, ie, receive a packet from local.
def send_packet_local(packet):
    global connection_to_local
    print("[INTERFAZ ACTIVA] Respuesta a local, paquete: ", end='')
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
                print("[INTERFAZ ACTIVA] Paquete recibido desde ML, paquete: ", end='')
                print(data)
                local_packet_queue.put(data)

def choose_node():
    biggest_size = -1
    big_ip = None

    for node_id in current_size_nodes:

        if(current_size_nodes[node_id] > biggest_size):
            biggest_size = current_size_nodes[node_id]
            big_ip = node_id

    return big_ip

def process_local_packet(local_packet_queue):
    while True:

        packet = local_packet_queue.get()
        operation_code = struct.unpack_from('B', packet)[0]

        if(operation_code == Operation_Code.SAVE.value):
            # No need to process, is the same packet that needs to be sent
            send_packet_node(packet, choose_node(), NODES_PORT)

        elif(operation_code == Operation_Code.READ.value):  
            # Where is the page?
            page_id = struct.unpack(distributed_packet_builder.INITIAL_FORMAT, packet)[1]
            node_id = page_location[page_id]
            send_packet_node(packet, nodes_location[node_id], NODES_PORT)

def execute():
    local_packet_queue = queue.Queue()

    receive_packet_node_thread = threading.Thread(target=receive_packet_node)
    receive_local_packet_thread = threading.Thread(target=receive_local_packet, args=(local_packet_queue,))
    process_local_packet_thread = threading.Thread(target=process_local_packet, args=(local_packet_queue,))
    enroll_node_thread = threading.Thread(target=enroll_node,)

    receive_packet_node_thread.start()
    receive_local_packet_thread.start()
    process_local_packet_thread.start()
    enroll_node_thread.start()
    
    receive_packet_node_thread.join()
    receive_local_packet_thread.join()
    process_local_packet_thread.join()
    enroll_node_thread.join()

