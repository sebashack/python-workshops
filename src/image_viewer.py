import io
import PySimpleGUI as sg
from PIL import Image
from collections import defaultdict
import cv2
from os import walk, path

from face_utils import read_image


file_types = [
    ("JPEG (*.jpg)", "*.jpg"),
    ("PNG (*.png)", "*.png"),
    ("All files (*.*)", "*.*"),
]


def launch_viewer(dirpath, width, height):
    layout = [
        [sg.Image(key="-IMAGE-")],
        [sg.Text("image-label")],
        [sg.InputText(size=(25, 1), key="-LABEL-")],
        [
            sg.Button("set-label", disabled=True),
            sg.Button("reset"),
            sg.Button("next", disabled=True),
        ],
    ]

    window = sg.Window("image-viewer", layout)

    labeled_images = defaultdict(list)
    cur_img = 0
    img_paths = []

    for (_, _, filenames) in walk(dirpath):
        for name in filenames:
            img_paths.append(path.join(dirpath, name))

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if cur_img >= len(img_paths):
            window.FindElement('next').Update(disabled=True)
            window.FindElement('reset').Update(disabled=False)
            cur_img = 0

        if (event == "reset" and cur_img == 0):
            window.FindElement('set-label').Update(disabled=False)
            window.FindElement('next').Update(disabled=False)
            window.FindElement('reset').Update(disabled=True)

            filename = img_paths[cur_img]

            image = Image.open(filename)
            image.thumbnail((width, height))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

        if event == "next":
            cur_img = cur_img + 1

            filename = img_paths[cur_img]

            image = Image.open(filename)
            image.thumbnail((width, height))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

        if event == "set-label":
            label = values["-LABEL-"]
            filename = img_paths[cur_img]
            np_image = read_image(filename)
            grey_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

            labeled_images[label].append(grey_image)

            print((label, filename))

    window.close()
    return labeled_images
