import os
import shutil


def create_temp_dir():
    temp_dir_name = 'temp'  # TODO: generate random name to avoid clashes
    if not os.path.exists(temp_dir_name):
        os.makedirs(temp_dir_name)
    return temp_dir_name


def delete_temp_dir(temp_dir_name):
    shutil.rmtree(temp_dir_name)
