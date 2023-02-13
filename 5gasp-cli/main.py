# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-01 16:31:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-13 17:29:35

from pprint import pprint

# Typer
import typer
from typing import Tuple

#ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

from testcase import Testcase
from execution import Execution

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
    clear_testcases: bool = typer.Option(False, 
                                        help = "Clear testcases"),
    clear_executions: bool = typer.Option(False, 
                                        help = "Clear executions")
    ):
    '''
    Create tests descriptor from a given config.yaml containing the intended tests
    '''
    if state["verbose"]: print("Reading configuration file...")

    with open(config_file, "r") as stream:
        try:
            intended_tests = yaml.load(stream) # dict
        except YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Configuration file read!")

    descriptor = reset_sections(intended_tests, clear_testcases, clear_executions)

    if state["verbose"]: print("Creating tests file...")

    with open(output_filename, "w") as file:
        try:
            t = yaml.dump(descriptor, file)
        except YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Tests file created!")


def reset_sections(
        intended_tests: dict(), 
        clear_testcases: bool, 
        clear_executions: bool
    ):
    '''
    Reset user-given sections to later be filled
    '''
    # tests info from test_information.yaml
    tests_info = read_tests_info()

    # testing descriptors from testing-descriptor_nods.yaml
    tests = read_testing_descriptors()

    # existing tests
    test_types = tests_info['tests']['testbed_itav']

    if clear_testcases:

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
            [testcase.add_parameter({'key': variable['variable_name'], 'value': ""}) 
                for variable in test['test_variables']]

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
    '''
    with open("../helpers/test_information.yaml", "r") as stream:
        try:
            test_information = yaml.load(stream)
        except YAMLError as exc:
            print(exc)

    return test_information


def read_testing_descriptors():
    '''
    Read testing descriptors from testing_descriptor_nods.yaml
    '''
    with open("../helpers/testing-descriptor_nods.yaml", "r") as stream:
        try:
            testing_descriptor_nods = yaml.load(stream)
        except YAMLError as exc:
            print(exc)
    
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