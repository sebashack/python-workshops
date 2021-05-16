from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
from random import randrange


def show_images_5x5(images, text_labels, num_labels, n, offset):
    plt.figure(figsize=(10, 10))
    for i in range(n):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i + offset], cmap=plt.cm.binary)
        plt.xlabel(text_labels[num_labels[i + offset]])
    plt.show()


def label_dict_to_matrix(data_set):
    mx = []
    labels = {}
    num_labels = []

    i = 0
    for label, images in data_set.items():
        for image in images:
            mx.append(image)
            num_labels.append(i)
        labels[i] = label
        i += 1

    shuffle(mx, num_labels)

    return (np.array(mx), np.array(num_labels), labels)


def shuffle(mx, num_labels):
    size = len(mx)

    for _ in range(size):
        i = randrange(size)
        j = randrange(size)

        mx[i], mx[j] = mx[j], mx[i]
        num_labels[i], num_labels[j] = num_labels[j], num_labels[i]


def train_model(training_images, training_labels, width, height, epochs):
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(width, height)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(10, activation='softmax'),
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    model.fit(training_images, training_labels, epochs=epochs)

    return model


def test_model(model, example_images, example_labels):
    return model.evaluate(example_images, example_labels, verbose=2)


def save_model(filepath, model):
    model.save(filepath)


def load_model(filepath):
    keras.models.load_model(filepath)
