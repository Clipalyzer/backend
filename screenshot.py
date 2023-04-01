import random
import subprocess
import cv2

import sys
import os
import numpy as np
from generator import image_processor, sub_list_from_frame_position, read_dir

sys.path.append("./yolov5")


def get_image(vidcap):
    success, image = vidcap.read()
    if success:
        cropped_image = sub_list_from_frame_position(image, "map")
        number_of_gray_pix = np.sum(cropped_image == 126)
        if number_of_gray_pix > 10_000:
            cropped_image = image_processor(cropped_image)
            return success, True, image
        return True, False, None
    return False, False, None


def do_screenshot(file):
    # file = f"5k ölig.mp4"
    dest_file = file.replace(".mp4", ".jpg")
    dest_path = dest_file
    # print(f"Writing result to {dest_path}")

    vidcap = cv2.VideoCapture(file)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    success, has_map, image = get_image(vidcap)
    n = 0
    if has_map:
        cv2.imwrite(dest_path, image)
        return dest_path

    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, n * 1000)
        current_frame = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
        success, has_map, image = get_image(vidcap)
        if has_map:
            cv2.imwrite(dest_path, image)
            return dest_path
        n = n + 1
    return "no"


dir = "G:\\Videos\\Videos\\Valorant\\"

print(sys.argv)

if len(sys.argv) == 1:
    print(f"Usage: python {sys.argv[0]} [<folder>|<filename>]")
    sys.exit()

if sys.argv[1].endswith(".mp4"):
    dir = sys.argv[1]
    print(f"Screenshotting video {dir}")
    do_screenshot(dir)

if not sys.argv[1].endswith(".mp4"):
    dir = sys.argv[1]
    print(f"Screenshotting all videos inside {dir}")
    d = read_dir(dir)
    d1 = [a for a in d if a.endswith(".mp4")]
    length = len(d1)
    for idx, img in enumerate(d1):
        print(f"{idx+1} of {length} {round((idx+1)*100/length,2)}%")
        do_screenshot(dir + img)


sys.exit()
