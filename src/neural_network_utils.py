import matplotlib.pyplot as plt
import numpy as np


def show_images_5x5(images, text_labels, numeric_labels, n, offset):
    plt.figure(figsize=(10, 10))
    for i in range(n):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i + offset], cmap=plt.cm.binary)
        plt.xlabel(text_labels[numeric_labels[i + offset]])
    plt.show()


def label_dict_to_matrix(data_set):
    mx = []
    labels = []

    for label, images in data_set.items():
        for image in images:
            mx.append(image)
        labels.append(label)

    numeric_labels = list(range(len(labels)))

    return (np.array(mx), np.array(numeric_labels), labels)
