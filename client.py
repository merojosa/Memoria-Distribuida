
import datetime
import queue
import socket
import struct
import threading
import time


import ack_builder
import file_manager
import packet_builder
import dht11_manager
import motion_manager


def crearPaquete(cola_paquetes):
    while True:
        # Get how much it takes in seconds.
        start = time.time()
        temperature, humidity = dht11_manager.get_data()
        end = time.time()
        elapsed = end - start

        if(elapsed > 1):
            timeout = 0
        else:
            timeout = 1 - elapsed  # By passing this, it will take exactly 1 second in total to get the data.

        movement = motion_manager.get_data(timeout)

        packetMov = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=temperature)
        packetTemp = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=humidity)
        packetHum = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x03',  sensor_type=0,  data=movement)

        cola_paquetes.put(packetMov)
        cola_paquetes.put(packetTemp)
        cola_paquetes.put(packetHum)


def enviarPaquete(sock, SERVER_IP, SERVER_PORT, cola_paquetes):
    while True:
        packet = cola_paquetes.get()
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
    UDP_IP = "10.1.137.74"
    UDP_PORT = 6000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    SERVER_IP = "10.1.137.45"
    SERVER_PORT = 5000

    cola_paquetes = queue.Queue()

    procesoCrearPaquete = threading.Thread(target=crearPaquete, args=(cola_paquetes,))
    procesoEnviarPaquete = threading.Thread(target=enviarPaquete, args=(sock, SERVER_IP, SERVER_PORT, cola_paquetes,))

    procesoCrearPaquete.start()
    procesoEnviarPaquete.start()

    procesoCrearPaquete.join()
    procesoEnviarPaquete.join()


main()
