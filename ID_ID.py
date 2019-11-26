import uuid
import socket
import struct
import time
import queue
import threading

import paquete_competir
import paquete_activa

page_location = {}
current_size_nodes = {}


def champions(sock, ronda):
    mac = uuid.getnode().to_bytes(6, 'big')
    timeout = 4

    salir = False
    campeon = False

    start_time = time.time()

    paquete = paquete_competir.crear(ronda)
    sock.sendto(paquete, ('<broadcast>', 6666))

    while True:
        sock.settimeout(timeout)

        try:
            paquete_recv, _ = sock.recvfrom(1024)

            if int(paquete_recv[0]) == 0:
                paquete_recv = paquete_competir.desempaquetar(paquete_recv)
                if paquete_recv[1] == mac:
                    print("Soy yo")
                    continue
                elif (int(paquete_recv[2]) > ronda) or (paquete_recv[1] > mac):
                    print("Perdi")
                    salir = True
                    break
                else:
                    print("Ronda: ", ronda)
                    ronda += 1
                    paquete = paquete_competir.crear(ronda)
                    sock.sendto(paquete, ('<broadcast>', 6666))

            elif int(paquete_recv[0]) == 1:
                guardar_actualizaciones(paquete_activa.desempaquetar(paquete_recv))
                salir = True
                break

            timeout = int(timeout - time.time() - start_time)
            if timeout < 0:
                print("Gane 1")
                campeon = True
                break

        except socket.timeout:
            print("Gane 2")
            campeon = True
            break

        if salir == True:
            break

    return campeon


def recibir_actualizaciones(sock, cola):
    keep_alive_timeout = 4

    while True:
        start_time = time.time()

        sock.settimeout(keep_alive_timeout)

        try:
            paquete_recv, _ = sock.recvfrom(1024)

            if int(paquete_recv[0]) != 2:
                keep_alive_timeout = int(keep_alive_timeout - time.time() - start_time)
            else:
                keep_alive_timeout = 4
                cola.put(paquete_recv)
        except socket.timeout:
            break

        if keep_alive_timeout < 0:
            break

    return


def procesar_actualizaciones(sock, cola):
    global stop

    keep_alive_timeout = 2
    stop = False

    while True:
        try:
            paquete = cola.get(timeout=keep_alive_timeout)
            datos = paquete_activa.desempaquetar(paquete)
            guardar_actualizaciones(datos)
            break
        except queue.Empty:
            if stop == True:
                break
    return


def guardar_actualizaciones(datos):
    pagina_id = 3
    nodo_id = pagina_id + 1
    for _ in range(int(datos[1])):
        page_location[datos[pagina_id]] = datos[nodo_id]
        pagina_id += 2
        nodo_id += 2

    if datos[1] == 0:
        nodo_id = 3
    else:
        nodo_id = pagina_id
    ip = nodo_id + 1
    espacio_disponible = ip + 1
    for _ in range(int(datos[2])):
        current_size_nodes[datos[nodo_id]] = [datos[ip], datos[espacio_disponible]]

    return


def start(id_ml_start, id_nm_start):
    UDP_IP = ""
    UDP_PORT = 6666

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))

    paquetes_pasivos = queue.Queue()

    ronda = 0

    while True:

        resultado = champions(sock, ronda)

        if resultado == True:
            paquete = paquete_activa.crear(op_code=1, numero_paginas=0, numero_nodos=0)
            sock.sendto(paquete, ('<broadcast>', 6666))
            id_ml_start.put(True)
            id_nm_start.put(True)
            # Escuchar por broadcast para agregar ID y NM (recibir_paquetes(), procesar_paquetes())
            # Enviar Keep Alive constantemente (enviar_paquetes())
        else:

            receive_packet_process = threading.Thread(target=recibir_actualizaciones, args=(sock, paquetes_pasivos,))
            process_packet_process = threading.Thread(target=procesar_actualizaciones, args=(sock, paquetes_pasivos,))

            receive_packet_process.start()
            process_packet_process.start()

            receive_packet_process.join()
            process_packet_process.join()

        ronda = 3

    return
