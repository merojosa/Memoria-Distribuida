import os
import lector_csv
import graph_builder
import interface
import time
import datetime


def menu():
    while True:
        os.system('clear')

        datos_sensores = lector_csv.a_lista('sensores.csv')
        lista_equipos = []
        datos_menu = []

        print("Equipo 404\n")
        print("Graficador\n")

        for j in range(1, len(datos_sensores)):
            if datos_sensores[j][0] not in lista_equipos and datos_sensores[j][0] != "":
                lista_equipos.append(datos_sensores[j][0])
                datos_menu.append(datos_sensores[j][2])

        for i in range(len(datos_menu)):
            print(lista_equipos[i] + " - " + datos_menu[i])

        print(lista_equipos)
        print(datos_menu)

        opcion = input("\nSeleccione una opcion >> ")

        try:
            indice = lista_equipos.index(opcion)
            sub_menu_sensores(opcion, datos_sensores, datos_menu[indice])
        except ValueError:
            continue


def sub_menu_sensores(equipo, datos_sensores, nombre_equipo):
    while True:
        os.system('clear')

        lista_sensores = []
        lista_tipos = []
        datos_menu = []

        print("Equipo 404\n")
        print("Graficador\n")

        for j in range(1, len(datos_sensores)):
            if datos_sensores[j][0] == str(equipo):
                lista_sensores.append(int(datos_sensores[j][4], 16))
                datos_menu.append(datos_sensores[j][5])
                lista_tipos.append(datos_sensores[j][6])

        for i in range(len(datos_menu)):
            print(str(lista_sensores[i]) + " - " + datos_menu[i])

        opcion = input("\nSeleccione una opcion >> ")

        try:
            opcion = int(opcion)
            tipos_index = lista_sensores.index(opcion)
            sub_menu_tiempo(equipo, opcion, lista_tipos[tipos_index], nombre_equipo, datos_menu[tipos_index])
            break
        except ValueError:
            continue
    return


def sub_menu_tiempo(equipo, sensor, tipo, nombre_equipo, nombre_sensor):
    while True:
        os.system('clear')

        lista_opciones = [1, 2, 3]

        print("Equipo 404\n")
        print("Graficador\n")

        print("1 - Minutos")
        print("2 - Horas")
        print("3 - Dias")

        opcion = input("\nSeleccione una opcion >> ")

        try:
            opcion = int(opcion)
            lista_opciones.index(opcion)

            lista_datos = interface.read(int(sensor), int(equipo))

            if len(lista_datos) == 0:
                print("\nNo hay datos disponibles de este sensor")
                time.sleep(3)
            else:
                for x in range (len(lista_datos)):
                    lista_datos[x][0] = str(datetime.datetime.fromtimestamp(int(lista_datos[x][0])))
                    lista_datos[x][1] = float(lista_datos[x][1])
                
                if opcion == 1:
                    eje_x, eje_y = graph_builder.procesar_datos_minuto(lista_datos, tipo)
                elif opcion == 2:
                    eje_x, eje_y = graph_builder.procesar_datos_hora(lista_datos, tipo)
                elif opcion == 3:
                    eje_x, eje_y = graph_builder.procesar_datos_dia(lista_datos, tipo)

                titulo = "Equipo: " + str(nombre_equipo) + "\n" + "Sensor: " + str(nombre_sensor)
                graph_builder.imprimir_grafico_lineas(eje_x, eje_y, "Rango de fechas", "Datos del sensor", titulo)

            break
        except ValueError:
            continue
    return
