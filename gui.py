from modules import functions
import PySimpleGUI as sg
import pandas as pd
import time

label = sg.Text('Escriba una tarea: ')
inputBox = sg.InputText(tooltip='', key='Tarea')
selectButton = sg.FilesBrowse('Seleccionar Lista',
                              file_types=(("CSV files", "*.csv"),))
addButton = sg.Button('Añadir')
exitButton = sg.Button('Salir')
window = sg.Window('App de Tareas',
                   layout=[[selectButton], [label], [inputBox, addButton],
                           [exitButton]],
                   font=('Georgia', 13))

while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    path = values['Seleccionar Lista']
    if path is not None and len(path) > 2:
        listaTareas = pd.read_csv(path)
        listaTareas.index += 1
    print(event)
    print(values)
    match event:
        case 'Añadir':
            nuevaTarea = values['Tarea']
            listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
            listaTareas.to_csv(path.split('/')[-1], index=False)
            print(listaTareas)

        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            window.close()
