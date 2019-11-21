import struct

DUMP1 = 'BB'
DUMP2 = 'B4sI'
BASE_FORMAT = 'BBB'


def crear(op_code, numero_paginas, numero_nodos, lista_paginas, lista_nodos):
    FORMAT = BASE_FORMAT

    if int(numero_paginas) != 0:
        for x in range(numero_paginas):
            FORMAT = FORMAT + DUMP1

    if int(numero_nodos) != 0:
        for x in range(numero_nodos):
            FORMAT = FORMAT + DUMP2

    if (numero_paginas == 0 and numero_nodos == 0):
        return struct.pack(FORMAT, op_code, numero_paginas, numero_nodos)
    elif (numero_paginas != 0 and numero_nodos != 0):
        return struct.pack(FORMAT, op_code, numero_paginas, numero_nodos, *lista_paginas, *lista_nodos)
    elif numero_nodos != 0:
        return struct.pack(FORMAT, op_code, numero_paginas, numero_nodos, *lista_nodos)
    elif numero_paginas != 0:
        return struct.pack(FORMAT, op_code, numero_paginas, numero_nodos, *lista_paginas)


def desempaquetar(paquete):
    FORMAT = BASE_FORMAT

    datos = struct.unpack(BASE_FORMAT, paquete[:3])

    if int(datos[1]) != 0:
        for x in range(datos[1]):
            FORMAT = FORMAT + DUMP1

    if int(datos[2]) != 0:
        for x in range(datos[2]):
            FORMAT = FORMAT + DUMP2

    return struct.unpack(FORMAT, paquete)
