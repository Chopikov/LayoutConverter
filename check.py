import os


def find_files(folder):
    if folder is None:
        raise Exception('Finding of files failed')

    try:
        tree = os.walk(folder)
        files = []
        for _ in tree:
            files = files.__add__([{'path': os.path.join(_[0], f), 'name': f}
                                   for f in filter(lambda x: x[-5:].lower() == '.json', _[2])])
    except WindowsError:
        raise Exception('Finding of files failed')
    return files


def find_files1(folder):
    if folder is None:
        raise Exception('Finding of files failed')

    try:
        tree = os.walk(folder)
        files = []
        for _ in tree:
            files = files.__add__([{'path': os.path.join(_[0], f), 'name': f}
                                   for f in filter(lambda x: x[-4:].lower() == '.png', _[2])])
    except WindowsError:
        raise Exception('Finding of files failed')
    return files


if __name__ == "__main__":
    src = './src'
    check = './check'
    files = find_files(src)
    print(files)
    arr = []
    for file in files:
        file_name = os.path.split(file['path'])[1]
        file_name_without = os.path.splitext(file_name)[0]
        arr.append(file_name_without)

    files = find_files1(check)
    print(files)
    for file in files:
        file_name = os.path.split(file['path'])[1]
        file_name_without = os.path.splitext(file_name)[0]
        if file_name_without not in arr:
            print(file_name)
        else:
            print('ok')