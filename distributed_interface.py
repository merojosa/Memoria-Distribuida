import threading
import queue
import socket
import time

NODES_PORT = 5000

page_location = {}
current_size_nodes = {}


# To a node
def save_page_node(local_queue_packets, ip_node_queue):

    socket_node = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        packet = local_queue_packets.get()
        # Pending process packet acording the protocol
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
def send_packet_local():
	pass


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


def main():

    current_size_nodes["127.0.0.1"] = 100
    
    local_queue_packets = queue.Queue()
    ip_node_queue = queue.Queue()
    metadata_queue = queue.Queue()

    save_page_node_thread = threading.Thread(target=save_page_node, args=(local_queue_packets, ip_node_queue,))
    receive_size_node_thread = threading.Thread(target=receive_packet_node, args=(ip_node_queue,))
    send_packet_local_thread = threading.Thread(target=send_packet_local, args=(ip_node_queue,))

    save_page_node_thread.start()
    receive_size_node_thread.start()

    save_page_node_thread.join()
    receive_size_node_thread.join()

main()