import sys

from face_utils import (
    reduce_samples,
    show_images,
    reduce_image_resolution,
    reduce_image_to_roi,
    remove_redundancy_from_samples,
    write_sample_as_json,
    read_sample_from_json
)
from image_viewer import launch_viewer


def main(argv):
    samples = launch_viewer()
    roi_samples = reduce_samples(samples, reduce_image_to_roi)
    reduced_samples = reduce_samples(
        roi_samples, lambda img: reduce_image_resolution(img, 120, 120)
    )
    samples_no_redundancy = remove_redundancy_from_samples(reduced_samples, 0.65)

    samples_path = "/home/sebastian/university/algorithms_and_data_structures/project_template/samples.json"
    write_sample_as_json(samples_no_redundancy, samples_path)

    read_sample = read_sample_from_json(samples_path)
    show_images(read_sample, 500)


if __name__ == "__main__":
    main(sys.argv[1:])
