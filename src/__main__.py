import sys

from face_utils import (
    show_images,
    reduce_image_resolution,
    remove_redundancy_from_samples,
    write_images,
    write_sample_as_json,
    read_sample_from_json,
    read_images,
    generate_rois,
)
from image_viewer import launch_viewer


def main(argv):
    # dirpath = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples"
    # images = read_images(dirpath)

    # rois = generate_rois(images, 200, 200)
    unlabeled_dirpath = "/home/sebastian/university/algorithms_and_data_structures/project_template/unlabeled-images"
    # write_images(rois, unlabeled_dirpath)

    samples = launch_viewer(unlabeled_dirpath, 200, 200)
    samples_no_redundancy = remove_redundancy_from_samples(samples, 0.65)
    print(len(samples["rihana"]))
    print(len(samples_no_redundancy["rihana"]))


if __name__ == "__main__":
    main(sys.argv[1:])
