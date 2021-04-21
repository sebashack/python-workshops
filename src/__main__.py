import cv2
import numpy as np
import sys
import time

from image_sampler import read_and_reduce_samples, show_images


def main(argv):
    ariana = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/ariana-grande"
    justin = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber"
    rihana = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/rihana"
    tyler = "/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/tyler"

    samples = read_and_reduce_samples(["ariana", "justin", "rihana", "tyler"],
                                      [ariana, justin, rihana, tyler], 150, 150)


    show_images(samples, 500)

#   # src = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber/justin2.png")
#   # src2 = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber/justin1.png")
#   src = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/correlation/phase7.png")
#   src2 = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/correlation/phase8.png")
#   # scale_percent = 50
#   # width = int(src.shape[1] * scale_percent / 100)
#   # height = int(src.shape[0] * scale_percent / 100)

#   # dsize = (width, height)
#   output = cv2.resize(src, (120, 120), interpolation = cv2.INTER_NEAREST)
#   gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

#   output2 = cv2.resize(src2, (120, 120), interpolation = cv2.INTER_NEAREST)
#   gray_output2 = cv2.cvtColor(output2, cv2.COLOR_BGR2GRAY)

#   # ret,thresh1 = cv2.threshold(gray_output,255,255,cv2.THRESH_BINARY)


#   c1 = cv2.phaseCorrelate(np.float32(gray_output), np.float32(gray_output))
#   c2 = cv2.phaseCorrelate(np.float32(gray_output2), np.float32(gray_output))

#   res = cv2.matchTemplate(gray_output, gray_output, cv2.TM_CCOEFF_NORMED)

#   src = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/correlation/phase3.png")
#   src2 = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/correlation/phase4.png")
#   # src = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber/justin2.png")
#   # src2 = read_image("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber/justin1.png")

#   output = cv2.resize(src, (120, 120), interpolation = cv2.INTER_NEAREST)
#   gray_output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

#   output2 = cv2.resize(src2, (120, 120), interpolation = cv2.INTER_NEAREST)
#   gray_output2 = cv2.cvtColor(output2, cv2.COLOR_BGR2GRAY)

#   c1 = cv2.phaseCorrelate(np.float32(gray_output), np.float32(gray_output))
#   c2 = cv2.phaseCorrelate(np.float32(gray_output2), np.float32(gray_output))

#   print(c2)

#   # cv2.imshow("img", gray_output2)
#   # cv2.waitKey(0)
#    read_images("/home/sebastian/university/algorithms_and_data_structures/project_template/face-examples/justin-bieber")


if __name__ == "__main__":
    main(sys.argv[1:])
