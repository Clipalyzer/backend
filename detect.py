import random
import subprocess
import cv2

import sys
import os
import numpy as np
from generator import image_processor, sub_list_from_frame_position, read_dir

sys.path.append("./yolov5")

try:
    os.mkdir("tests")
except OSError as error:
    print("Folder tests already existing")


dir = "G:\\Videos\\Videos\\Valorant\\"
d = read_dir(dir)
file = f"{dir}\\{random.choice(d)}"
print(f"Checking file {file}")


def get_image(vidcap):
    success, image = vidcap.read()
    if success:
        cropped_image = sub_list_from_frame_position(image, "map")
        number_of_gray_pix = np.sum(cropped_image == 126)
        if number_of_gray_pix > 10_000:
            cropped_image = image_processor(cropped_image)
            return success, True, cropped_image
        return True, False, None
    return False, False, None


print("Creating images from the video", end="\r")
vidcap = cv2.VideoCapture(file)
frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
success, has_map, image = get_image(vidcap)
n = 0
if has_map:
    cv2.imwrite("tests/-1.png", image)
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC, n * 1000)
    current_frame = vidcap.get(cv2.CAP_PROP_POS_FRAMES)
    # print(frame_count * 100 / ((n + 1) * 1000))

    print(
        f"Creating images from the video: {current_frame} / {frame_count} {round(current_frame * 100 / frame_count,2)}%",
        end="\r",
    )
    success, has_map, image = get_image(vidcap)
    if has_map:
        cv2.imwrite(f"tests/{n}.png", image)
    n = n + 1
print("100%")

print("Checking images with yolov5")
cmd = "python yolov5/detect.py --weights ./best_color.pt --source ./tests --save-txt --save-conf --nosave"
subprocess.run(cmd.split(" "), capture_output=True, text=True)
print("Done checking images")

print("Grabbing Maps")
maps = {}
maps_conf = {}
with open("data/obj.names", "r") as content:
    data = content.read().split("\n")
    for n, map in enumerate(data):
        maps[n] = {"name": map, "count": 0, "num": 0, "cnum": 0, "idx": n}
# print(maps)

print("Calculating Map")
d = read_dir("yolov5/runs/detect")
dir = f"yolov5/runs/detect/{d[len(d)-1]}/labels"
for file in read_dir(dir):
    with open(f"{dir}/{file}", "r") as content:
        data = content.read().replace("\n", "").split(" ")
        idx = int(data[0])
        maps[idx]["count"] = maps[idx]["count"] + 1
        maps[idx]["num"] = maps[idx]["num"] + float(data[len(data) - 1])
        maps[idx]["cnum"] = maps[idx]["num"] / maps[idx]["count"]

final_maps = []
for idx in maps:
    if maps[idx]["count"] > 0:
        final_maps.append(maps[idx])

final_maps.sort(key=lambda x: x["count"])
print(final_maps)
m = final_maps[0]

print(
    "Found map: {} with a overall confidence of {}% @ {} images".format(
        m["name"], round(m["cnum"] * 100, 2), m["count"]
    )
)

subprocess.run("rm -rf tests/".split(" "), capture_output=True, text=True)
subprocess.run("rm -rf yolov5/runs/detect/".split(" "), capture_output=True, text=True)

sys.exit()
