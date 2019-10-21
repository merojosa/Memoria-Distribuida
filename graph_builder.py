# sudo apt install python3-pip
# python3 -m pip install matplotlib

import matplotlib.pyplot as plt

# Pruebas, borrar despues
import datetime
import time
import struct
####

# Pruebas, borrar despues
def lista_generica():
    x = 2
    lista = []

    while x != 0:
        data = 1.0
        current_time = datetime.datetime.now()
        FORMAT = 'If'
        timestamp = int(time.mktime(current_time.timetuple()))
        packet = struct.pack(FORMAT, timestamp, data)
        data = struct.unpack(FORMAT, packet)
        lista.append((str(datetime.datetime.fromtimestamp(data[0])), str(data[1])))
        x -= 1
        time.sleep(1)

    return lista
####


def procesar_datos(lista_datos):
    print(lista_datos[0][0][11:])
    if lista_datos[0][0] < lista_datos[1][0]:
        print("Se vale comparar")
    if '2019-10-21 00:00:01' < '2019-10-22 00:00:00':
        print("Definitivamente se vale comparar")
    return 0, 0


def sumar_horas(lista_horas):
    #lista_horas = ['00:10:00', '00:00:59', '23:59:59']
    total = 0
    for hora in lista_horas:
        h, m, s = map(int, hora.split(":"))
        total += 3600*h + 60*m + s
    print("%02d:%02d:%02d" % (total / 3600, total / 60 % 60, total % 60))


def imprimir_grafico(eje_x, eje_y, label_y, label_x, titulo):
    plt.bar(eje_x, eje_y)
    plt.title(titulo)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()
    return

# x = [5, 2, 1, 4, 7]
# y = ["A", "B", "C", "D", "E"]

# x = [5, 2, 1, 4, 7]
# y = [12, 3, 5, 7, 9]


lista = lista_generica()
procesar_datos(lista)
