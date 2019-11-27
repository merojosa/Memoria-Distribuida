import threading
import queue
import socket
import time
import struct
import packet_builders.node_broadcast as node_broadcast_builder
import packet_builders.distributed_packet_builder as distributed_packet_builder
import packet_builders.node_ok_packet_builder as node_ok_packet_builder
from enum_operation_code import Operation_Code

NODES_PORT = 4003
BROADCAST_NODES_PORT = 2224

# page id - node id
page_location = {}

# node id - ip
nodes_location = {}

# node id - size
current_size_nodes = {}


LOCAL_PORT = 2011
MY_IP = '10.1.137.218'

connection_to_local = None


# To given node
def send_packet_node_no_answer(packet, node_ip, node_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        socket_node.connect((node_ip, node_port))

        print("[INTERFAZ ACTIVA] Paquete enviado a nodo, ip: " + node_ip + ", paquete: ", end='')
        print(packet)
        socket_node.sendall(packet)
        socket_node.close()

def send_packet_node_wait_answer(packet, node_ip, node_port):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_node:

        socket_node.connect((node_ip, node_port))

        print("[INTERFAZ ACTIVA] Paquete enviado a nodo, ip: " + node_ip + ", paquete: ", end='')
        print(packet)
        socket_node.sendall(packet)

        answer = socket_node.recv(1024)

        socket_node.close()

        return answer


def enroll_node():
    global current_size_nodes
    global nodes_location

    socket_broadcast_node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket_broadcast_node.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    socket_broadcast_node.bind(("10.1.255.255", BROADCAST_NODES_PORT))
    while True:
        packet, addr = socket_broadcast_node.recvfrom(1024)
        
        data = struct.unpack(node_broadcast_builder.FORMAT, packet)     
        
        # DEBUGGING
        print('[INTERFAZ ACTIVA] Nodo registrado, ip: ' + addr[0] + ', tamanno: ' + str(data[1] ) )

        nodes_location[len(nodes_location)] = addr[0]
        current_size_nodes[len(current_size_nodes)] = data[1]

        send_packet_node_no_answer(distributed_packet_builder.create_ok_broadcast_packet(), addr[0] , NODES_PORT)


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
# Returns ip
def choose_node():
    biggest_size = -1
    big_ip = None

    for node_id in current_size_nodes:

        if(current_size_nodes[node_id] > biggest_size):
            biggest_size = current_size_nodes[node_id]
            big_ip = nodes_location[node_id]

    return big_ip

def process_local_packet(local_packet_queue):
    while True:

        packet = local_packet_queue.get()
        operation_code = struct.unpack_from('B', packet)[0]

        if(operation_code == Operation_Code.SAVE.value):
            # No need to process, is the same packet that needs to be sent
            answer = send_packet_node_wait_answer(packet, choose_node(), NODES_PORT)
            print("[INTERFAZ ACTIVA] Paquete recibido desde NM ", end="")
            print(answer)

            answer_packet = struct.unpack(node_ok_packet_builder.FORMAT, answer)

            # Create an ok packet with given page id and send it to local
            send_packet_local(distributed_packet_builder.create_ok_local_packet(answer_packet[1])

        elif(operation_code == Operation_Code.READ.value):  
            # Where is the page?
            page_id = struct.unpack(distributed_packet_builder.INITIAL_FORMAT, packet)[1]
            node_id = page_location[page_id]
            answer = send_packet_node_wait_answer(packet, nodes_location[node_id], NODES_PORT)
            
            print("[INTERFAZ ACTIVA] Paquete recibido desde NM ", end="")
            print(answer)


def execute():
    local_packet_queue = queue.Queue()

    receive_local_packet_thread = threading.Thread(target=receive_local_packet, args=(local_packet_queue,))
    process_local_packet_thread = threading.Thread(target=process_local_packet, args=(local_packet_queue,))
    enroll_node_thread = threading.Thread(target=enroll_node,)

    receive_local_packet_thread.start()
    process_local_packet_thread.start()
    enroll_node_thread.start()
    
    receive_local_packet_thread.join()
    process_local_packet_thread.join()
    enroll_node_thread.join()

execute()
