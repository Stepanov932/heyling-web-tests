import inspect
import re

from importlib import import_module
from os.path import join, split


from constants.constants import PROJECT_PATH


def find_functions(module, function_mask=None):
    functions = inspect.getmembers(import_module(module), inspect.isfunction)
    if function_mask:
        matching_functions = []
        for function in functions:
            if re.fullmatch(function_mask, function[0]):
                matching_functions.append(function)
        return matching_functions
    else:
        return functions


def convert_to_module(file_path):
    return '.'.join(split(file_path.replace(join(PROJECT_PATH, ''), ''))).replace('.py', '')


def convert_to_modules(files_paths):
    modules = []
    for file_path in files_paths:
        modules.append(convert_to_module(file_path))
    return modules
