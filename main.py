import importlib
import os
import random
import shutil
import unittest
import importlib.machinery

result_folder = "Mutations"

RUN_INFO = {
    "file_name": "code02.py",
    "code_function": "is_prime",
    "test_file": "test02.py",
    "test_class": "TestIsPrime",
    "test_functions": ["test_func"]
}

# RUN_INFO = {
#     "file_name": "code01.py",
#     "code_function": "BMI",
#     "test_file": "test01.py",
#     "test_class": "TestBMI",
#     "test_functions": ["test_underweight"]
# }
TEST = None
live_mutations = []
killed_mutations = []
stillborn_mutations_files = []

operator_list = {
    " + ":
        [" - ", " * ", " / ", " % ", " ** "],
    " - ":
        [" + ", " * ", " / ", " % ", " ** "],
    " * ":
        [" + ", " - ", " / ", " % ", " ** "],
    " / ":
        [" % ", " * ", " + ", " - ", " ** "],
    " % ":
        [" / ", " + ", " - ", " * ", " ** "],
    " ** ":
        [" / ", " + ", " - ", " * ", " % "],
    " < ":
        [" != ", " > ", " <= ", " >= ", " == "],
    " > ":
        [" != ", " < ", " <= ", " >= ", " == "],
    " <= ":
        [" != ", " < ", " > ", " >= ", " == "],
    " >= ":
        [" != ", " < ", " <= ", " > ", " == "],
    " == ":
        [" != ", " < ", " > ", " <= ", " >= "],
    " != ":
        [" == ", " < ", " > ", " <= ", " >= "],
    " and ":
        [" or "],
    " or ":
        [" and "],
}


class line_info:
    def __init__(self, line_num, operator, index):
        self.line_num = line_num
        self.operator = operator
        self.index = index


def create_possible_mutation(list_of_detect_logic, list_lines, mutation_folder_path):
    # Creating all possible mutation files
    # Save path of all files in list_mutate_file_path[]
    list_mutate_file_path = []
    number_mutate = 0
    for item in list_of_detect_logic:
        operator = item.operator
        alternatives = operator_list[operator]
        num_mutate = random.randint(1, len(alternatives))
        sample_alternatives = random.sample(alternatives, num_mutate)
        for sample in sample_alternatives:

            path = fr"{mutation_folder_path}\mutation{number_mutate}"
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)
            list_mutate_file_path.append(path)

            file_mutate = list_lines.copy()
            mutated_line = file_mutate[item.line_num][0:item.index] + sample + file_mutate[item.line_num][
                                                                       item.index + len(item.operator):]
            file_mutate[item.line_num] = mutated_line
            file_name = f"mutation.py"
            new_file_path = fr"{path}\{file_name}"
            # print(new_file_path)
            # list_mutate_file_path.append(new_file_path)

            with open(new_file_path, 'w') as out_file:
                out_file.writelines(file_mutate)

            with open(fr"{path}\test.py", 'w') as f:
                f.write(
                    f'from {result_folder}.mutation{number_mutate}.mutation import {RUN_INFO["code_function"]}\n')
                for line in TEST:
                    f.write(line)

            number_mutate += 1

    return list_mutate_file_path


def detect_operations(input_file):
    # Finding all lines with have Logic Operators and Comparison Operators and arithmatic
    # Save line number - operator index - operator
    list_detect_logic = []
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            for op in operator_list:
                number_of_substrings_found = lines[i].count(op)
                if number_of_substrings_found > 0:
                    indices = [index for index in range(len(lines[i])) if lines[i].startswith(op, index)]
                    for index in indices:
                        list_detect_logic.append(line_info(line_num=i, index=index, operator=op))

    return [list_detect_logic, lines]


def run_test(path):
    address = fr"{path}\test.py"
    module_name = address[:-3]

    # Import the module dynamically
    loader = importlib.machinery.SourceFileLoader(module_name, address)
    module = loader.load_module()

    # Get the test class from the module
    test_class = getattr(module, RUN_INFO["test_class"])

    # Create a TestSuite and add the test case
    suite = unittest.TestSuite()
    for test in RUN_INFO["test_functions"]:
        suite.addTest(test_class(test))

    # Run the test suite and store the results
    res = unittest.TestResult()
    suite.run(res)

    results = {
        'mutation_file_path': path,
        'passed': res.wasSuccessful(),
        'failed': len(res.failures),
        'errors': len(res.errors),
        'error_results': res.errors
    }

    # Print or store the test results
    return results


def calculate_score(live_numbers, killed_numbers,
                    stillborn_numbers, equivalent_number=0):
    total_mutations = live_numbers + killed_numbers + stillborn_numbers - equivalent_number
    print(f"Total Mutations: {total_mutations}")
    effective_mutations = killed_numbers
    return (effective_mutations / total_mutations) * 100


if __name__ == "__main__":
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)

    os.makedirs(result_folder)

    with open(RUN_INFO["test_file"], 'r') as file:
        TEST = file.readlines()

    [detect_logic, list_line] = detect_operations(RUN_INFO["file_name"])
    list_mutations_file_path = create_possible_mutation(detect_logic, list_line, result_folder)

    # print(list_mutate_file_path)

    for p in list_mutations_file_path:
        result = run_test(p)
        print(result)

        if result['passed'] is True:
            live_mutations.append(p)
        elif result['passed'] is False and result["errors"] == 0:
            killed_mutations.append(p)
        if result['errors'] > 0:
            stillborn_mutations_files.append(p)

    print()
    mutation_score = calculate_score(live_numbers=len(live_mutations),
                                     killed_numbers=len(killed_mutations),
                                     stillborn_numbers=len(stillborn_mutations_files))
    print(f"Mutation Score: {mutation_score}")
