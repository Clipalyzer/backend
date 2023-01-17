import os
from generator import (
    generate_file_system,
    grab_images_from_video,
    grab_detailed_images_from_video,
    generate_testing_images,
    create_configs,
    image_processor,
    read_dir,
    write_file,
)
import pytesseract
import sys
import cv2
import numpy as np
import math
from queue import Queue
import random

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# video_path = "G:\Videos\Valorant"
video_path = "G:\Videos\Videos\Valorant"

q = Queue()

# number_of_images = 0
# classes = read_dir("data\\obj")
# for class_name in classes:
#     for image in read_dir(f"data\\obj\\{class_name}"):
#         if image.endswith(".png"):
#             number_of_images = number_of_images + 1

# current_i = 0
# for class_name in classes:
#     for image in read_dir(f"data\\obj\\{class_name}"):
#         # print(f"Updating {image}")
#         if image.endswith(".png"):
#             file_name = f"data\\obj\\{class_name}\\{image}"
#             img = cv2.imread(file_name)
#             img = image_processor(img)
#             cv2.imwrite(file_name, img)
#             print(f"{round(current_i/number_of_images*100,2)}% {current_i} / {number_of_images} {file_name}")
#             current_i = current_i + 1
#             # cv2.imwrite(image, img)

# print(images)
# d = read_dir("data\\all_images\\Ascent\\")
# img = cv2.imread(f"data\\all_images\\Ascent\\{d[random.randint(0, len(d))]}")
# img = image_processor(img)
# cv2.imwrite("test.png", img)

if len(sys.argv) <= 1:
    print('Error! Start with "python {} s1" or "python {} s2"'.format(sys.argv[0], sys.argv[0]))
    print('> Use "python {} s1" to generate categorizable images from your clips.'.format(sys.argv[0]))
    print("  Videos must be inside {}".format(video_path))
    print(
        '> Use "python {} s2" create learning enviroment after categorizing your clips from hand!'.format(sys.argv[0])
    )
    sys.argv.append("")
    sys.exit()

if sys.argv[1] == "s1":
    # Step #1
    generate_file_system()
    grab_images_from_video(video_path, q)
    print("You may now filter your images by hand. Move them from data/all_images to obj/all_images/{map}")

if sys.argv[1] == "s2":
    # Step #2
    number_of_learn_images_per_thread = 800
    grab_detailed_images_from_video(number_of_learn_images_per_thread)

    number_of_testing_images = 300
    generate_testing_images(number_of_testing_images)

    create_configs()


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.5140])


if sys.argv[1] == "s3":
    # Step #3
    classId = -1
    for dir in read_dir("data\obj"):
        classId = classId + 1
        for file in read_dir(f"data\obj\{dir}"):
            if file.endswith(".png"):
                write_file(
                    "data\\obj\\{}\\{}.txt".format(dir, file.split(".")[0]),
                    "{} 0.5 0.5 1 1".format(classId),
                )
