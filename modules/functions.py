import os

def lista_archivos(path):
    """Devuelve lista de archivos .txt en el path especificado más un item 'Crear nuevo' """
    archivos = []
    for x in os.listdir(path):
        if x.endswith('.txt'):
            archivos.append(x)
    archivos.append('Crear nuevo')
    return archivos


# función para elegir el archivo que queremos abrir
def elegir_archivo(lista):
    """Devuelve un item de una lista según el input numérico que se ingrese en el prompt. Se debe ingresar el número
    como se muestre en la lista. """
    while True:
        try:
            #global archivos
            archivo = int(input('Ingrese el número de la lista de tareas que desea abrir: '))
            archivo = lista[archivo -1]
            break
        except IndexError:
            print('Valor fuera de índice')
        except ValueError:
            print('Entrada no válida')
    return archivo


# función para el write
def save(arch, lista):
    """Escribe el contenido de una lista en un archivo .txt"""
    with open(arch, 'w') as file:
        file.writelines(lista)


# printear la lista
def show(lista):
    """Muestra el contenido de una lista enumerándola y stripeando las newlines"""
    for i, tarea in enumerate(lista):
        tarea = tarea.strip('\n')
        #tarea = tarea.split('|')[0]
        msj = f"{i + 1}. {tarea}"
        print(msj)

