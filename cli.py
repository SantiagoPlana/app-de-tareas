import time
import pandas as pd
from modules import functions
import glob

if "__main__" == __name__:
    files = glob.glob('*.csv')


files.append('Crear Nuevo')
# print lista de archivos
for i, a in enumerate(files):
    a = a.removesuffix('.csv')
    print(f'{i + 1}. {a}')

# seleccionar archivo
archivo = functions.elegir_archivo(files)

# Abrimos el archivo para leer y guardamos la lista. Si se seleccionó "crear nuevo" se crea uno nuevo
# y señalamos a una lista vacía.
if archivo is files[-1]:
    archivo = input('Ingrese un nombre para la nueva lista: ') + '.csv'
    listaTareas = pd.DataFrame(columns=['Entrada', 'Fecha'])
else:
    listaTareas = pd.read_csv(archivo)
    if 'Unnamed: 0' in listaTareas.columns:
        listaTareas.drop('Unnamed: 0', axis=1, inplace=True)

listaTareas.index += 1

print(listaTareas)
count = 0

# loop del programa
while __name__ == '__main__':

    fecha = time.strftime('%d %B, %Y, %H:%M')
    # user prompt para seleccionar función
    u_prompt = input('Escriba AGREGAR, VER, EDITAR, COMPLETAR, o SALIR: ')
    # formateo del input
    u_prompt = u_prompt.lower().strip()

    # Matchear input
    match u_prompt:
        # agregar tarea
        case 'agregar':
            while True:

                tarea = input("Ingrese una tarea: " + '\n'
                                                      "(Para volver ingrese 0)")
                if tarea.strip('\n') == '0':
                    if count > 1:
                        print(f'Se agregaron {count} tareas nuevas')
                        count = 0
                    elif count == 1:
                        print('Se agregó 1 tarea nueva')
                        count = 0
                    else:
                        break
                    break

                listaTareas.loc[len(listaTareas) + 1] = [tarea, fecha]
                print(listaTareas)
                listaTareas.to_csv(archivo, index=False)
                print(f'Se agregó "{tarea}"')
                count += 1

        # ver la lista
        case 'ver':
            if listaTareas.empty:
                print('La lista está vacía')
            else:
                for i in listaTareas.index:
                    entrada = listaTareas.loc[i]['Entrada']
                    fecha = listaTareas.loc[i]['Fecha']
                    print(str(i) + '. ' + entrada + '\t' + fecha)

        # editar algún item
        case 'editar':
            # functions.show(tareas)
            print(listaTareas)
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
                if edit > len(listaTareas) or 0 > edit:
                    print('Número no válido')
                # si el input es 0
                elif edit == 0:
                    break
                # input válido
                else:
                    n_tarea = input('Edite tranquilo: ')
                    listaTareas.loc[edit]['Entrada'] = n_tarea
                    listaTareas.loc[edit]['Fecha'] = fecha
                    print('Se editó la tarea exitosamente')
            # save

            listaTareas.to_csv(archivo, index=False)

        # Completar una tarea
        case 'completar':
            print(listaTareas)
            while True:
                try:
                    tarea_comp = int(input('Ingrese el número de la tarea completa: \n'
                                           '(Ingrese 0 para volver al menú)'))
                except ValueError:
                    print('Debe ingresar un número')
                    continue
                if tarea_comp > len(listaTareas) or 0 > tarea_comp:
                    print('Número fuera del índice')
                elif tarea_comp == 0:
                    if count > 1:
                        print(f'Completaste {count} tareas nuevas')
                        count = 0
                    elif count == 1:
                        print('Completaste 1 tarea nueva')
                        count = 0
                    else:
                        break
                    break
                else:

                    tarea = listaTareas.loc[tarea_comp]['Entrada']
                    print(f'¡Felicitaciones! ¡Completaste "{tarea}"!')
                    listaTareas.drop(index=tarea_comp, axis=0, inplace=True)
                    # tareas.pop(tarea_comp)
                    count += 1
            # save
            listaTareas.reset_index(inplace=True, drop=True)
            listaTareas.index += 1
            listaTareas.to_csv(archivo, index=False)

        # escape
        case 'salir':
            print('¡Adiós!')
            break
        # opción no válida

        case _:
            print('Ingrese una opción válida')
