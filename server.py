import ack_builder
import datetime
import file_manager
import packet_builder
import queue
import random
import socket
import struct
import threading


def recibirPaquete(sock, cola_paquetes_espera):
    while True:
        packet, addr = sock.recvfrom(1024)
        cola_paquetes_espera.put((packet, addr))


def procesarPaquete(sock, cola_paquetes_espera, cola_paquetes_procesados):

    ultima_secuencia = -1

    while True:
        packet, addr = cola_paquetes_espera.get()

        data = struct.unpack(packet_builder.FORMAT, packet)
        date = str(datetime.datetime.fromtimestamp(data[1]))
        team_id = str(data[2])
        sensor_id = str(int.from_bytes(data[3], "big"))
        sensor_type = str(data[4])
        data_packet = str(data[5])

        if ultima_secuencia != data[0]:
            file_manager.save_data(date, team_id, sensor_id, sensor_type, data_packet)
            ultima_secuencia = data[0]
            print("Paquete almacenado")
        else:
            print("Paquete descartado")

        cola_paquetes_procesados.put((packet, addr))


def enviarACK(sock, cola_paquetes_procesados):
    while True:
        packet, addr = cola_paquetes_procesados.get()

        data = struct.unpack(packet_builder.FORMAT, packet)
        ack = ack_builder.create(team_id=data[2], sensor_id=data[3], sequence=data[0])

        if random.randint(0, 100) < 100:
            sock.sendto(ack, addr)


def main():
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    cola_paquetes_espera = queue.Queue()
    cola_paquetes_procesados = queue.Queue()

    procesoRecibirPaquete = threading.Thread(target=recibirPaquete, args=(sock, cola_paquetes_espera,))
    procesoProcesarPaquete = threading.Thread(target=procesarPaquete, args=(sock, cola_paquetes_espera, cola_paquetes_procesados,))
    procesoEnviarACK = threading.Thread(target=enviarACK, args=(sock, cola_paquetes_procesados,))

    procesoRecibirPaquete.start()
    procesoProcesarPaquete.start()
    procesoEnviarACK.start()

    procesoRecibirPaquete.join()
    procesoProcesarPaquete.join()
    procesoEnviarACK.join()


main()
