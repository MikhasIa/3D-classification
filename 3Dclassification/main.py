import os
import vedo
import atexit
from CNNmodel import classify, model, image_transform
import PySimpleGUI as sg
from PIL import Image

mesh = None
posit = None

def select_file():
    global mesh
    global posit
    global window
    file_path = sg.popup_get_file('')
    if file_path is not None:
        mesh = vedo.load(file_path)
        if mesh is not None:
            plotters=vedo.Plotter()
            plotters.add(mesh)
            window.hide()
            plotters.show()
            window.un_hide()
            posit=plotters.camera.GetPosition()
        else:
            label2.update(value='No file selected')
    else:
        label2.update(value="You didn't choose a model")

def take_a_screenshot():
    global mesh
    global posit
    plotter = vedo.Plotter(offscreen=True)
    plotter.add(mesh)
    camera = plotter.camera
    camera.SetPosition(posit)
    print(plotter.camera.GetPosition())
    if mesh is not None:
        plotter.show().screenshot('myphotso.png')
        print(label2.update(value='Screenshot success.'))
        img = Image.open('myphotso.png')
        img = img.resize((400, 400), Image.LANCZOS)
        img.save('myphotso.png')
        window['-IMAGE-'].update(filename='myphotso.png')
    else:
        label2.update(value="No file selected.")

def Class():
    global mesh
    label2.update(value="")
    try:
        if mesh is not None:
            label2.update(value="File loaded")

        answer = classify(model, image_transform, 'myphotso.png')
        if answer is not None:
            label2.update(value='This is a ' + str(answer))
        else:
            label2.update(value='Error')
    except:
        label2.update(value='Error uploading file or image')

def delete_photo():
    file_path = 'myphotso.png'
    if os.path.exists(file_path):
        os.remove(file_path)

layout = [
    [sg.Button('Select File', button_color=('black', 'gray'), size=(15, 1),tooltip='This button allows you to select a file to check on the classifier')],
    [sg.Image('', key='-IMAGE-', size=(400, 400))]
]
button_2 = sg.Button('Take a screenshot', button_color=('black', 'gray'), size=(15, 1),tooltip='This button takes a screenshot of the 3D model')
layout.append([button_2])

button_3 = sg.Button('Classify', button_color=('black', 'gray'), size=(15, 1), tooltip='This button allows you to classify your object by photo')
layout.append([button_3])

label2 = sg.Text('', size=(40, 1))
layout.append([label2])

window = sg.Window('CLASSIFY IMAGE', layout,finalize=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Select File':
        select_file()
    if event == 'Take a screenshot':
        take_a_screenshot()
    if event == 'Classify':
        Class()

window.close()
atexit.register(delete_photo)