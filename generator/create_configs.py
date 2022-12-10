from .read_dir import read_dir
from .write_file import write_file
import os

def create_configs():
    print("[CONFIG] Creating Configs.")
    trainTXT = open("data\\train.txt", "w")
    names = []

    print("[CONFIG] Reading data\\obj")
    class_number = 0
    for classId in read_dir("data\\obj\\"):
        dir = read_dir("data\\obj\\{}".format(classId))
        print("[CONFIG] Reading data\\obj\\{}".format(classId))
        for image in dir:
            write_file("data\\obj\\{}\\{}.txt".format(classId,image[:-4]),"{} 0.5 0.5 1 1".format(class_number))
            trainTXT.write("data\\obj\\{}\\{}.txt\n".format(classId,image[:-4]))
        if len(dir)>0:
            names.append(classId)
            class_number = class_number + 1
    trainTXT.close()
    write_file("data\\obj.names", "\n".join(names))
    print("[CONFIG] Wrote {} classes into data\\obj.names".format(len(names)))

    print("[CONFIG] Reading data\\tests")
    testTXT = open("data\\test.txt", "w")
    names = []

    class_number = 0
    for image in read_dir("data\\test\\"):
        testTXT.write("data\\test\\{}.txt\n".format(image[:-4]))
    testTXT.close()

    print("[CONFIG] Wrote data\\tests.txt")

    cwd = os.getcwd().replace("\\","\\\\")

    datayaml = [
        "# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]",
        "path: \"{}\\\\data\"".format(cwd),
        "train: \"{}\\\\data\\\\obj\"".format(cwd),
        "val: \"{}\\\\data\\\\test\"".format(cwd),
        "test: \"{}\\\\data\\\\test\"".format(cwd),
        "",
        "# Classes",
        "names:",
    ]

    i=0
    for map in names:
        datayaml.append("   {}: {}".format(i,map))
        i = i + 1

    write_file("data.yaml","\n".join(datayaml))
    print("[CONFIG] Wrote data.yaml")

    write_file("data\\obj.data","\n".join([
        "classes = {}".format(class_number),
        "train = data/train.txt",
        "valid = data/test.txt",
        "names = data/obj.names",
        "backup = data/backup",
    ]))

    print("[CONFIG] Wrote data\\obj.data")
    