import sys
import traceback

from time import sleep


from constants.constants import TESTS_PATH
from utils.file_utils import list_py_files
from utils.function_utils import convert_to_modules, find_functions


def main() -> int:
    exceptions = []
    test_files = list_py_files(TESTS_PATH, '^test_.*')
    print(f'Found {len(test_files)} test_files')
    for test_file in test_files:
        print(f'   {test_file}')
    test_modules = convert_to_modules(test_files)
    test_modules_functions = {}

    for test_module in test_modules:
        test_functions = find_functions(test_module, '^test_.*')
        test_modules_functions[test_module] = test_functions
        print(f'Fount {len(test_functions)} functions in module {test_module}')
        for function in test_functions:
            print(f'   {function[0]}')

    for test_module in test_modules_functions.keys():
        test_functions = test_modules_functions[test_module]
        print(f'Starting test module {test_module}')
        for test_function in test_functions:
            result = 'FAILED'
            print(f'   Test: {test_function[0]}')

            try:
                test_function[1]()
                result = 'PASSED'
            except Exception:
                error = (f'An error occurred in test {test_module}.{test_function[0]}!'
                         f'\n{traceback.format_exc()}')
                exceptions.append(error)

            print(f'   Result: {result}')

    sleep(0.5)
    if len(exceptions) > 0:
        raise Exception('Some tests have failed!\n\n' + '\n\n'.join(exceptions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
