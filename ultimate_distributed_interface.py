import uuid
import socket
import struct
import time
import queue
import threading
import os

import active_distributed_interface
import paquete_competir
import paquete_activa

from subprocess import call

TCP_IP = "10.1.138.199"
UDP_IP = '10.164.71.135'
BROADACAST_UDP = "10.164.71.255" 
UDP_PORT = 9876


def obener_metadatos():
    numero_paginas = len(active_distributed_interface.page_location)
    numero_nodos = len(active_distributed_interface.nodes_location)
    lista_paginas = []
    lista_nodos = []

    for i in active_distributed_interface.page_location.keys():
        lista_paginas.append(i)
        lista_paginas.append(active_distributed_interface.page_location[i])

    for i in active_distributed_interface.nodes_location.keys():
        lista_nodos.append(i)
        lista_nodos.append(active_distributed_interface.nodes_location[i])
        lista_nodos.append(active_distributed_interface.current_size_nodes[i])

    return paquete_activa.crear(op_code=1, numero_paginas=numero_paginas, numero_nodos=numero_nodos, lista_paginas=lista_paginas, lista_nodos=lista_nodos)


def guardar_metadatos(datos):
    pagina_id = 3
    nodo_id = pagina_id + 1

    for _ in range(int(datos[1])):
        active_distributed_interface.page_location[datos[pagina_id]] = datos[nodo_id]
        pagina_id += 2
        nodo_id += 2

    if datos[1] == 0:
        nodo_id = 3
    else:
        nodo_id = pagina_id
    ip = nodo_id + 1
    espacio_disponible = ip + 1

    for _ in range(int(datos[2])):
        active_distributed_interface.nodes_location[datos[nodo_id]] = socket.inet_ntoa(datos[ip])
        active_distributed_interface.current_size_nodes[datos[nodo_id]] = datos[espacio_disponible]

    return


def recibir_paquetes(sock, paquetes, fin):

    timeout = 1

    while True:
        sock.settimeout(timeout)

        try:
            paquete_recv, addrs = sock.recvfrom(1024)
            paquetes.put((paquete_recv, addrs))

        except socket.timeout:
            if fin.empty() == False:
                break
    return


def champions(sock, ronda):
    cola_paquetes = queue.Queue()
    cola_finalizar_proceso = queue.Queue()
    direccion_mac = uuid.getnode().to_bytes(6, 'little')
    soy_campeon = False
    tiempo_espera = 4

    hilo_recibir_paquetes = threading.Thread(target=recibir_paquetes, args=(sock, cola_paquetes, cola_finalizar_proceso,))
    hilo_recibir_paquetes.start()

    paquete = paquete_competir.crear(ronda)
    sock.sendto(paquete, (UDP_IP, UDP_PORT))

    while True:

        start_time = time.time()

        try:
            paquete_recibido_completo = cola_paquetes.get(timeout=tiempo_espera)
            paquete_datos = paquete_recibido_completo[0]

            if int(paquete_datos[0]) == 0:
                print("[Champions] Recibiendo datos")
                datos_completos = paquete_competir.desempaquetar(paquete_datos)
                datos_mac = datos_completos[1]
                datos_ronda = int(datos_completos[2])
                print("[Champions] Datos: ", datos_completos)

                if datos_mac == direccion_mac:
                    print("[Champions] Descartando mi propio broadcast")
                    continue

                elif datos_ronda > ronda:
                    print("[Champions] Perdi la champions por tener una ronda menor")
                    soy_campeon = False
                    cola_finalizar_proceso.put(soy_campeon)
                    break

                elif datos_mac > direccion_mac:
                    print("[Champions] Perdi la champions por tener una direccion MAC menor")
                    soy_campeon = False
                    cola_finalizar_proceso.put(soy_campeon)
                    break

                elif datos_ronda < ronda or datos_mac < direccion_mac:
                    ronda += 1
                    print("[Champions] Avanzando a la ronda ", ronda)
                    paquete = paquete_competir.crear(ronda)
                    sock.sendto(paquete, (UDP_IP, UDP_PORT))

            elif int(paquete_datos[0]) == 1:
                print("[Champions] Habemus activa")
                guardar_metadatos(paquete_activa.desempaquetar(paquete_datos))
                soy_campeon = False
                cola_finalizar_proceso.put(soy_campeon)
                break

            tiempo_espera = tiempo_espera - (time.time() - start_time)

            if tiempo_espera <= 0:
                print("[Champions] Gane la champions")
                paquete = obener_metadatos()
                sock.sendto(paquete, (UDP_IP, UDP_PORT))
                soy_campeon = True
                cola_finalizar_proceso.put(soy_campeon)
                break

        except queue.Empty:
            print("[Champions] Gane la champions")
            paquete = obener_metadatos()
            sock.sendto(paquete, (UDP_IP, UDP_PORT))
            soy_campeon = True
            terminar_champions = True
            cola_finalizar_proceso.put(terminar_champions)
            break

    hilo_recibir_paquetes.join()

    return ronda, soy_campeon, tiempo_espera


def tiempo_extra(sock, ronda):
    cola_paquetes = queue.Queue()
    cola_finalizar_proceso = queue.Queue()
    direccion_mac = uuid.getnode().to_bytes(6, 'little')
    direccion_ip = []
    soy_campeon = False
    tiempo_espera = 1

    hilo_recibir_paquetes = threading.Thread(target=recibir_paquetes, args=(sock, cola_paquetes, cola_finalizar_proceso,))
    hilo_recibir_paquetes.start()

    while True:

        start_time = time.time()

        try:
            paquete_recibido_completo = cola_paquetes.get(timeout=tiempo_espera)
            paquete_datos = paquete_recibido_completo[0]
            paquete_addrs = paquete_recibido_completo[1]

            if int(paquete_datos[0]) == 0:
                print("[Tiempo Extra] Recibiendo datos")
                datos_completos = paquete_competir.desempaquetar(paquete_datos)
                datos_mac = datos_completos[1]
                datos_ronda = int(datos_completos[2])
                print("[Tiempo Extra] Datos: ", datos_completos)

                if paquete_addrs in direccion_ip:

                    direccion_ip.remove(paquete_addrs)

                    if datos_mac == direccion_mac:
                        print("[Tiempo Extra] Descartando mi propio broadcast")
                        continue

                    elif datos_ronda > ronda:
                        print("[Tiempo Extra] Perdi la champions por tener una ronda menor")
                        soy_campeon = False
                        cola_finalizar_proceso.put(soy_campeon)
                        break

                    elif datos_mac > direccion_mac:
                        print("[Tiempo Extra] Perdi la champions por tener una direccion MAC menor")
                        soy_campeon = False
                        cola_finalizar_proceso.put(soy_campeon)
                        break

                    elif datos_ronda < ronda or datos_mac < direccion_mac:
                        ronda += 1
                        print("[Tiempo Extra] Avanzando a la ronda ", ronda)
                        paquete = paquete_competir.crear(ronda)
                        sock.sendto(paquete, (UDP_IP, UDP_PORT))

            elif int(paquete_datos[0]) == 1:
                print("[Tiempo Extra] Compitiendo contra: ", paquete_addrs)
                direccion_ip.append(paquete_addrs)
                ronda += 1
                paquete = paquete_competir.crear(ronda)
                sock.sendto(paquete, (UDP_IP, UDP_PORT))

            tiempo_espera = tiempo_espera - (time.time() - start_time)

            if tiempo_espera <= 0:
                print("[Tiempo Extra] Gane la champions")
                paquete = obener_metadatos()
                sock.sendto(paquete, (UDP_IP, UDP_PORT))
                soy_campeon = True
                cola_finalizar_proceso.put(soy_campeon)
                break

        except queue.Empty:
            print("[Tiempo Extra] Gane la champions")
            paquete = obener_metadatos()
            sock.sendto(paquete, (UDP_IP, UDP_PORT))
            soy_campeon = True
            terminar_champions = True
            cola_finalizar_proceso.put(terminar_champions)
            break

    hilo_recibir_paquetes.join()

    return soy_campeon


def recibir_keep_alive(sock, tiempo_espera_restante):
    cola_paquetes = queue.Queue()
    cola_finalizar_proceso = queue.Queue()
    keep_alive_tiempo_espera = 4 + tiempo_espera_restante + 1

    hilo_recibir_paquetes = threading.Thread(target=recibir_paquetes, args=(sock, cola_paquetes, cola_finalizar_proceso,))
    hilo_recibir_paquetes.start()

    print("[Pasiva] Keep alive inicial: ", keep_alive_tiempo_espera)

    while True:

        start_time = time.time()

        try:
            paquete_recibido_completo = cola_paquetes.get(timeout=keep_alive_tiempo_espera)
            paquete_datos = paquete_recibido_completo[0]
            paquete_addrs = paquete_recibido_completo[1]
            print("[Pasiva] Paquete keep alive recibido: ", paquete_datos, paquete_addrs)

            if int(paquete_datos[0]) != 2:
                keep_alive_tiempo_espera = keep_alive_tiempo_espera - (time.time() - start_time)

            else:
                keep_alive_tiempo_espera = 4
                datos = paquete_activa.desempaquetar(paquete_datos)
                guardar_metadatos(datos)

                print("[Pasiva] Tabla de paginas: ", active_distributed_interface.page_location)
                print("[Pasiva] Tabla de nodos: ", active_distributed_interface.nodes_location)
                print("[Pasiva] Tabla de espacio: ", active_distributed_interface.current_size_nodes)


            print("[Pasiva] Keep alive restante: ", keep_alive_tiempo_espera)
            if keep_alive_tiempo_espera <= 0:
                cola_finalizar_proceso.put(True)
                break

        except queue.Empty:
            cola_finalizar_proceso.put(True)
            break

    hilo_recibir_paquetes.join()

    return


def enviar_keep_alive(sock, cola_actualizaciones):
    keep_alive_tiempo_espera = 2

    while True:

        try:
            datos = cola_actualizaciones.get(timeout=keep_alive_tiempo_espera)

            if datos[0] == 0:
                lista_paginas = [datos[1], datos[2]]
                paquete = paquete_activa.crear(op_code=2, numero_paginas=1, numero_nodos=0, lista_paginas=lista_paginas)
                sock.sendto(paquete, (UDP_IP, UDP_PORT))
                print("[Activa] Paquete keep alive enviado: ", paquete)

            elif datos[0] == 1:
                direccion_ip = socket.inet_aton(datos[2])
                lista_nodos = [datos[1], direccion_ip, datos[3]]
                paquete = paquete_activa.crear(op_code=2, numero_paginas=0, numero_nodos=1, lista_nodos=lista_nodos)
                sock.sendto(paquete, (UDP_IP, UDP_PORT))
                print("[Activa] Paquete keep alive enviado: ", paquete)

        except queue.Empty:
            paquete = paquete_activa.crear(op_code=2, numero_paginas=0, numero_nodos=0)
            sock.sendto(paquete, (UDP_IP, UDP_PORT))
            print("[Activa] Paquete keep alive enviado: ", paquete)

    return


def iniciar():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))

    cola_actualizaciones = queue.Queue()

    ronda = 0

    while True:

        ronda, resultado, tiempo_espera_restante = champions(sock, ronda)

        if resultado == True:

            resultado = tiempo_extra(sock, ronda)

            if resultado == True:

                print("[Activa] Adquiriendo IP")

                call(["sudo", "ip", "addr", "flush", "dev", "enp2s0"])
                call(["ip", "a", "add", TCP_IP + "/255.255.0.0", "broadcast", BROADACAST_UDP ,"dev", "enp2s0"])

                print("[Activa] Inicializando servicios")

                hilo_interfaz_distribuida = threading.Thread(target=active_distributed_interface.execute, args=(cola_actualizaciones,))
                hilo_enviar_keep_alive = threading.Thread(target=enviar_keep_alive, args=(sock, cola_actualizaciones,))
                hilo_interfaz_distribuida.start()
                hilo_enviar_keep_alive.start()
                hilo_interfaz_distribuida.join()
                hilo_enviar_keep_alive.join()
                break

        else:
            print("[Pasiva] Inicializando servicios")
            hilo_recibir_keep_alive = threading.Thread(target=recibir_keep_alive, args=(sock, tiempo_espera_restante))
            hilo_recibir_keep_alive.start()
            hilo_recibir_keep_alive.join()
            print("[Pasiva] Limite en el retraso de los paquetes Keep Alive, inicializando champions")

        ronda = 3

    return


iniciar()
