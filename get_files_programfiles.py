from os import listdir
from os.path import isfile, join
import os
import shutil


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



# def get_file_from_path(path):
#     my_list = os.listdir(path)
#     list_of_path_directory = []
#     only_files = []
#     help_recursive_function(path, list_of_path_directory, only_files, my_list)
#     # print(list_of_path_directory)
#     print(only_files)

# def help_recursive_function(path, list_of_path_directory, only_files, all_the_folder_in_this_path):
#     if len(all_the_folder_in_this_path) == 0:
#         return
#     # check if thia path is directory
#     var = path + "\\" + all_the_folder_in_this_path[0]
#
#     if os.path.isdir(var):
#         list_of_path_directory.append(var)
#         my_list = os.listdir(var)
#         all_the_folder_in_this_path[0]
#         help_recursive_function(var, list_of_path_directory, only_files, my_list)
#     # check if thia path is file
#     if os.path.isfile(var):
#         only_files.append(var)
#     else:
#         return
