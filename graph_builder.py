# sudo apt install python3-pip
# python3 -m pip install matplotlib
import matplotlib.pyplot as plt
import datetime


def procesar_datos_minuto(lista_datos, tipo_dato):
    fechas_procesadas = []
    datos_procesados = []

    fechas_procesadas.append(lista_datos[0][0])
    datos_procesados.append(0)
        
    while len(lista_datos) != 0: 

        contador = 0
    
        hora_inicial = sumar_horas([lista_datos[0][0][11:], '00:01:00'], False)
        fecha_inicial = lista_datos[0][0][:10]
        
        if hora_inicial > '23:59:59':
            hora_inicial = sumar_horas([lista_datos[0][0][11:], '00:01:00'], True)
            fecha_inicial = sumar_fecha(lista_datos[0][0][:10], 1)

        fecha = fecha_inicial + ' ' + hora_inicial

        fechas_procesadas.append(fecha)
        datos_procesados.append(0)

        for x in range(len(lista_datos)):
            if lista_datos[x][0] < fecha:
                datos_procesados[-1] = datos_procesados[-1] + lista_datos[x][1]
                contador += 1
            else:
                break

        if tipo_dato != "Booleano":
            datos_procesados[-1] = datos_procesados[-1] / contador

        for x in range(contador):
            lista_datos.pop(0)

    for x in range(len(fechas_procesadas)):
        fechas_procesadas[x] = fechas_procesadas[x].replace(' ', '\n')

    return fechas_procesadas, datos_procesados


def procesar_datos_hora(lista_datos, tipo_dato):
    fechas_procesadas = []
    datos_procesados = []

    fechas_procesadas.append(lista_datos[0][0])
    datos_procesados.append(0)
        
    while len(lista_datos) != 0: 

        contador = 0
    
        hora_inicial = sumar_horas([lista_datos[0][0][11:], '01:00:00'], False)
        fecha_inicial = lista_datos[0][0][:10]
        
        if hora_inicial > '23:59:59':
            hora_inicial = sumar_horas([lista_datos[0][0][11:], '01:00:00'], True)
            fecha_inicial = sumar_fecha(lista_datos[0][0][:10], 1)

        fecha = fecha_inicial + ' ' + hora_inicial

        fechas_procesadas.append(fecha)
        datos_procesados.append(0)

        for x in range(len(lista_datos)):
            if lista_datos[x][0] < fecha:
                datos_procesados[-1] = datos_procesados[-1] + lista_datos[x][1]
                contador += 1
            else:
                break

        if tipo_dato != "Booleano":
            datos_procesados[-1] = datos_procesados[-1] / contador

        for x in range(contador):
            lista_datos.pop(0)

    for x in range(len(fechas_procesadas)):
        fechas_procesadas[x] = fechas_procesadas[x].replace(' ', '\n')

    return fechas_procesadas, datos_procesados


def procesar_datos_dia(lista_datos, tipo_dato):
    fechas_procesadas = []
    datos_procesados = []

    fechas_procesadas.append(lista_datos[0][0])
    datos_procesados.append(0)
        
    while len(lista_datos) != 0: 

        contador = 0
    
        hora_inicial = lista_datos[0][0][11:]
        fecha_inicial = sumar_fecha(lista_datos[0][0][:10], 1)
        
        fecha = fecha_inicial + ' ' + hora_inicial

        fechas_procesadas.append(fecha)
        datos_procesados.append(0)

        for x in range(len(lista_datos)):
            if lista_datos[x][0] < fecha:
                datos_procesados[-1] = datos_procesados[-1] + lista_datos[x][1]
                contador += 1
            else:
                break

        if tipo_dato != "Booleano":
            datos_procesados[-1] = datos_procesados[-1] / contador

        for x in range(contador):
            lista_datos.pop(0)

    for x in range(len(fechas_procesadas)):
        fechas_procesadas[x] = fechas_procesadas[x].replace(' ', '\n')

    return fechas_procesadas, datos_procesados


def sumar_fecha(fecha, dias):
    total = datetime.datetime.strptime(fecha, "%Y-%m-%d")
    total = total + datetime.timedelta(days=dias)
    return (str(total)[:10])


def sumar_horas(lista_horas, modular):
    total = 0
    for hora in lista_horas:
        h, m, s = map(int, hora.split(":"))
        total += 3600*h + 60*m + s
    if modular == False:
        return("%02d:%02d:%02d" % (total / 3600, total / 60 % 60, total % 60))
    else:
        return("%02d:%02d:%02d" % (total / 3600 % 24, total / 60 % 60, total % 60))

def imprimir_grafico_barras(eje_x, eje_y, label_x, label_y, titulo):
    plt.bar(eje_x, eje_y)
    plt.title(titulo)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()
    return


def imprimir_grafico_lineas(eje_x, eje_y, label_x, label_y, titulo):
    plt.plot(eje_x, eje_y)
    plt.title(titulo)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.show()
    return