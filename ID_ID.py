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

# Sirve
def participantes(sock, cola, end):
    
    timeout = 1
    
    while True:
        sock.settimeout(timeout)
        
        try:
            paquete_recv, addrs = sock.recvfrom(1024)
            print(addrs)
            cola.put(paquete_recv)
        
        except socket.timeout:
            if end.empty() == False:
                break
                
    return

# Sirve
def champions(sock, ronda):
    
    cola = queue.Queue()
    end = queue.Queue()

    mac = uuid.getnode().to_bytes(6, 'big')
    salir = False
    campeon = False
    timeout1 = 4
    
    sorteo_process = threading.Thread(target=participantes, args=(sock, cola, end))
    sorteo_process.start()

    paquete = paquete_competir.crear(ronda)
    sock.sendto(paquete, ('<broadcast>', 6666))
    
    start_time = time.time()

    while True:

        try:
            paquete_recv = cola.get(timeout=timeout1)
            print(paquete_recv)

            if int(paquete_recv[0]) == 0:
                
                datos = paquete_competir.desempaquetar(paquete_recv)
                datos_op_code = int(datos[0])
                datos_mac = datos[1]
                datos_ronda = int(datos[2])
                
                if mac == datos_mac:
                    print("Descartando mi propio paquete")
                    continue
                elif (datos_ronda > ronda) or (datos_mac > mac):
                    print("Perdi la champions")
                    salir = True
                    end.put(True)
                    break
                elif (datos_ronda < ronda):
                    print("Avanzando a la ronda: ", ronda)
                    ronda += 1
                    paquete = paquete_competir.crear(ronda)
                    sock.sendto(paquete, ('<broadcast>', 6666))

            elif int(paquete_recv[0]) == 1:
                print(paquete_recv)
                guardar_actualizaciones(paquete_activa.desempaquetar(paquete_recv))
                salir = True
                end.put(True)
                print("Habemus activa")
                break

            timeout1 = int(timeout1 - (time.time() - start_time))
            print(timeout1)
            if timeout1 <= 0:
                print("Gane la champions")
                campeon = True
                salir = True
                end.put(True)
                break

        except queue.Empty:
            print("Gane la champions")
            campeon = True
            salir = True
            end.put(True)
            break

        if salir == True:
            break
            
    sorteo_process.join()

    return campeon

# No sirve
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
            #global stop
            break

        if keep_alive_timeout < 0:
            #global stop
            break

    return

# No sirve
def procesar_actualizaciones(sock, cola):
    global stop_procesar_actualizaciones

    keep_alive_timeout = 2
    stop_procesar_actualizaciones = False

    while True:
        try:
            paquete = cola.get(timeout=keep_alive_timeout)
            datos = paquete_activa.desempaquetar(paquete)
            guardar_actualizaciones(datos)
            break
        except queue.Empty:
            if procesar_actualizaciones == True:
                break
    return

# Igual y sirve
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
