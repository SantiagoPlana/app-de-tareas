from modules import functions
import PySimpleGUI as sg
import pandas as pd
import time

sg.theme('DarkTeal2')
label = sg.Text('Escriba una tarea: ')
inputBox = sg.InputText(tooltip='', key='Tarea')

mostrarButton = sg.Button('')
selectButton = sg.FilesBrowse('Seleccionar Lista', key='Files', target='Files',
                              file_types=(("CSV files", "*.csv"),), enable_events=True)

addButton = sg.Button('Añadir')
editButton = sg.Button('Editar', target='Tareas')
exitButton = sg.Button('Salir')

listaT = []
listBox = sg.Listbox(values=listaT, key='Tareas',
                     enable_events=True, size=(45, 10))

window = sg.Window('App de Tareas',
                   layout=[[selectButton], [label],
                           [inputBox, addButton],
                           [listBox, editButton],
                           [exitButton], [mostrarButton]],
                   font=('Georgia', 13))

while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    # window.refresh()
    print(event, values)

    path = values['Files']
    # print(path)
    listaTareas = pd.read_csv(path)
    print(listaTareas)
    listaTareas.index += 1
    window['Tareas'].update(values=listaTareas['Entrada'])
    # print(event)
    # print(values)
    match event:
        case 'Añadir':
            print(event, values)
            nuevaTarea = values['Tarea']
            listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
            listaTareas.to_csv(path.split('/')[-1], index=False)
            window['Tareas'].update(values=listaTareas['Entrada'])
            print(listaTareas)
        case 'Editar':
            pass
        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            break

window.close()
