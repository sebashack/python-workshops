import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import math
from random import randrange

from face_utils import reduce_image_resolution, to_gray_image


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
        p = "{:.2f}".format(prob)
        plt.xlabel(f"{label}: {p}")

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


def train_model(training_images, training_labels, num_output_layers, batch_size, epochs):
    size = training_images.shape[0]
    width = training_images.shape[1]
    height = training_images.shape[2]

    model = basic_cnn_model((width, height, 1), num_output_layers)

    model.compile(
        optimizer="adam",
        loss=tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )

    training_images_ = training_images.reshape(size, width, height, 1) / 255.0

    gen = make_data_generator(training_images_, training_labels, batch_size)

    model.fit_generator(gen['iterator'],
                        steps_per_epoch=gen['steps_per_epoch'],
                        epochs=epochs)

    return model


def retrain_model(model, training_images, training_labels, num_output_layers, batch_size, epochs):
    size = training_images.shape[0]
    width = training_images.shape[1]
    height = training_images.shape[2]

    training_images_ = training_images.reshape(size, width, height, 1) / 255.0

    gen = make_data_generator(training_images_, training_labels, batch_size)

    model.fit_generator(gen['iterator'],
                        steps_per_epoch=gen['steps_per_epoch'],
                        epochs=epochs)

    return model


def partition_sample(training_images, training_labels, percentage):
    assert percentage >= 1 and percentage <= 100
    size = len(training_images)
    test_size = round(size * (percentage / 100))
    training_size = size - test_size

    training_set = (training_images[:training_size], training_labels[:training_size])
    test_set = (training_images[training_size:], training_labels[training_size:])

    return {"training": training_set, "test": test_set}


def evaluate_model(model, example_images, example_labels, batch_size):
    size = example_images.shape[0]
    width = example_images.shape[1]
    height = example_images.shape[2]

    example_images_ = example_images.reshape(size, width, height, 1) / 255.0
    gen = make_data_generator(example_images_, example_labels, batch_size)

    (loss, accuracy) = model.evaluate(gen['iterator'], verbose=2)

    return (loss, accuracy)


def save_model_for_training(model, filepath):
    model.save(filepath, save_format='tf')


def save_model_weights(model, filepath):
    model.save(filepath, save_format='h5')


def load_model(filepath):
    return keras.models.load_model(filepath)


def preprocess_image(image, w, h):
    gray_image = to_gray_image(image)
    return reduce_image_resolution(gray_image, w, h)


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

    return list(map(lambda p: get_label(text_labels, p), predictions))


def get_label(text_labels, prediction):
    i = np.argmax(prediction)
    predicted_label = text_labels[i]
    probability = prediction[i]

    return (predicted_label, probability)


def make_data_generator(data_set, labels, batch_size):
    size = data_set.shape[0]
    width = data_set.shape[1]
    height = data_set.shape[2]

    data_set_ = data_set.reshape(size, width, height, 1)

    datagen = ImageDataGenerator(horizontal_flip=True,
                                 rotation_range=50,
                                 brightness_range=[0.2, 1.0])

    it = datagen.flow(data_set_, labels, batch_size=batch_size)
    steps_per_epoch = math.ceil(len(data_set) / batch_size)

    return {'iterator': it, 'steps_per_epoch': steps_per_epoch}


def basic_cnn_model(shape, num_output_layers):
    model = models.Sequential()

    # First layer
    model.add(
        layers.Conv2D(
            40,
            (5, 5),
            activation="relu",
            padding="same",
            input_shape=shape,
        )
    )

    # Second layer
    model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Third layer
    model.add(layers.Conv2D(100, (5, 5), activation="relu", padding="same"))

    # Fourth layer
    model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    # Fifth layer
    model.add(layers.Flatten())
    model.add(layers.Dense(500, activation="relu"))

    # Output layer
    model.add(layers.Dense(num_output_layers, activation="softmax"))

    return model


def resnet50_cnn_model(shape, num_output_layers):
    model = tf.keras.applications.ResNet50(
            include_top=True,
            weights=None,
            input_tensor=None,
            input_shape=shape,
            pooling=None,
            classes=num_output_layers
    )

    return model
