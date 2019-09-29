import os

from utils import find_files


if __name__ == "__main__":
    valid = './valid'
    image = './image'
    mask = './mask'

    files = find_files(valid, '.png')
    print(files)
    arr = []
    for file in files:
        file_name = os.path.split(file['path'])[1]
        file_name_without = os.path.splitext(file_name)[0]
        arr.append(file_name_without)

    files = find_files(image, '.png')
    print(files)
    for file in files:
        file_name = os.path.split(file['path'])[1]
        file_name_without = os.path.splitext(file_name)[0]
        if file_name_without in arr:
            os.rename(file['path'], "new_valid/image/" + file_name)

    files = find_files(mask, '.png')
    print(files)
    for file in files:
        file_name = os.path.split(file['path'])[1]
        file_name_without = os.path.splitext(file_name)[0]
        if file_name_without in arr:
            os.rename(file['path'], "new_valid/mask/" + file_name)
