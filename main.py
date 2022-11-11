import os
import time
from modules import functions

#from contextlib import suppress

#! hacer que el path sea elegible y no hardcodeado
path = r"C:\Users\Santiago\Desktop\Programas\Apps\proj1\venv"
archivos = functions.lista_archivos(path)

# print lista de archivos
for i, a in enumerate(archivos):
    a = a.removesuffix('.txt')
    print(f'{i+1}. {a}')

# seleccionar archivo
archivo = functions.elegir_archivo(archivos)

# abrimos el archivo para leer y guardamos la lista. Si se seleccionó "crear nuevo" se crea uno nuevo
# y señalamos a una lista vacía.
if archivo is archivos[-1]:
    archivo = input('Ingrese un nombre para la nueva lista: ') + '.txt'
    open(archivo, 'w')
    tareas = []
else:
    with open(archivo, 'r') as file:
        tareas = file.readlines()  # readlines devuelve una lista

# loop del programa
while __name__ == '__main__':
    #count = 0
    fecha = time.strftime('%d %B, %Y, %H:%M')
    # user prompt para seleccionar función
    u_prompt = input('Escriba AGREGAR, VER, EDITAR, COMPLETAR, o SALIR: ')
    # formateo del input
    u_prompt = u_prompt.lower().strip()

    # matchear input
    match u_prompt:
        #agregar tarea
        case 'agregar':
            while True:
                tarea = input("Ingrese una tarea: "+ '\n'
                          "(Para volver ingrese 0)") +  '\n'
                if tarea.strip('\n') == '0':
                    break

                tarea = tarea.strip('\n')+ '\t' + '|' + '\t' + fecha +'\n'

                tareas.append(tarea)

                functions.save(archivo, tareas)
                stripped = tarea.strip('\n').split('|')[0]
                print(f'Se agregó "{stripped.strip()}".')


        #ver la lista
        case 'ver':
            if tareas:
                functions.show(tareas)
            if not tareas:
                print('No hay tareas pendientes')

        # editar algún item
        case 'editar':
            functions.show(tareas)
            while True:
                try:
                    edit = int(input('Ingrese el número del elemento a editar: \n'
                                    '(Ingrese 0 para volver al menú)'))
                # inputs no válidos
                except ValueError:
                    print('Debe ingresar un número')
                    continue
                # aquí usamos un if porque un IndexError no saltaría hasta el bloque else
                # y queremos agarrar el error antes de que corra lo demás
                if edit > len(tareas) or 0 > edit:
                    print('Número no válido')
                # si el input es 0
                elif edit == 0:
                    break
                # input válido
                else:
                    edit = edit - 1
                    n_tarea = input('Edite tranquilo: ') + '\n'
                    tareas[edit] = n_tarea
                    print('Se editó la tarea exitosamente')
            # save
            functions.save(archivo, tareas)

        # Completar una tarea
        case 'completar':
            functions.show(tareas)
            while True:
                count =+ 1
                try:
                    tarea_comp = int(input('Ingrese el número de la tarea completa: \n'
                                            '(Ingrese 0 para volver al menú)'))
                except ValueError:
                    print('Debe ingresar un número')
                    continue
                if tarea_comp > len(tareas):
                    print('Número fuera del índice')
                elif tarea_comp == 0:
                    break
                else:
                    tarea_comp = tarea_comp - 1
                    tarea = tareas[tarea_comp].strip('\n')
                    print(f'¡Felicitaciones! ¡Completaste "{tarea}"!')
                    tareas.pop(tarea_comp)
            # save
            functions.save(archivo, tareas)

        # escape
        case 'salir':
            print('¡Adiós!')
            break
        # opción no válida

        case _:
            print('Ingrese una opción válida')