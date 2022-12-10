from read_dir import read_dir
from create_folder import create_folder
from write_file import write_file
from frame_positions import sub_list_from_frame_position
import pytesseract
import cv2
from threading import Thread
import os
import re
import math
import json
import numpy as np
from pathlib import Path

def grab_images_within_range(list,path,i):
    n = 0
    my_dict = {}
    for entry in list:
        file = "{}\{}".format(path,entry)
        file_name = "data\\all_images\{}.png".format((len(list)*i)+n)
        print("[{}] {}/{} {}".format(str(i).rjust(2),n,len(list),file_name))
        
        # emit('generate_initial', json.dumps({"thread":i,"current":n,"max":len(list),"file_name":file_name}))

        test = 0

        vidcap = cv2.VideoCapture(file)
        vidcap.set(cv2.CAP_PROP_POS_MSEC,(30*1000))
        success,image = vidcap.read()
        while success:
            cropped_image = sub_list_from_frame_position(image,"map")

            number_of_gray_pix = np.sum(cropped_image==126)
            if number_of_gray_pix < 10_000:
                test = test + 1
                vidcap.set(cv2.CAP_PROP_POS_MSEC,(test*30*1000))
                success,image = vidcap.read()
            else:
                cv2.imwrite(file_name, cropped_image)
                my_dict[file_name] = file
                # write_file("{}.txt".format(file_name[:-4]),file)
                break
        n = n + 1
    write_file("data\\{}.json".format(str(i)),json.dumps(my_dict))

def grab_images_from_video(path):
    number_of_threads = os.cpu_count()
    threads = []
    obj = read_dir(path)
    create_folder("data\\all_images")
    items_per_thread = math.ceil(len(obj)/number_of_threads)
    i = 0
    while i < number_of_threads:
        sub_list = obj[i*items_per_thread:(i+1)*items_per_thread]
        t = Thread(target=grab_images_within_range, args=[sub_list,path,i])
        t.start()
        threads.append(t)
        i = i + 1
    for t in threads:
        t.join()
    jsons = read_dir("data")
    my_dict = {}
    for item in jsons:
        if item[-5:]==".json":
            file_name = 'data\\{}'.format(item)
            with open(file_name, 'r') as file:
                data = json.loads(file.read().replace('\n', ''))
                for key in data:
                    # data\\all_images\\
                    my_dict[key.split("\\")[2]] = data[key]
            os.remove(file_name)
    write_file("data\\all_images.json",json.dumps(my_dict))
    create_folder("data\\obj")

# Cheers twitch.tv/TessilRx
def find_grayscales(path):
    dir = "data\\all_images"
    obj = read_dir(dir)
    # summed = np.sum(output, axis=2)
    for image in obj:
        file_name = "{}\\{}".format(dir,image)
        img = cv2.imread(file_name)
        # https://www.geeksforgeeks.org/opencv-counting-the-number-of-black-and-white-pixels-in-the-image/
        number_of_white_pix = np.sum(img==126)
        print("{}: {}".format(image,number_of_white_pix))
        if number_of_white_pix < 10_000:
            print("{}: {}".format(image,number_of_white_pix))
            # https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python
            Path(file_name).rename("{}\\test\\{}".format(dir,image))

# Map: #7e7e7e (126,126,126)

# Singlethreadded (Threads nacheinander)
# real    2m49,319s
# user    0m0,015s
# sys     0m0,015s

# Multithreadded (24 Threads)
# real    1m23,339s
# user    0m0,000s
# sys     0m0,031s