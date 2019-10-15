import datetime
import queue
import socket
import struct
import threading
import time

import ack_builder
import file_manager
import packet_builder
from enum_sensor_type import *

def create_motion_packet(queue_packets):

    timeout = 1.0

    while True:
        time.sleep(1.0)

        movement = 1.0
        current_time = datetime.datetime.now()
        packetMov = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x01',  sensor_type=Sensor_Type.MOVEMENT.value,  data=movement, current_date=current_time)
        queue_packets.put(packetMov)

def create_DHT11_packet(queue_packets):

    timeout = 5.0

    while True:
        time.sleep(5.0)
        temperature = 27.42
        humidity = 60.5

        current_time = datetime.datetime.now()


        packetTemp = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x08',  sensor_type=Sensor_Type.TEMPERATURE.value,  data=temperature, current_date=current_time)
        packetHum = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x06',  sensor_type=Sensor_Type.HUMIDITY.value,  data=humidity, current_date=current_time)

        queue_packets.put(packetTemp)
        queue_packets.put(packetHum)


def send_packet(sock, SERVER_IP, SERVER_PORT, queue_packets):
    while True:
        packet = queue_packets.get()
        data = struct.unpack(packet_builder.FORMAT, packet)
        sequence = data[0]
        team_id = data[2]
        sensor_id = data[3]

        while True:

            sock.settimeout(1)

            try:
                sock.sendto(packet, (SERVER_IP, SERVER_PORT))
                ack, addr = sock.recvfrom(1024)

                data = struct.unpack(ack_builder.FORMAT, ack)

                if (sequence == data[0] and team_id == data[1] and sensor_id == data[2] and (SERVER_IP, SERVER_PORT) == addr):
                    print("ACK Correcto")
                    break
                else:
                    print("ACK Incorrecto")

            except socket.timeout:
                print("ACK Timeout")
                continue


def main():
    UDP_IP = "10.1.138.56"
    UDP_PORT = 6000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    SERVER_IP = "10.1.138.56"
    SERVER_PORT = 5000

    queue_packets = queue.Queue()

    create_motion_packet_process = threading.Thread(target=create_motion_packet, args=(queue_packets,))
    create_dht11_packet_process = threading.Thread(target=create_DHT11_packet, args=(queue_packets,))

    send_packet_process = threading.Thread(target=send_packet, args=(sock, SERVER_IP, SERVER_PORT, queue_packets,))

    create_motion_packet_process.start()
    create_dht11_packet_process.start()
    send_packet_process.start()

    create_motion_packet_process.join()
    create_dht11_packet_process.join()
    send_packet_process.join()


main()
