import csv

def a_lista(archivo):
    with open(archivo) as datos:
        lista = []
        leer_csv = csv.reader(datos, delimiter=',')
        for fila in leer_csv:
            sublista = []
            for indice in fila:
                sublista.append(indice)
            lista.append(sublista)
        return lista
