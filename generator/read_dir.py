import os


def read_dir(path):
    ret = []
    obj = os.scandir(path)
    for entry in obj:
        if entry.is_dir() or entry.is_file():
            ret.append(entry.name)
    return ret
