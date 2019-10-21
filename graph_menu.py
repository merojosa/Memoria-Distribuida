import os
import lector_csv
import graph_builder


def menu():
    os.system('clear')

    # Solicitamos todos los datos disponibles de los equipos
    # lista_equipos = interfaz.get_equipos()

    # Eliminar esto una vez que se conecte con la interfaz
    lista_equipos = [1, 2, 3, 4, 5, 6]
    ####

    datos_sensores = lector_csv.a_lista('sensores.csv')
    datos_menu = []

    print("Equipo 404\n")
    print("Graficador\n")
    print("Lista de equipos con datos disponibles\n")

    print("0 - Refrescar la lista de equipos")

    if len(lista_equipos) == 0:
        print("No hay datos de ningun equipo disponible")

    for i in lista_equipos:
        for j in range(1, len(datos_sensores)):
            if str(i) == datos_sensores[j][0]:
                datos_menu.append(datos_sensores[j][2])
                break

    for i in range(len(datos_menu)):
        print(str(i + 1) + " - " + datos_menu[i])

    opcion = input("\nSeleccione un numero >> ")

    try:
        opcion = int(opcion)
    except ValueError:
        menu()

    try:
        lista_equipos.index(opcion)
    except ValueError:
        menu()

    sub_menu_sensores(opcion, datos_sensores)
    menu()


def sub_menu_sensores(equipo, datos_sensores):
    os.system('clear')

    # Solicitamos todos los datos disponibles de los sensores
    # lista_sensores = interfaz.get_sensores(equipo)

    # Eliminar esto una vez que se conecte con la interfaz
    lista_sensores = [1, 6, 8]
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
                    break

    for i in range(len(datos_menu)):
        print(str(lista_sensores[i]) + " - " + datos_menu[i])

    opcion = input("\nSeleccione un numero >> ")

    try:
        opcion = int(opcion)
        lista_sensores.index(opcion)

        # Pedimos los datos del sensor a la interfaz
        # lista_datos = interfaz.get_datos(equipo, opcion)

        # Mandamos a dividir e imprimir los datos
        # eje_x, eje_y = graph_builder.procesar_datos(lista_datos)
        # graph_builder.imprimir_grafico(eje_x, eje_x)

    except ValueError:
        sub_menu_sensores(equipo, datos_sensores)

    return


menu()
