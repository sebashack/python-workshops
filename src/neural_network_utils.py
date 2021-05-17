import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
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
        plt.imshow(images[i + offset])
        plt.xlabel(text_labels[num_labels[i + offset]])
    plt.show()


def show_classified_images_5x5(images, labels_and_pobs):
    plt.figure(figsize=(10, 10))

    for (i, image) in enumerate(images):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(image)
        (label, prob) = labels_and_pobs[i]
        plt.xlabel(f"{label}: {prob}")

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


def train_model(training_images, training_labels, num_output_layers, width, height, epochs):
    model = models.Sequential()

    # First layer
    model.add(layers.Conv2D(20, (5, 5), activation="relu", padding="same", input_shape=(width, height, 1)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Second layer
    model.add(layers.Conv2D(50, (5, 5), activation="relu", padding="same"))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Third layer
    model.add(layers.Flatten())
    model.add(layers.Dense(500, activation='relu'))

    # Output layer
    model.add(layers.Dense(num_output_layers, activation='softmax'))

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    training_images_ = training_images.reshape(len(training_images), height, width, 1) / 255.0
    model.fit(training_images_, training_labels, epochs=epochs)

    return model


def test_model(model, example_images, example_labels):
    return model.evaluate(example_images, example_labels, verbose=2)


def save_model(filepath, model):
    model.save(filepath)


def load_model(filepath):
    keras.models.load_model(filepath)


def classify_image(model, text_labels, image):
    width = image.shape[0]
    height = image.shape[1]
    input_ = np.array([image]).reshape(1, width, height, 1)

    prediction = model.predict(input_)[0]

    return get_label(text_labels, prediction)


def classify_images(model, text_labels, images):
    size = images.shape[0]
    width = images.shape[1]
    height = images.shape[2]
    input_ = np.array(images).reshape(size, width, height, 1)

    predictions = model.predict(input_)
    print(f"Original preds: {predictions}")

    return list(map(lambda p: get_label(text_labels, p), predictions))


def get_label(text_labels, prediction):
    i = np.argmax(prediction)
    predicted_label = text_labels[i]
    probability = prediction[i]

    return (predicted_label, probability)
