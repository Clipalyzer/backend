import os

# https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
def create_folder(path):
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)