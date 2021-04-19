import sys

from faces import read_image, detect_faces, add_rectangle, showFaces


def main(argv):
    img = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber/justin2.png")
    faces, face_images = detect_faces(img)
    showFaces(img, faces)


if __name__ == "__main__":
    main(sys.argv[1:])
