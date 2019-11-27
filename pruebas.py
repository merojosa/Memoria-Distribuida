import paquete_competir
import paquete_activa
import ID_ID

import uuid
import socket
import struct
import time
import os

def get_hex_mac(mac):
    mac_num = hex(int.from_bytes(mac, 'big')).replace('0x', '').upper()
    mac = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac


def main():

    """
    # MAC en 6 bytes
    mac = uuid.getnode().to_bytes(6, 'big')
    print("MAC en 6 bytes: ", mac)
    print("MAC normal: ", get_hex_mac(mac))

    print()

    # IP en 4 bytes
    ip = socket.inet_aton('192.168.1.1')
    print("IP en 4 bytes: ", ip)
    print("IP normal: ", socket.inet_ntoa(ip))

    print()

    # Quiero Ser
    paquete = paquete_competir.crear(ronda=0)
    unpack_paquete = paquete_competir.desempaquetar(paquete)
    print("Quiero Ser: ", unpack_paquete)

    print()

    # Soy Activa sin datos
    lista_paginas = []
    lista_nodos = []
    paquete = paquete_activa.crear(op_code=1, numero_paginas=0, numero_nodos=0)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Soy Activa sin datos: ", unpack_paquete)

    # Soy Activa con todos los datos
    lista_paginas = [6, 7, 4, 5]
    lista_nodos = [1, ip, 50, 2, ip, 50]
    paquete = paquete_activa.crear(op_code=1, numero_paginas=2, numero_nodos=2, lista_paginas=lista_paginas, lista_nodos=lista_nodos)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Soy Activa con todos los datos: ", unpack_paquete)

    # Soy Activa sin paginas y con nodos
    lista_paginas = []
    lista_nodos = [1, ip, 50, 2, ip, 50]
    paquete = paquete_activa.crear(op_code=1, numero_paginas=0, numero_nodos=2, lista_nodos=lista_nodos)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Soy Activa sin paginas y con nodos: ", unpack_paquete)

    print()

    # Keep Alive sin datos
    lista_paginas = []
    lista_nodos = []
    paquete = paquete_activa.crear(op_code=2, numero_paginas=0, numero_nodos=0, lista_paginas=lista_paginas, lista_nodos=lista_nodos)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Keep Alive sin datos: ", unpack_paquete)

    # Keep Alive con todos los datos
    lista_paginas = [1, 2, 2, 3]
    lista_nodos = [1, ip, 50, 2, ip, 50]
    paquete = paquete_activa.crear(op_code=2, numero_paginas=2, numero_nodos=2, lista_paginas=lista_paginas, lista_nodos=lista_nodos)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Keep Alive con todos los datos: ", unpack_paquete)

    # Keep Alive sin paginas y con nodos
    lista_paginas = []
    lista_nodos = [1, ip, 50, 2, ip, 50]
    paquete = paquete_activa.crear(op_code=2, numero_paginas=0, numero_nodos=2, lista_paginas=lista_paginas, lista_nodos=lista_nodos)
    unpack_paquete = paquete_activa.desempaquetar(paquete)
    print("Keep Alive sin paginas y con nodos: ", unpack_paquete)

    print()
    """

    # Pruebas de socket
    UDP_IP = '192.168.1.255'
    UDP_PORT = 6666

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))
    print(ID_ID.champions(sock, 0))
    
    #os.system("sudo ifconfig eth0 down")
    #os.system("sudo ifconfig eth0 10.1.138.199")
    #os.system("sudo ifconfig wlan0 192.168.1.199")
    #os.system("sudo ifconfig eth0 up")

    
main()
