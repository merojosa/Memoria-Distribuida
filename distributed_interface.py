import uuid
import socket
import struct
import time
import queue
import threading

import active_distributed_interface
import paquete_competir
import paquete_activa

UDP_IP = '10.1.255.255'
UDP_PORT = 6666

def tiempo_extra(sock, ronda):
    
    timeout = 1
    campeon = True
    
    while True:
        sock.settimeout(timeout)
        
        try:
            paquete_recv, addrs = sock.recvfrom(1024)
            
            if int(paquete_recv[0]) == 1: 
                datos = paquete_competir.desempaquetar(paquete_recv)
                datos_mac = datos[1]
                
                if mac == datos_mac:
                    print("Descartando mi propio paquete")
                    continue
                    
                elif datos_mac > mac:
                    print("Perdi la champions en tiempo extra")
                    guardar_actualizaciones(paquete_activa.desempaquetar(paquete_recv))
                    campeon = False
                    break
                    
                else:
                    print("Gane la champions en tiempo extra")
                    paquete = paquete_dump_total()
                    sock.sendto(paquete, (UDP_IP, UDP_PORT))
                    break
        
        except socket.timeout:
            print("Gane la champions en tiempo extra")
            paquete = paquete_dump_total()3
    timeout = 1
    
    while True:
        sock.settimeout(timeout)
        
        try:
            paquete_recv, addrs = sock.recvfrom(1024)
            cola.put(paquete_recv)
        
        except socket.timeout:
            if end.empty() == False:
                break        
    return


def champions(sock, ronda):
    
    cola = queue.Queue()
    end = queue.Queue()

    mac = uuid.getnode().to_bytes(6, 'little')
    salir = False
    campeon = False
    timeout1 = 4
    
    sorteo_process = threading.Thread(target=escuchar_datos, args=(sock, cola, end))
    sorteo_process.start()

    paquete = paquete_competir.crear(ronda)
    sock.sendto(paquete, (UDP_IP, UDP_PORT))
    
    start_time = time.time()

    while True:

        try:
            paquete_recv = cola.get(timeout=timeout1)

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
                    sock.sendto(paquete, (UDP_IP, UDP_PORT))

            elif int(paquete_recv[0]) == 1:
                guardar_actualizaciones(paquete_activa.desempaquetar(paquete_recv))
                salir = True
                end.put(True)
                print("Habemus activa")
                break

            timeout1 = timeout1 - (time.time() - start_time)
            if timeout1 <= 0:
                print("Gane la champions sin tiempo extra")
                paquete = paquete_dump_total()
                sock.sendto(paquete, (UDP_IP, UDP_PORT))
                campeon = True
                salir = True
                end.put(True)
                break

        except queue.Empty:
            print("Gane la champions sin tiempo extra")
            paquete = paquete_dump_total()
            sock.sendto(paquete, (UDP_IP, UDP_PORT))
            campeon = True
            salir = True
            end.put(True)
            break

        if salir == True:
            break
            
    sorteo_process.join()
    
    return ronda, campeon

def paquete_dump_total():
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
    

def guardar_actualizaciones(datos):
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
        active_distributed_interface.nodes_location[datos[nodo_id]] = datos[ip]
        active_distributed_interface.current_size_nodes[datos[nodo_id]] = [espacio_disponible]

    return
    
    
def actualizar_tabla(sock):
    cola = queue.Queue()
    end = queue.Queue()
    
    keep_alive_timeout = 4
    
    datos_process = threading.Thread(target=escuchar_datos, args=(sock, cola, end))
    datos_process.start()
    
    start_time = time.time()

    while True:

        try:
            paquete_recv = cola.get(timeout=keep_alive_timeout)

            if int(paquete_recv[0]) != 2:
                keep_alive_timeout = keep_alive_timeout - (time.time() - start_time)

            else:
                keep_alive_timeout = 4
                datos = paquete_activa.desempaquetar(paquete_recv)
                guardar_actualizaciones(datos)

            if keep_alive_timeout <= 0:
                end.put(True)
                break

        except queue.Empty:
            end.put(True)
            break
            
    datos_process.join()
    
    return
    

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))

    paquetes_pasivos = queue.Queue()
    cola_actualizacion = queue.Queue()

    ronda = 0

    while True:

        ronda, resultado = champions(sock, ronda)

        if resultado == True:
            resultado = tiempo_extra(sock, ronda)
            print("Entrando a tiempo extra")
            if resultado == True:
                # Falta la IP fija
                # os.system("sudo ifconfig eth0 down")
                # os.system("sudo ifconfig eth0 AQUI LA IP FIJA")
                # os.system("sudo ifconfig eth0 up")
                
                # Esto debe ser un hilo
                # active_distributed_interface.execute(cola_actualizacion)
                print("Funciono como activa")
                # Aqui debo actualizar interfaces pasivas
                # Esto debe ser un hilo
                # actualizar_a_los_demas(cola_actualizacion)
                break

        else:
            print("Soy Pasiva")
            receive_packet_process = threading.Thread(target=actualizar_tabla, args=(sock,))
            receive_packet_process.start()
            receive_packet_process.join()
            print("No hay Keep Alive")

        ronda = 3

    return

start()