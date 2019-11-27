import struct
import uuid

FORMAT = 'B6sB'


def crear(ronda):
    mac = uuid.getnode().to_bytes(6, 'big')
    return struct.pack(FORMAT, 0, mac, ronda)


def desempaquetar(paquete):
    return struct.unpack(FORMAT, paquete)
