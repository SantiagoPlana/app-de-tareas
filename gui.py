from modules import functions
import PySimpleGUI as sg

label = sg.Text('Escriba una tarea: ')
inputBox = sg.InputText(tooltip='Ingrese una tarea')
addButton = sg.Button('Añadir')
window = sg.Window('App de Tareas', layout=[[label], [inputBox], [addButton]])

window.read()
window.close()
