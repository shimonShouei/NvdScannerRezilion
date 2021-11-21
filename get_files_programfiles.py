from os import listdir
from os.path import isfile, join
import os
import shutil


def get_file_from_path():
    list_of_path_directory = []
    list_of_path_files = []
    path = ["C:\Program Files", "C:\Program Files (x86)"]
    for i in path:
        get_file_from_path_by_dfs(list_of_path_directory, list_of_path_files, i)
        print(list_of_path_files)
    return list_of_path_files


def get_file_from_path_by_dfs(list_of_path_directory, list_of_path_files, path):
    if os.path.isdir(path) and path not in list_of_path_directory:
        list_of_path_directory.append(path)
        for neighbour in os.listdir(path):
            try:
                get_file_from_path_by_dfs(list_of_path_directory, list_of_path_files, path + "\\" + neighbour)
            except PermissionError:
                pass
    # check if thia path is file
    elif os.path.isfile(path) and path not in list_of_path_files:
        list_of_path_files.append(path)
    else:
        pass

