# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-01 16:31:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-07 18:07:48

import typer
import yaml
from pprint import pprint

app = typer.Typer()
state = {"verbose": False}


@app.command()
def create_tests(
    test_description: str,
    config_file: str = typer.Option(...)
    ):
    '''
    Create tests descriptor from a given config.yaml containing the intended tests
    '''
    if state["verbose"]: print("Reading configuration file...")

    with open(config_file, "r") as stream:
        try:
            intended_tests = yaml.safe_load(stream) # dict
        except yaml.YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Configuration file read!")

    # tests info from test_information.yaml
    tests_info = read_tests_info()

    # testing descriptors from testing-descriptor_nods.yaml
    tests = read_testing_descriptors()

    # existing tests
    test_types = tests_info['tests']['testbed_itav']

    tests['test_phases']['setup']['testcases'].clear()
    
    intended_test_types = [type for type in test_types if type in intended_tests['tests']]
    
    # add intended test to testcases
    [tests['test_phases']['setup']['testcases'].append(
            {
                'testcase_id': i,
                'type': test_types[test]['test_type'],
                'scope': "",
                'name': test_types[test]['name'],
                'description': test_types[test]['description'],
                'parameters': [
                    {
                        'key': key['variable_name'],
                        'value': "# user-provided"
                    } for key in test_types[test]['test_variables']
                ],
            }
        ) for i, test in enumerate(intended_test_types, 1)
    ]

    if state["verbose"]: print("Creating tests file...")

    with open("testing-descriptor.yaml", "w") as file:
        try:
            t = yaml.safe_dump(
                tests, 
                file, 
                sort_keys = False, 
                default_flow_style = False,)
        except yaml.YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Tests file created!")
    

def read_tests_info():
    '''
    Read tests information from test_information.yaml
    '''
    with open("helpers/test_information.yaml", "r") as stream:
        try:
            test_information = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return test_information


def read_testing_descriptors():
    '''
    Read testing descriptors from testing_descriptor_nods.yaml
    '''
    with open("helpers/testing-descriptor_nods.yaml", "r") as stream:
        try:
            testing_descriptor_nods = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
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