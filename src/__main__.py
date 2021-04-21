import sys

from image_sampler import (
    read_and_reduce_samples,
    remove_redundancy_from_samples,
    show_images,
)


def main(argv):
    ariana = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/ariana-grande"
    justin = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber"
    rihana = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/rihana"
    tyler = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/tyler"

    samples = read_and_reduce_samples(
        ["ariana", "justin", "rihana", "tyler"],
        [ariana, justin, rihana, tyler],
        150,
        150,
    )

    for (label, images) in samples.items():
        print(f"{label}: {len(images)}")

    samples_without_redundancy = remove_redundancy_from_samples(samples, 0.65)

    print("\nAfter removing redundancy\n")

    for (label, images) in samples_without_redundancy.items():
        print(f"{label}: {len(images)}")

    show_images(samples_without_redundancy, 500)


if __name__ == "__main__":
    main(sys.argv[1:])
