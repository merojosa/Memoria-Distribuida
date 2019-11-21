import uuid
import socket
import struct

import paquete_competir
import paquete_activa


def ronda_seleccion(sock, ronda):
    my_mac = uuid.getnode().to_bytes(6, 'big')
    recv_mac = -1
    resultado = True

    while True:
        paquete = paquete_competir.crear(ronda)
        sock.sendto(paquete, ('<broadcast>', 6666))

        while True:
            sock.settimeout(2)

            try:
                paquete_recv, addr = sock.recvfrom(1024)

                op_code = struct.unpack('B', paquete_recv)

                if int(op_code) == 0:
                    paquete_recv = paquete_competir.desempaquetar(paquete_recv)
                    if paquete_recv[1] == my_mac:
                        continue
                    elif int(paquete[2]) > ronda:
                        resultado = False
                        ronda = ronda + 1
                        break
                    else:
                        recv_mac = paquete_recv[1]
                        ronda = ronda + 1
                        break
                elif int(op_code) == 1:
                    resultado = False
                    ronda = ronda + 1
                    break

            except socket.timeout:
                recv_mac = -1
                ronda + ronda + 1
                break

        if resultado == False:
            break
        elif recv_mac == -1:
            break
        elif recv_mac > my_mac:
            resultado = False
            break

    return ronda, resultado


def recibir_paquetes():
    return


def procesar_paquetes():
    return


def enviar_paquetes():
    return


def recibir_actualizaciones():
    return


def procesar_actualizaciones():
    return


def start(id_ml_start, id_nm_start):
    UDP_IP = ""
    UDP_PORT = 6666

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind((UDP_IP, UDP_PORT))

# Preguntar si mientras se compite, no se reciben datos ya que el que gana es el unico que actualiza
# Preguntar por el aumento de ronda
# Preguntar por la MAC -> little

    ronda = 0

    ronda, resultado = ronda_seleccion(sock, ronda)

    if resultado == True:
        # Enviar soy activa
        # Activar ID_ML
        id_ml_start.put(True)
        # Activar ID_MN
        id_nm_start.put(True)
        # Escuchar por broadcast para agregar ID y NM (recibir_paquetes(), procesar_paquetes())
        # Enviar Keep Alive constantemente (enviar_paquetes())
    # else:
        # Esperar cada dos segundos un Keep Alive (recibir_actualizaciones(), procesar_actualizaciones)
        # Ejecutar ronda_seleccion(sock, ronda) al dejar de recibir Keep Alive en 4 segundos

    return
