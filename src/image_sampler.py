from collections import defaultdict
from os import walk, path
import cv2
import numpy as np


def read_image(path):
    return cv2.imread(path)


def read_images(dirpath):
    images = []

    for (_, _, filenames) in walk(dirpath):
        for name in filenames:
            img_path = read_image(path.join(dirpath, name))
            images.append(img_path)

    return images


def reduce_img(image, width, height):
    output = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)
    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    return gray_output


def read_and_reduce_samples(labels, dirpaths, width, height):
    labeled_images = defaultdict(list)

    for (label, dirpath) in zip(labels, dirpaths):
        images = read_images(dirpath)
        reduced_images = list(map(lambda img: reduce_img(img, width, height), images))
        labeled_images[label] = reduced_images

    return labeled_images


def show_images(img_dict, delay):
    for images in img_dict.values():
        for image in images:
            cv2.imshow("img", image)
            cv2.waitKey(delay)
