# from modules import functions
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
editButton = sg.Button('Editar')
completeButton = sg.Button('Completar')
exitButton = sg.Button('Salir')

listaT = []
listBox = sg.Listbox(values=listaT, key='Tareas',
                     enable_events=True, size=(45, 10),
                     select_mode='LISTBOX_SELECT_MODE_SINGLE')

window = sg.Window('App de Tareas',
                   layout=[[selectButton], [label],
                           [inputBox, addButton],
                           [listBox, editButton, completeButton],
                           [exitButton], [mostrarButton]],
                   font=('Georgia', 13))

count = 0
while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    # window.refresh()
    print(event, values)
    path = values['Files']
    listaTareas = pd.read_csv(path)
    listaTareas.index += 1
    print(listaTareas)
    if count == 0:
        window['Tareas'].update(values=listaTareas['Entrada'])
        count += 1
    match event:
        case 'Añadir':
            nuevaTarea = values['Tarea']
            listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
            listaTareas.to_csv(path.split('/')[-1], index=False)
            window['Tareas'].update(values=listaTareas['Entrada'])
            print(listaTareas)
        case 'Editar':
            tarea_aEditar = values['Tareas'][0]
            nuevaTarea = values['Tarea']
            index = listaTareas.loc[listaTareas['Entrada'] == tarea_aEditar].index[0]
            listaTareas.loc[index, ['Entrada']] = nuevaTarea
            listaTareas.to_csv(path.split('/')[-1], index=False)
            window['Tareas'].update(values=listaTareas['Entrada'])
        case 'Completar':
            tareaCompleta = values['Tareas'][0]
            index = listaTareas.loc[listaTareas['Entrada'] == tareaCompleta].index[0]
            listaTareas.drop(index, axis=0, inplace=True)
            listaTareas.to_csv(path.split('/')[-1], index=False)
            window['Tareas'].update(values=listaTareas['Entrada'])

        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            break

window.close()
