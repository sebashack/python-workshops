from os import walk, path, mkdir, rmdir, remove, getcwd, environ

environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path
import argparse
import sys
from datetime import datetime


from face_utils import (
    show_images,
    generate_rois,
    merge_samples,
    read_images,
    read_image,
    read_sample_from_json,
    remove_redundancy_from_samples,
    show_images_dict,
    write_images,
    write_sample_as_json,
)
from image_viewer import launch_viewer
from neural_network_utils import (
    classify_image,
    classify_images,
    evaluate_model,
    label_dict_to_matrix,
    partition_sample,
    show_classified_images_5x5,
    show_images_5x5,
    train_model,
    retrain_model,
    save_model_for_training,
    save_model_weights,
    load_model,
    all_text_labels,
)


def main(argv):
    parser = argparse.ArgumentParser(description="Celebrity face classifier")
    parser.add_argument(
        "-m",
        "--mode",
        required=True,
        metavar="MODE",
        choices=["train", "classify", "evaluate"],
        type=str,
        help="program mode",
    )

    parser.add_argument(
        "-i",
        "--input-image",
        required=False,
        metavar="FILE",
        type=Path,
        help="input image to be classified",
    )

    parser.add_argument(
        "-l",
        "--model",
        required=False,
        metavar="DIR",
        type=Path,
        help="path to pretrained model",
    )

    parser.add_argument(
        "-e",
        "--epochs",
        required=False,
        metavar="INT",
        default=10,
        type=int,
        help="number of epochs to train model",
    )

    parser.add_argument(
        "-d",
        "--data-set",
        required=False,
        metavar="FILE",
        type=Path,
        help="path to json file with data-set",
    )

    args = parser.parse_args()

    if args.mode == "classify" and args.input_image is None:
        print("'classify' mode requires '--input-image'", file=sys.stderr)
        exit(1)

    if args.mode == "train" and args.data_set is None:
        print("'train' mode requires '--data-set'", file=sys.stderr)
        exit(1)

    if args.mode == "evaluate" and (args.data_set is None or args.model is None):
        print("'evaluate' mode requires '--model' and '--data-set'", file=sys.stderr)
        exit(1)

    if args.mode == "classify":
        image = read_image(str(args.input_image))
        width = 300
        height = 300

        rois = generate_rois([image], width, height)

        if len(rois) > 0:
            loaded_model = load_model(args.model)
            predictions = classify_images(loaded_model, all_text_labels, rois)

            show_classified_images_5x5(rois[:25], predictions[:25])
        else:
            print("no rois detected")

        exit(0)

    if args.mode == "evaluate":
        print("evaluating model ...")
        sample_path = args.data_set
        sample = read_sample_from_json(sample_path)
        (sample_imgs, numeric_labels, text_labels) = label_dict_to_matrix(sample)
        data_set = partition_sample(sample_imgs, numeric_labels, percentage=10)
        trained_model = load_model(args.model)

        evaluation = evaluate_model(
            trained_model, data_set["test"][0], data_set["test"][1], batch_size=4
        )

        print(f"loss: {evaluation[0]}, accuracy: {evaluation[1]}")
        exit(0)

    if args.mode == "train":
        sample_path = args.data_set
        sample = read_sample_from_json(sample_path)
        (sample_imgs, numeric_labels, text_labels) = label_dict_to_matrix(sample)
        data_set = partition_sample(sample_imgs, numeric_labels, percentage=10)

        models_dir = path.join(getcwd(), "trained-models")

        try:
            mkdir(models_dir)
        except OSError:
            print("'trained-models' DIR already exists")

        num_output_layers = len(text_labels)
        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%m-%d-%H:%M:%S")
        model_name = str(timestamp) + "--model"
        epochs = args.epochs
        trained_model = None

        if args.model is None:
            print(f"trainining model from scratch for {epochs} epoch(s)...")
            trained_model = train_model(
                data_set["training"][0],
                data_set["training"][1],
                num_output_layers,
                batch_size=32,
                epochs=epochs,
            )
        else:
            print(f"trainining model from previous one for {epochs} epoch(s)...")
            trained_model = load_model(args.model)
            trained_model = retrain_model(
                trained_model,
                data_set["training"][0],
                data_set["training"][1],
                num_output_layers,
                batch_size=32,
                epochs=epochs,
            )

        save_model_for_training(trained_model, path.join(models_dir, model_name))

        evaluation = evaluate_model(
            trained_model, data_set["test"][0], data_set["test"][1], batch_size=4
        )

        print(f"loss: {evaluation[0]}, accuracy: {evaluation[1]}")
        exit(0)


def rmdir_r(rootpath):
    for (parent, subdirs, filenames) in walk(rootpath):
        for fname in filenames:
            remove(path.join(parent, fname))
        for dirpath in subdirs:
            rmdir(path.join(parent, dirpath))
        rmdir(parent)

    rmdir(rootpath)


if __name__ == "__main__":
    main(sys.argv[1:])
