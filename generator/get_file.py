from read_dir import read_dir
def get_file():
    path = "G:\Videos\Valorant"
    obj = read_dir(path)
    for entry in obj :
        return "{}\{}".format(path,entry.name)
    return ""
