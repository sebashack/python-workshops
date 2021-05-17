import io
import PySimpleGUI as sg
from PIL import Image
from collections import defaultdict
from os import walk, path

from face_utils import read_image, to_gray_image


file_types = [
    ("JPEG (*.jpg)", "*.jpg"),
    ("PNG (*.png)", "*.png"),
    ("All files (*.*)", "*.*"),
]


def launch_viewer(dirpath, width, height, labels):
    layout = [
        [sg.Image(key="-IMAGE-")],
        [sg.InputOptionMenu(labels, key="-LABEL-", default_value=labels[0])],
        [
            sg.Button("start"),
            sg.Button("set-label", disabled=True),
            sg.Button("next", disabled=True),
            sg.Button("finish"),
        ],
    ]

    window = sg.Window("image-viewer", layout, return_keyboard_events=True)

    stored_images = defaultdict(lambda: defaultdict(str))
    cur_img = 0
    img_paths = {}
    prev_label = ""
    is_start = True

    for (_, _, filenames) in walk(dirpath):
        for name in filenames:
            img_paths[cur_img] = {0: path.join(dirpath, name), 1: False}
            cur_img = cur_img + 1

    cur_img = 0

    while True:

        event, values = window.read()
        if event == "finish" or event == "Exit" or event == sg.WIN_CLOSED:
            break

        if len(values["-LABEL-"]) < 1:
            window.FindElement("set-label").Update(disabled=True)

        if event == "start" and is_start and cur_img == 0:
            is_start = False
            window.FindElement("set-label").Update(disabled=False)
            window.FindElement("next").Update(disabled=False)
            window.FindElement("start").Update(disabled=True)

            filename = img_paths[cur_img][0]

            image = Image.open(filename)
            image.thumbnail((width, height))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())

        if event == "next":
            cur_img = cur_img + 1

            if cur_img == len(img_paths):
                cur_img = 0

            filename = img_paths[cur_img][0]
            image = Image.open(filename)
            image.thumbnail((width, height))
            bio = io.BytesIO()

            image.save(bio, format="PNG")

            window["-IMAGE-"].update(data=bio.getvalue())

        if event == "set-label":
            is_labeled = img_paths[cur_img][1]
            label = values["-LABEL-"]
            filename = img_paths[cur_img][0]

            if is_labeled:
                remove_file(stored_images, prev_label, filename)

            np_image = read_image(filename)
            gray_image = to_gray_image(np_image)

            stored_images[label][filename] = gray_image
            img_paths[cur_img][1] = True

            prev_label = label

            print((label, filename))

    window.close()

    labeled_images = defaultdict(list)
    for (label, images) in stored_images.items():
        labeled_images[label] = list(images.values())

    return labeled_images


def remove_file(d, label, filename):
    if label in d and filename in d[label]:
        files = d[label]
        del files[filename]
