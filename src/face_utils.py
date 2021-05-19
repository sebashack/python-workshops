from collections import defaultdict
from os import walk, path, mkdir
from skimage import metrics, img_as_float
import base64
import cv2
import json
import numpy as np
import random


def remove_redundancy_from_samples(labeled_images, tolerance, limit):
    optimized_samples = defaultdict(list)

    for (label, images) in labeled_images.items():
        optimized_samples[label] = remove_redundancy(images, tolerance, limit)

    return optimized_samples


def generate_rois(images, w, h):
    roiss = list(map(lambda img: detect_faces(img)[1], images))
    rois = [item for roi in roiss for item in roi]

    return list(map(lambda img: reduce_image_resolution(img, w, h), rois))


def write_images(images, dirpath):
    if not path.exists(dirpath):
        mkdir(dirpath)

    for (i, image) in enumerate(images):
        name = "face" + str(i) + ".jpg"
        cv2.imwrite(path.join(dirpath, name), image)


def read_images(dirpath):
    images = []

    for (_, _, filenames) in walk(dirpath):
        for name in filenames:
            img_path = read_image(path.join(dirpath, name))
            images.append(img_path)

    return images


def read_image(path):
    return cv2.imread(path)


def reduce_image_resolution(image, width, height):
    output = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)

    return output


def to_gray_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def detect_faces(image):
    face_cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(face_cascade)
    gray_image = to_gray_image(image)

    rectangles = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30)
    )

    roi_images = []

    for (x, y, w, h) in rectangles:
        ROI = gray_image[y : y + h, x : x + w]
        roi_images.append(ROI)

    return (rectangles, roi_images)


def show_images(images, delay):
    for image in images:
        cv2.imshow("img", image)
        cv2.waitKey(delay)


def show_images_dict(img_dict, delay):
    for images in img_dict.values():
        for image in images:
            cv2.imshow("img", image)
            cv2.waitKey(delay)


def write_sample_as_json(labeled_images, filepath):
    obj = sample_to_json(labeled_images)
    with open(filepath, "w") as f:
        json.dump(obj, f)


def sample_to_json(labeled_images):
    obj = defaultdict(list)
    for (label, images) in labeled_images.items():
        obj[label] = list(map(np_image_to_base64, images))

    return obj


def read_sample_from_json(filepath):
    labeled_images = defaultdict(list)
    with open(filepath, "r") as f:
        data = json.load(f)

        for (label, encoded_imgs) in data.items():
            images = list(map(base64_str_to_np_image, encoded_imgs))
            labeled_images[label] = list(map(to_gray_image, images))

        f.close()

    return labeled_images


def merge_samples(labeled_images1, labeled_images2):
    merged_images = labeled_images1

    for (label, images) in labeled_images2.items():
        if label in merged_images:
            prev_images = merged_images[label]
            merged_images[label] = prev_images + images
        else:
            merged_images[label] = images

    return merged_images


def base64_str_to_np_image(s):
    buff = base64.b64decode(s)
    image_as_np = np.frombuffer(buff, dtype=np.uint8)
    return cv2.imdecode(image_as_np, flags=1)


def np_image_to_base64(image):
    retval, buff = cv2.imencode(".png", image)
    img_as_text = base64.b64encode(buff)
    return img_as_text.decode("utf-8")


def remove_redundancy(images, tolerance, limit):
    return remove_redundancy_(images, 0, tolerance, limit)


def remove_redundancy_(images, i, tolerance, limit):
    if len(images) < 2:
        return images

    if i >= len(images) - 1 or not images:
        return images

    head = images[0]
    tail = images[1:]
    # Compare against a random sample for performance purposes.
    sample = tail
    random.shuffle(sample)

    if is_similar_to_any(head, sample[0:limit], tolerance):
        return remove_redundancy_(tail, i + 1, tolerance, limit)
    else:
        tail.append(head)
        return remove_redundancy_(tail, i + 1, tolerance, limit)


def is_similar_to_any(image, images, tolerance):
    for i in images:
        if similarity_score(image, i) >= tolerance:
            return True
    return False


def similarity_score(img1, img2):
    return metrics.structural_similarity(img_as_float(img1), img_as_float(img2))
