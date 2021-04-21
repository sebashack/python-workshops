from collections import defaultdict
from os import walk, path
from skimage import metrics, img_as_float

import cv2


def read_images(dirpath):
    images = []

    for (_, _, filenames) in walk(dirpath):
        for name in filenames:
            img_path = read_image(path.join(dirpath, name))
            images.append(img_path)

    return images


def read_and_reduce_samples(labels, dirpaths, width, height):
    labeled_images = defaultdict(list)

    for (label, dirpath) in zip(labels, dirpaths):
        images = read_images(dirpath)
        reduced_images = list(map(lambda img: reduce_img(img, width, height), images))
        labeled_images[label] = reduced_images

    return labeled_images


def remove_redundancy_from_samples(labeled_images, tolerance):
    optimized_samples = defaultdict(list)

    for (label, images) in labeled_images.items():
        optimized_samples[label] = remove_redundancy(images, tolerance)

    return optimized_samples


def show_images(img_dict, delay):
    for images in img_dict.values():
        for image in images:
            cv2.imshow("img", image)
            cv2.waitKey(delay)


# Helpers


def read_image(path):
    return cv2.imread(path)


def reduce_img(image, width, height):
    output = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)
    gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

    return gray_output


def remove_redundancy(images, tolerance):
    return remove_redundancy_(images, 0, tolerance)


def remove_redundancy_(images, i, tolerance):
    if len(images) < 2:
        return images

    if i >= len(images) - 1 or not images:
        return images

    head = images[0]
    tail = images[1:]

    if is_similar_to_any(head, tail, tolerance):
        return remove_redundancy_(tail, i + 1, tolerance)
    else:
        tail.append(head)
        return remove_redundancy_(tail, i + 1, tolerance)


def is_similar_to_any(image, images, tolerance):
    for i in images:
        if similarity_score(image, i) >= tolerance:
            return True
    return False


def similarity_score(img1, img2):
    return metrics.structural_similarity(img_as_float(img1), img_as_float(img2))
