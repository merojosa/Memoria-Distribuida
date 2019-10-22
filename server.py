import datetime
import queue
import random
import socket
import struct
import threading

import ack_builder
import file_manager
import packet_builder
import interface
import graph_menu
from enum_sensor_type import *

def receive_packet(sock, waiting_queue_packets):
    while True:
        packet, addr = sock.recvfrom(1024)
        waiting_queue_packets.put((packet, addr))


def process_packet(sock, waiting_queue_packets, processed_queue_packets):

    addr_list = []
    sequence_list = []

    while True:
        packet, addr = waiting_queue_packets.get()

        try:
            sequence_index = addr_list.index(addr)
        except ValueError:
            addr_list.append(addr)
            sequence_list.append(-1)
            sequence_index = len(sequence_list) - 1

        data = struct.unpack(packet_builder.FORMAT, packet)

        # Eliminar esto una vez que se conecte con la interfaz
        # date = str(datetime.datetime.fromtimestamp(data[1]))
        # team_id = int(data[2])
        # sensor_id = str(int.from_bytes(data[3], "big"))
        # sensor_type = str(data[4])
        # data_packet = str(data[5])
        ####

        date = data[1]
        team_id = data[2]
        sensor_type = data[4]
        data_packet = data[5]

        if sequence_list[sequence_index] != data[0] and Sensor_Type.KEEP_ALIVE.value != data[4]:

            interface.save_data(sensor_type, team_id, date, data_packet)

            # Eliminar esto una vez que se conecte con la interfaz
            # file_manager.save_data(date, team_id, sensor_id, sensor_type, data_packet)
            ####

            sequence_list[sequence_index] = data[0]

        processed_queue_packets.put((packet, addr))


def send_ACK(sock, processed_queue_packets):
    while True:
        packet, addr = processed_queue_packets.get()

        data = struct.unpack(packet_builder.FORMAT, packet)
        ack = ack_builder.create(team_id=data[2], sensor_id=data[3], sequence=data[0])

        if random.randint(0, 100) < 100:
            sock.sendto(ack, addr)


def main():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    waiting_queue_packets = queue.Queue()
    processed_queue_packets = queue.Queue()

    receive_packet_process = threading.Thread(target=receive_packet, args=(sock, waiting_queue_packets,))
    process_packt_process = threading.Thread(target=process_packet, args=(sock, waiting_queue_packets, processed_queue_packets,))
    send_ACK_process = threading.Thread(target=send_ACK, args=(sock, processed_queue_packets,))
    menu_process = threading.Thread(target=graph_menu.menu)

    receive_packet_process.start()
    process_packt_process.start()
    send_ACK_process.start()
    menu_process.start()

    receive_packet_process.join()
    process_packt_process.join()
    send_ACK_process.join()
    menu_process.join()


main()
