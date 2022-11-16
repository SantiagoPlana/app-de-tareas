from modules import functions
import PySimpleGUI as sg
import pandas as pd
import time

sg.theme('DarkTeal2')
label = sg.Text('Escriba una tarea: ')
inputBox = sg.InputText(tooltip='', key='Tarea')

selectButton = sg.FilesBrowse('Seleccionar Lista',
                              file_types=(("CSV files", "*.csv"),))
addButton = sg.Button('Añadir')
editButton = sg.Button('Editar')
exitButton = sg.Button('Salir')

listaT = []
listBox = sg.Listbox(values=listaT, key='Tareas',
                     enable_events=True, size=[45, 10])

window = sg.Window('App de Tareas',
                   layout=[[selectButton], [label],
                           [inputBox, addButton],
                           [listBox, editButton],
                           [exitButton]],
                   font=('Georgia', 13))

while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    window.refresh()
    print(event, values)
    # if values['Seleccionar Lista'] is None:
    path = values['Seleccionar Lista']
    # print(path)
    listaTareas = pd.read_csv(path)
    print(listaTareas)
    listaTareas.index += 1
    window['Tareas'].update(values=listaTareas['Entrada'])
    # print(event)
    # print(values)
    match event:
        case 'Seleccionar Lista':
            path = values['Seleccionar Lista']
            print(path)
            listaTareas = pd.read_csv(path)
            print(listaTareas)
            listaTareas.index += 1
            window['Tareas'].update(values=listaTareas['Entrada'])
        case 'Añadir':
            nuevaTarea = values['Tarea']
            listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
            listaTareas.to_csv(path.split('/')[-1], index=False)
            print(listaTareas)
        case 'Editar':
            pass
        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            window.close()
