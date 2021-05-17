from os import walk, path, mkdir, rmdir, remove
from pathlib import Path
import argparse
import sys

from face_utils import (
    remove_redundancy_from_samples,
    write_images,
    write_sample_as_json,
    read_sample_from_json,
    read_images,
    show_images,
    generate_rois,
)
from image_viewer import launch_viewer
from neural_network_utils import (
    show_images_5x5,
    label_dict_to_matrix,
    train_model,
    classify_image,
    classify_images,
    show_classified_images_5x5,
    partition_sample,
    evaluate_model,
)


def main(argv):
    parser = argparse.ArgumentParser(description="Face trainer")
    parser.add_argument(
        "-i",
        "--input-dir",
        required=True,
        metavar="DIR",
        type=Path,
        help="raw images input dir",
    )
    parser.add_argument(
        "-o",
        "--out-dir",
        required=True,
        metavar="DIR",
        type=Path,
        help="processed rois output dir",
    )
    parser.add_argument(
        "-j",
        "--out-json",
        required=True,
        metavar="FILE",
        type=Path,
        help="json file output",
    )
    parser.add_argument(
        "-wt",
        "--width",
        required=True,
        metavar="INT",
        type=int,
        help="proccessed image width",
    )
    parser.add_argument(
        "-ht",
        "--height",
        required=True,
        metavar="INT",
        type=int,
        help="proccessed image height",
    )
    args = parser.parse_args()

    raw_dirpath = args.input_dir

    if not path.isdir(raw_dirpath):
        print(f"non-existent raw input dir: {raw_dirpath}", file=sys.stderr)
        raise Exception("non-existent directory")

    images = read_images(raw_dirpath)
    width = args.width
    height = args.height
    rois = generate_rois(images, width, height)

    unlabeled_dirpath = args.out_dir

    try:
        rmdir_r(unlabeled_dirpath)
        mkdir(unlabeled_dirpath)
    except OSError:
        print(f"creating processed rois output dir at: {unlabeled_dirpath}")
        mkdir(unlabeled_dirpath)

    write_images(rois, unlabeled_dirpath)

    all_text_labels = ["donald-trump",
                       "rihanna",
                       "emma-chamberlain",
                       "barack-obama",
                       ]

    samples = launch_viewer(unlabeled_dirpath, args.width, args.height, all_text_labels)
    samples_no_redundancy = remove_redundancy_from_samples(samples, 0.65, 30)

    json_path = args.out_json
    write_sample_as_json(samples_no_redundancy, json_path)

    # read_sample = read_sample_from_json(json_path)

    # (sample_imgs, numeric_labels, text_labels) = label_dict_to_matrix(read_sample)

    # num_output_layers = len(text_labels)
    # print(f"num output layers: {num_output_layers}")

    # data_set = partition_sample(sample_imgs, numeric_labels, 10)

    # print(
    #     f"len training: {(len(data_set['training'][0]), len(data_set['training'][1]))}"
    # )
    # print(f"len test: {(len(data_set['test'][0]), len(data_set['test'][1]))}")

    # trained_model = train_model(
    #     data_set["training"][0], data_set["training"][1], num_output_layers, epochs=10
    # )

    # evaluation = evaluate_model(trained_model, data_set["test"][0], data_set["test"][1])

    # print(f"(loss, accuracy): {evaluation}")

    # predictions = classify_images(trained_model, text_labels, data_set["test"][0])

    # print(data_set["test"][1])
    # print(text_labels)
    # print(predictions)
    # show_classified_images_5x5(data_set["test"][0], predictions)


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
