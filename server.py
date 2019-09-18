import datetime
import queue
import random
import socket
import struct
import threading

import ack_builder
import file_manager
import packet_builder


def receive_packet(sock, waiting_queue_packets):
    while True:
        packet, addr = sock.recvfrom(1024)
        waiting_queue_packets.put((packet, addr))


def process_packet(sock, waiting_queue_packets, processed_queue_packets):

    last_sequence = -1

    while True:
        packet, addr = waiting_queue_packets.get()

        data = struct.unpack(packet_builder.FORMAT, packet)
        date = str(datetime.datetime.fromtimestamp(data[1]))
        team_id = int(data[2])
        sensor_id = str(int.from_bytes(data[3], "big"))
        sensor_type = str(data[4])
        data_packet = str(data[5])

        if last_sequence != data[0]:
            file_manager.save_data(date, team_id, sensor_id, sensor_type, data_packet)
            last_sequence = data[0]
            print("Paquete almacenado")
        else:
            print("Paquete descartado")

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

    receive_packet_process.start()
    process_packt_process.start()
    send_ACK_process.start()

    receive_packet_process.join()
    process_packt_process.join()
    send_ACK_process.join()


main()
