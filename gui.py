# from modules import functions
import os
import PySimpleGUI as sg
import pandas as pd
import time

script_path = os.path.dirname(os.path.abspath(__file__))
print(script_path * 3)
sg.theme('DarkGrey3')
label = sg.Text('Escriba una tarea: ')

inputBox = sg.InputText(tooltip='', key='Tarea')

selectButton = sg.FilesBrowse('Seleccionar Lista', key='Files', target='Files',
                              file_types=(("CSV files", "*.csv"),), enable_events=True)

# Botones
addButton = sg.Button('Añadir')
editButton = sg.Button('Editar')
completeButton = sg.Button('Completar')
exitButton = sg.Button('Salir')
saveAs = sg.FileSaveAs('Save as', key='Save', file_types=(('CSV', '.csv'), ),
                       target='Save', enable_events=True)

# Placeholder para mensaje
mensaje = sg.Text('', key='Mensaje', font=10)

#
listaT = []
listBox = sg.Listbox(values=listaT, key='Tareas',
                     enable_events=True, size=(60, 10),
                     select_mode='LISTBOX_SELECT_MODE_SINGLE',
                     horizontal_scroll=True)

# layout del programa
layout = [[selectButton, saveAs], [label], [inputBox, addButton],
          [listBox, editButton, completeButton], [mensaje], [exitButton]]

# window object
window = sg.Window('App de Tareas',
                   layout=layout,
                   font=('Calibri', 14),
                   size=(820, 500))

# loop del programa
count = 0
listaTareas = None
nombre = ''
path = ''
while True:
    fecha = time.strftime('%d %B, %Y, %H:%M')
    event, values = window.read()
    print(event, values)
    if values['Files']:
        path = values['Files']
        nombre = values['Files'].split('/')[-1]
        listaTareas = pd.read_csv(path)
        # path = path.split('/')[-1]
        listaTareas.index += 1
        # Cuando se abre un archivo por primera vez queremos que se muestre el contenido en la listbox
        if count == 0:
            window['Tareas'].update(values=listaTareas['Entrada'])
            count += 1
    # Creamos un archivo nuevo si ningún archivo se ha seleccionado y está en el primer loop
    if count == 0 and not values['Files']:
        path = script_path + '/nueva lista.csv'
        print(path)

    # El save as/guardar como
    if values['Save']:
        path = values['Save']
        nombre = values['Save'].split('/')[-1]
        # save and update
        listaTareas.to_csv(path, index=False)
        window['Mensaje'].update(value=f'Se guardó el archivo {nombre.removesuffix(".csv")}')
    # matchear los eventos
    match event:
        case 'Añadir':
            nuevaTarea = values['Tarea']
            try:
                listaTareas.loc[len(listaTareas) + 1] = [nuevaTarea, fecha]
                listaTareas.to_csv(path, index=False)

                # save and update
                window['Mensaje'].update(value=f'Se guardó el archivo {nombre.removesuffix(".csv")}')
                window['Tareas'].update(values=listaTareas['Entrada'])
                window['Tarea'].update(value='')
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
                # window['Mensaje'].update(value=f'Se guardó el archivo "nueva lista"')
                window['Tareas'].update(values=listaTareas['Entrada'])
                window['Tarea'].update(value='')

            print(listaTareas)
        case 'Editar':
            try:
                tarea_aEditar = values['Tareas'][0]
                nuevaTarea = values['Tarea']
                index = listaTareas.loc[listaTareas['Entrada'] == tarea_aEditar].index[0]
                listaTareas.loc[index, ['Entrada']] = nuevaTarea
                listaTareas.to_csv(path, index=False)
                # save and update
                window['Mensaje'].update(value=f'Se guardó el archivo {nombre.removesuffix(".csv")}')
                window['Tareas'].update(values=listaTareas['Entrada'])
                window['Tarea'].update(value='')
            except IndexError:
                sg.popup('Ningún elemento seleccionado')

        case 'Completar':
            try:
                tareaCompleta = values['Tareas'][0]
                index = listaTareas.loc[listaTareas['Entrada'] == tareaCompleta].index[0]
                listaTareas.drop(index, axis=0, inplace=True)
                listaTareas.to_csv(path, index=False)

                # limpia la input box
                window['Tarea'].update(value='')
                # save and update
                window['Mensaje'].update(value=f'Se guardó el archivo {nombre.removesuffix(".csv")}')
                window['Tareas'].update(values=listaTareas['Entrada'])
            except IndexError:
                sg.popup('Ningún elemento seleccionado')

        # Update del input box cuando se selecciona elemento de la lista
        case 'Tareas':
            window['Tarea'].update(value=values['Tareas'][0])
        # Exit
        case sg.WIN_CLOSED:
            break
        case 'Salir':
            break

window.close()
