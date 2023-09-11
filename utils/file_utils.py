from os import listdir
from os.path import isfile, join, split
from re import fullmatch


def read_file(path):
    with open(path, 'r') as file:
        return file.read()


def list_files(path, file_mask=None):
    files = []
    if isfile(path):
        if not file_mask or fullmatch(file_mask, split(path)[-1]):
            files.append(path)
    else:
        for file in listdir(path):
            sub_files = list_files(join(path, file), file_mask)
            for sub_file in sub_files:
                files.append(sub_file)
    return files


def list_py_files(path, file_mask=None):
    all_files = list_files(path, file_mask)
    py_files = []
    for file in all_files:
        if file.endswith('.py'):
            py_files.append(file)
    return py_files
