from .create_folder import create_folder
from .fetch_maps import fetch_maps


def generate_file_system():
    create_folder("data")
    create_folder("data\\obj")
    create_folder("data\\backup")
    create_folder("data\\test")
    for map in fetch_maps():
        create_folder("data\\all_images\\{}".format(map))
        create_folder("data\\obj\\{}".format(map))
