import cv2
import math
import json
import cv2
from read_dir import read_dir
from write_file import write_file
from threading import Thread
import numpy as np

def create_test_by_folder_thread(folder,items_per_class,base_dir,path,classId,video_cache):
    subdir = read_dir("{}\\{}".format(base_dir,folder))
    print("[{}] started".format(folder))
    usable_videos = []
    for image in subdir:
        if image[-4:]==".png":
            if len(usable_videos) < items_per_class:
                file = video_cache[image] #"{}\{}".format(path,image[:-4])
                print("[{}] {}%".format(folder,round((len(usable_videos)+1)*100/items_per_class,2)))
                vidcap = cv2.VideoCapture(file)
                vidcap.set(cv2.CAP_PROP_POS_MSEC,(30*1000))
                success,img = vidcap.read()
                offset = 1
                while success:
                    cropped_image= img[40:500,20:480]
                    number_of_gray_pix = np.sum(cropped_image==126)
                    if number_of_gray_pix > 10_000:
                        cv2.imwrite("data\\test\\{}-{}.png".format(classId,len(usable_videos)), cropped_image)
                        write_file("data\\test\\{}-{}.txt".format(classId,len(usable_videos)), "{} 0.5 0.5 1 1".format(classId))
                        usable_videos.append(img[:-4])
                        success = False
                    else:
                        vidcap.set(cv2.CAP_PROP_POS_MSEC,((30 + 10*offset)*1000))
                        success,img = vidcap.read()
                        offset = offset + 1
    print("[{}] done".format(folder))

def generate_testing_images(max_items):
    path = "G:\Videos\Valorant"
    base_dir = "data\\all_images"
    dir = read_dir(base_dir)

    # print(dir)

    video_cache = {}
    with open("data\\all_images.json", 'r') as file:
        video_cache = json.loads(file.read().replace('\n', ''))

    items_per_class = math.ceil(max_items / len(dir))

    my_threads = []
    for folder in dir:
        my_threads.append(Thread(target=create_test_by_folder_thread, args=[folder,items_per_class,base_dir,path,len(my_threads),video_cache]))
        my_threads[len(my_threads)-1].start()

    for t in my_threads:
        t.join()
    print("done")
