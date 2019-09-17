
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

        
def crearPaqueteMovimiento(cola_paquetes):
    
    timeout = 1.0
    
    while True:
        # Siempre dura 1 segundo
        movement, current_time = motion_manager.get_data(timeout)
        packetMov = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x01',  sensor_type=0,  data=movement, current_date=current_time)
        cola_paquetes.put(packetMov)

def crearPaqueteDHT11(cola_paquetes):
    
    timeout = 5.0
    
    while True:
        temperature, humidity, current_time = dht11_manager.get_data(timeout)
        
        packetTemp = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x08',  sensor_type=0,  data=temperature, current_date=current_time)
        packetHum = packet_builder.create(team_id=5, sensor_id=b'\x00\x00\x06',  sensor_type=0,  data=humidity, current_date=current_time)
        
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
    UDP_IP = "127.0.0.1"
    UDP_PORT = 6000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 5000

    cola_paquetes = queue.Queue()

    procesoCrearPaqueteMovimiento = threading.Thread(target=crearPaqueteMovimiento, args=(cola_paquetes,))
    procesoCrearPaqueteDHT11 = threading.Thread(target=crearPaqueteDHT11, args=(cola_paquetes,))

    procesoEnviarPaquete = threading.Thread(target=enviarPaquete, args=(sock, SERVER_IP, SERVER_PORT, cola_paquetes,))

    procesoCrearPaqueteMovimiento.start()
    procesoCrearPaqueteDHT11.start()
    procesoEnviarPaquete.start()

    procesoCrearPaqueteMovimiento.join()
    procesoCrearPaqueteDHT11.join()
    procesoEnviarPaquete.join()


main()
