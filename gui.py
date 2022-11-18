# from modules import functions
import os
import PySimpleGUI as sg
import pandas as pd
import time

script_path = os.path.dirname(__file__)
print(script_path)
sg.theme('DarkGrey14')
label = sg.Text('Escriba una tarea: ')

inputBox = sg.InputText(tooltip='', key='Tarea')

selectButton = sg.FilesBrowse('Seleccionar Lista', key='Files', target='Files',
                              file_types=(("CSV files", "*.csv"),), enable_events=True)

addButton = sg.Button('Añadir')
editButton = sg.Button('Editar')
completeButton = sg.Button('Completar')
exitButton = sg.Button('Salir')
saveAs = sg.FileSaveAs('Save as', key='Save', file_types=(('CSV', '.csv'), ),
                       target='Save', enable_events=True)

mensaje = sg.Text('', key='Mensaje', font=10)

listaT = []
listBox = sg.Listbox(values=listaT, key='Tareas',
                     enable_events=True, size=(60, 10),
                     select_mode='LISTBOX_SELECT_MODE_SINGLE',
                     horizontal_scroll=True)

layout = [[selectButton, saveAs], [label], [inputBox, addButton],
          [listBox, editButton, completeButton], [mensaje], [exitButton]]

window = sg.Window('App de Tareas',
                   layout=layout,
                   font=('Calibri', 13),
                   size=(750, 500))

count = 0
listaTareas = None
while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    print(event, values)
    if values['Files']:
        path = values['Files']
        listaTareas = pd.read_csv(path)
        path = path.split('/')[-1]
        listaTareas.index += 1
        print(listaTareas)
        if count == 0:
            window['Tareas'].update(values=listaTareas['Entrada'])
            count += 1
        if count == 0 and not values['Files']:
            path = script_path + '/nueva lista.csv'
            print(path)
            count += 1
    if values['Save']:
        path = values['Save'].split('/')[-1]

        # save and update
        listaTareas.to_csv(path, index=False)
        window['Mensaje'].update(value=f'Se guardó el archivo {path.removesuffix(".csv")}')
    match event:
        case 'Añadir':
            nuevaTarea = values['Tarea']
            try:
                listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
                listaTareas.to_csv(path.split('/')[-1], index=False)

                # save and update
                window['Mensaje'].update(value=f'Se guardó el archivo {path.removesuffix(".csv")}')
                window['Tareas'].update(values=listaTareas['Entrada'])
            except (NameError, AttributeError):
                if count == 0:
                    listaTareas = pd.DataFrame(columns=['Entrada', 'Fecha'])
                    listaTareas.index += 1
                    count += 1
                    listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
                    print(listaTareas)
                    window['Mensaje'].update(value='Se creó un nuevo archivo "nueva lista"')
                # save and update
                listaTareas.to_csv(script_path + '/nueva lista.csv', index=False)
                window['Mensaje'].update(value=f'Se guardó el archivo "nueva lista"')
                window['Tareas'].update(values=listaTareas['Entrada'])

            print(listaTareas)
        case 'Editar':
            tarea_aEditar = values['Tareas'][0]
            nuevaTarea = values['Tarea']
            index = listaTareas.loc[listaTareas['Entrada'] == tarea_aEditar].index[0]
            listaTareas.loc[index, ['Entrada']] = nuevaTarea
            listaTareas.to_csv(path.split('/')[-1], index=False)

            # save and update
            window['Mensaje'].update(value=f'Se guardó el archivo {path.removesuffix(".csv")}')
            window['Tareas'].update(values=listaTareas['Entrada'])
        case 'Completar':
            tareaCompleta = values['Tareas'][0]
            index = listaTareas.loc[listaTareas['Entrada'] == tareaCompleta].index[0]
            listaTareas.drop(index, axis=0, inplace=True)
            listaTareas.to_csv(path.split('/')[-1], index=False)

            # save and update
            window['Mensaje'].update(value=f'Se guardó el archivo {path.removesuffix(".csv")}')
            window['Tareas'].update(values=listaTareas['Entrada'])

        # Update del input box cuando se selecciona elemento de la lista
        case 'Tareas':
            window['Tarea'].update(value=values['Tareas'][0])
        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            break

window.close()
