# This file will create exports for each .dart file in the folder

from pathlib import Path

folder_path = '/Users/kales/Documents/code/flutter/projects/caroby/lib/src/extensions'

# Create a Path object for the folder
folder = Path(folder_path)

# Get a list of all items (files and subfolders) in the folder
folder_contents = list(folder.iterdir())

# Filter out subfolders (directories) and files
files = [item for item in folder_contents if item.is_file()]

# Here we get input from user to detect which folders we need
# For example if we say 1 then it will be only file name
# If we say 2 then it will be => lib/file.name
path_length = int(input("Path length: "))

export_paths = []

for file in files:
    list_path = str(file).split("/")
    length = list_path.__len__()
    min_length = length-path_length

    list_path = list_path[min_length:]

    new_path = '/'.join(list_path)

    new_path = "export '{}';".format(new_path)

    export_paths.append(new_path)

with open("extensions.dart", 'w') as file:
    for x in export_paths:
        file.write("{}\n".format(x))