from read_dir import read_dir
import os

def cleanup_classes():
    counter = 0
    dir = read_dir("data\\all_images")
    for item in dir:
        d = "data\\all_images\\{}".format(item)
        subdir = read_dir(d)
        if len(subdir) == 0:
            os.rmdir(d)
        else:
            counter = counter + 1
    return counter