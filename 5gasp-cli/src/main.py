# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-01 16:31:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-20 15:12:41

# Typer
import typer

#ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from Testcase.testcase import Testcase
from Execution.execution import Execution

app = typer.Typer()
state = {"verbose": False}

yaml = YAML(typ = "safe") # safe mode - loads a document without resolving unknown tags
yaml.default_flow_style = False

@app.command()
def create_tests(
    config_file: str = typer.Option(None, 
                                        help = "Name of the config file \
                                        containing the desired test' names"),
    output_filename: str = typer.Option("testing-descriptor.yaml", 
                                        help = "Output filename"),
    clear_executions: bool = typer.Option(False, 
                                        help = "Clear executions")
    ):
    '''
    Create tests descriptor from a given config.yaml containing the intended tests
    
    Parameters
    ----------
    config_file : str (optional)
        A string representing the name of the config file containing 
        the names of the intended tests.
    output_filename : str (optional)
        A string representing the name of the output file for the
        test descriptor.
    clear_executions : bool (optional)
        A boolean flag indicating whether to clear previous test
        execution history from the test descriptor before creating the new descriptor.
    
    Returns
    -------
    None
    '''
    if state["verbose"]: 
        print("Reading configuration file...")

    try:
        with open(config_file, "r") as stream:
            try:
                intended_tests = yaml.load(stream) # dict
            except YAMLError as exc:
                print(exc)
    except FileNotFoundError as e:
        print(f"Error! File {config_file} not found!")
        return

    if state["verbose"]: 
        print("Configuration file read!")

    descriptor = reset_sections(intended_tests, clear_executions)

    if state["verbose"]: 
        print("Creating the descriptor...")

    with open("../../" + output_filename, "w") as file:
        try:
            yaml.dump(descriptor, file)
        except YAMLError as exc:
            print(exc)

    if state["verbose"]:
        print("Descriptor generated, check it at the descriptor folder")


def reset_sections(intended_tests: dict(), clear_executions: bool):
    '''
    Reset user-given sections to later be filled by the user

    Parameters
    ----------
    intended_tests : dict
        Dictionary containing tests information from test_information.yaml.
    clear_executions : bool
        Boolean for whether to clear existing executions.
    
    Returns
    -------
    tests: dict
        Updated testing descriptors.
    '''
    # tests info from test_information.yaml
    tests_info = read_tests_info()

    # testing descriptors from testing-descriptor_nods.yaml
    tests = read_testing_descriptors()

    # existing tests
    test_types = tests_info['tests']['testbed_itav']

    tests['test_phases']['setup']['testcases'].clear()
    
    intended_test_types = [type for type in test_types 
                            if type in intended_tests['tests']]
    
    # add intended test to testcases
    for i, test in enumerate(intended_test_types, 1):
        test = test_types[test]
        
        testcase = Testcase(
                        id = i,
                        type = test['test_type'],
                        name = test['name'],
                        description = test['description'],
                    )

        testcase.create_testcase()

        # add parameters to testcase
        for variable in test['test_variables']:
            testcase.add_parameter({'key': variable['variable_name'], 'value': ""})

        # add testcase to tests
        tests['test_phases']['setup']['testcases'].append(testcase.testcase)
        
    if clear_executions:
      
        tests['test_phases']['execution'].clear()

        execution = Execution(1, "", [1])
        
        execution.create_execution()

        tests['test_phases']['execution'] = [
                {"batch_id": 1,"executions": [execution.execution]}
        ]

    return tests


def read_tests_info():
    '''
    Read tests information from test_information.yaml

    Returns
    -------
    test_information : dict
        Dictionary containing tests information from test_information.yaml.
    '''
    try:
        with open("../../helpers/test_information.yaml", "r") as stream:
            try:
                test_information = yaml.load(stream)
            except YAMLError as exc:
                print(exc)
    except FileNotFoundError as e:
        print(f"Error! File test_information.yaml not found!")
        return

    return test_information


def read_testing_descriptors():
    '''
    Read testing descriptors from testing_descriptor_nods.yaml
    
    Returns
    -------
    testing_descriptor_nods : dict
        Dictionary containing the testing descriptors.
    '''
    try:
        with open("../../helpers/testing-descriptor_nods.yaml", "r") as stream:
            try:
                testing_descriptor_nods = yaml.load(stream)
            except YAMLError as exc:
                print(exc)
    except FileNotFoundError as e:
        print(f"Error! File testing-descriptor_nods.yaml not found!")
        return

    return testing_descriptor_nods
     

@app.callback()
def main(verbose: bool = False):
    """
    5GASP CLI
    """
    if verbose:
        #print("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()
