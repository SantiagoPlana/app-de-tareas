import os
import pandas as pd


def lista_archivos(path):
    """Devuelve lista de archivos .txt en el path especificado más un item 'Crear nuevo' """
    archivos = []
    for x in os.listdir(path):
        if x.endswith('.csv'):
            archivos.append(x)
    archivos.append('Crear nuevo')
    return archivos


# función para elegir el archivo que queremos abrir
def elegir_archivo(lista):
    """Devuelve un item de una lista según el input numérico que se ingrese en el prompt. Se debe ingresar el número
    como se muestre en la lista. """
    while True:
        try:
            archivo = int(input('Ingrese el número de la lista de tareas que desea abrir: '))
            archivo = lista[archivo - 1]
            break
        except IndexError:
            print('Valor fuera de índice')
        except ValueError:
            print('Entrada no válida')
    return archivo


def dataframe(lista):
    """Recibe una lista y devuelve un dataframe con cada item formateado y ordenado"""
    dic = {}
    for i in lista:
        i = i.strip('\n').strip('\t')
        i = i.split('|')
        try:
            dic[i[0]] = i[1]
        except IndexError:
            pass

    list_k = [k.removesuffix('\t') for k, v in dic.items()]
    list_v = [v.removeprefix('\t') for k, v in dic.items()]

    sheet = pd.DataFrame(columns=['Entrada', 'Fecha'])

    sheet['Entrada'] = list_k
    sheet['Fecha'] = list_v

    return sheet
