from collections import defaultdict
from skimage import metrics, img_as_float
import base64
import cv2
import numpy as np
import json


def reduce_samples(labeled_images, redux):
    reduced_images = defaultdict(list)

    for (label, images) in labeled_images.items():
        reduced_images[label] = list(map(redux, images))

    return reduced_images


def reduce_image_resolution(image, width, height):
    output = cv2.resize(image, (width, height), interpolation=cv2.INTER_NEAREST)

    return output


def reduce_image_to_roi(image):
    rectangles, roi_images = detect_faces(image)

    if len(rectangles) < 1:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    current_area = 0
    j = 0

    for (i, (_, _, w, h)) in enumerate(rectangles):
        area = w * h

        if area > current_area:
            current_area = area
            j = i

    return roi_images[j]


def remove_redundancy_from_samples(labeled_images, tolerance):
    optimized_samples = defaultdict(list)

    for (label, images) in labeled_images.items():
        optimized_samples[label] = remove_redundancy(images, tolerance)

    return optimized_samples


def detect_faces(image):
    face_cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(face_cascade)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    rectangles = face_classifier.detectMultiScale(
        grey_image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30)
    )

    roi_images = []

    for (x, y, w, h) in rectangles:
        ROI = grey_image[y: y + h, x: x + w]
        roi_images.append(ROI)

    return (rectangles, roi_images)


def show_images(img_dict, delay):
    for images in img_dict.values():
        for image in images:
            cv2.imshow("img", image)
            cv2.waitKey(delay)


def read_image(path):
    return cv2.imread(path)


def write_sample_as_json(labeled_images, filepath):
    obj = sample_to_json(labeled_images)
    with open(filepath, 'w') as f:
        json.dump(obj, f)


def sample_to_json(labeled_images):
    obj = defaultdict(list)
    for (label, images) in labeled_images.items():
        obj[label] = list(map(np_image_to_base64, images))

    return obj


def read_sample_from_json(filepath):
    labeled_images = defaultdict(list)
    with open(filepath, 'r') as f:
        data = json.load(f)

        for (label, encoded_imgs) in data.items():
            labeled_images[label] = list(map(base64_str_to_np_image, encoded_imgs))

        f.close()

    return labeled_images


def base64_str_to_np_image(s):
    buff = base64.b64decode(s)
    image_as_np = np.frombuffer(buff, dtype=np.uint8)
    return cv2.imdecode(image_as_np, flags=1)


def np_image_to_base64(image):
    retval, buff = cv2.imencode('.png', image)
    img_as_text = base64.b64encode(buff)
    return img_as_text.decode('utf-8')


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