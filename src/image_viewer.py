import io
import os
import PySimpleGUI as sg
from PIL import Image
from collections import defaultdict

from face_utils import read_image


file_types = [
    ("JPEG (*.jpg)", "*.jpg"),
    ("PNG (*.png)", "*.png"),
    ("All files (*.*)", "*.*"),
]


def launch_viewer():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Load Image"),
        ],
        [sg.Text("Image Label"), sg.InputText(size=(23, 1), key="-LABEL-")],
    ]

    window = sg.Window("Image Viewer", layout)
    labeled_images = defaultdict(list)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            label = values["-LABEL-"]
            if os.path.exists(filename) and len(label) > 0:
                np_image = read_image(filename)
                labeled_images[label].append(np_image)
                print(label)

                image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

    window.close()
    return labeled_images
