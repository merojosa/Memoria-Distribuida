import os
import lector_csv
import graph_builder
import interface

def menu():
    while True:
        os.system('clear')

        # Eliminar esto una vez que se conecte con la interfaz
        lista_equipos = [5, 6]
        ####

        datos_sensores = lector_csv.a_lista('sensores.csv')
        datos_menu = []

        print("Equipo 404\n")
        print("Graficador\n")
        print("Lista de equipos con datos disponibles\n")

        if len(lista_equipos) == 0:
            print("No hay datos de ningun equipo disponible")

        for i in lista_equipos:
            for j in range(1, len(datos_sensores)):
                if str(i) == datos_sensores[j][0]:
                    datos_menu.append(datos_sensores[j][2])
                    break

        for i in range(len(datos_menu)):
            print(str(lista_equipos[i]) + " - " + datos_menu[i])

        print("\nPrecione cualquier otra tecla para refrescar la lista de equipos disponible")

        opcion = input("\nSeleccione una opcion >> ")

        try:
            opcion = int(opcion)
            if opcion != 0:
                lista_equipos.index(opcion)
                sub_menu_sensores(opcion, datos_sensores)
        except ValueError:
            continue


def sub_menu_sensores(equipo, datos_sensores):
    while True:
        os.system('clear')

        # Eliminar esto una vez que se conecte con la interfaz
        lista_sensores = [1, 6, 8]
        lista_tipos = []
        ####

        datos_menu = []

        print("Equipo 404\n")
        print("Graficador\n")
        print("Lista de sensores disponibles\n")

        for i in lista_sensores:
            for j in range(1, len(datos_sensores)):
                dato = str(datos_sensores[j][4])
                if dato != '':
                    numero = int(dato, 16)
                    if i == numero:
                        datos_menu.append(datos_sensores[j][5])
                        lista_tipos.append(datos_sensores[j][6])
                        break

        for i in range(len(datos_menu)):
            print(str(lista_sensores[i]) + " - " + datos_menu[i])
        
        print("\nPrecione cualquier otra tecla para refrescar la lista de equipos disponible")

        opcion = input("\nSeleccione una opcion >> ")

        try:
            opcion = int(opcion)
            tipos_index = lista_sensores.index(opcion)

            # Pedimos los datos del sensor a la interfaz
            # lista_datos = interface.get_data(equipo, opcion)

            # Mandamos a dividir e imprimir los datos
            # eje_x, eje_y = graph_builder.procesar_datos(lista_datos, lista_tipos[tipos_index])
            # graph_builder.imprimir_grafico(eje_x, eje_x)

            break
        except ValueError:
            continue
    return


menu()
