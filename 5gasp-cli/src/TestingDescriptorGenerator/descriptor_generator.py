# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-03 23:41:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-05 15:02:46

# OS
import sys
import os

# Python
from typing import List, Optional

# ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

# Modules
from Testcase.testcase import Testcase
from Execution.execution import Execution
from Parser.parser import InjectedTagsParser
from helpers.FileReader.reader import FileReader
from helpers.Prompt.prompts import Prompts

yaml = YAML()
yaml.default_flow_style = False

class TestingDescriptorGenerator:
    def __init__(self, state):
        self.state = state
        self.file_reader = FileReader()
        self.prompts = Prompts()

    def create_testing_descriptor(
    self,
    config_file: str,
    output_filename: str,
    clear_executions: bool,
    infer_tags_from_nsd: Optional[List[str]]
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
        network_service_descriptor : list[str] (optional)
            Network Service Descriptor to be used to infer tags 
            (this option can be called multiple times)
        infer_tags_from_nsd : list[str] (optional)
            Network Service Descriptor to be used to infer tags 
            (this option can be called multiple times)
        
        Returns
        -------
        None
        '''

        infering = False
        connection_points = {}
        connection_point_values = {}
        
        if infer_tags_from_nsd:
            infering = True
            descriptors = [os.path.basename(path) for path in infer_tags_from_nsd]
            connection_points = self.infer_tags(infer_tags_from_nsd)
            connection_point_values = self.file_reader.read_connection_point_values()

        else:
            opt = self.prompts.continue_without_nsd()

            if opt == "n":
                infering = True
                
                d = input("\nEnter the location of the descriptors, separated by a \",\": ")
                descriptors = [os.path.basename(path) for path in d.split(",")]

                connection_points = self.infer_tags(d.split(","))
                connection_point_values = self.file_reader.read_connection_point_values()

        if infering and self.state["verbose"]: 
                print(f"\nInfering tags from the following descriptors: {descriptors}")

        if self.state["verbose"]: 
            print("\nReading configuration file...")

        try:
            with open(config_file, "r") as stream:
                try:
                    intended_tests = yaml.load(stream) # dict
                except YAMLError as exc:
                    print(exc)
        except FileNotFoundError as e:
            print(f"Error! File {config_file} not found!")
            return sys.exit(0)

        if self.state["verbose"]: 
            print("Configuration file read!")

        # testing descriptors from testing-descriptor_nods.yaml
        tests = self.file_reader.read_testing_descriptors()

        # tests info from test_information.yaml
        tests_info = self.file_reader.read_tests_info()

        cleared_tests = self.reset_sections(tests, clear_executions)

        # add intended tests to testcases
        descriptor = self.add_tests_to_testcases(
                        cleared_tests, 
                        tests_info, 
                        intended_tests, 
                        connection_points,
                        connection_point_values
                    )

        if self.state["verbose"]: 
            print("Creating the descriptor...")

        # save data to the descriptor
        with open("../../" + output_filename, "w") as file:
            try:
                yaml.dump(descriptor, file)
            except YAMLError as exc:
                print(exc)

        if self.state["verbose"]:
            print("\nDescriptor generated!")
            

    def list_available_tests(self):
        '''
        List available tests to developer
        '''
        tests = self.file_reader.read_tests_info()['tests']['testbed_itav']

        tests_list = [test for test in tests]
        
        print("\nThe following tests can be injected on the testing descriptor:\n")
        
        for i, test in enumerate(tests, 1):
            print(f"{i} - {test} - {tests[test]['description']}")
            
        test_number = self.prompts.info_about_test(i)
            
        test = tests_list[int(test_number) - 1]

        print(f"The chosen test was: {test}")
        print("\nTest information:")
        print(f"\nName: {tests[test]['name']}")
        print(f"Description: \"{tests[test]['description']}\"")
        print(f"Parameters/Variables:")

        for parameter in tests[test]['test_variables']:
            print(f"\n\tVariable name: {parameter['variable_name']}")
            print(f"\tDescription: {parameter['description']}")
        
        self.list_available_tests()  


    def reset_sections(self, tests: dict(), clear_executions: bool):
        '''
        Reset user-given sections to later be filled by the developer

        Parameters
        ----------
        tests : dict
            Dictionary containing testing descriptors.
        clear_executions : bool
            Boolean for whether to clear existing executions.
        
        Returns
        -------
        tests: dict
            Updated testing descriptors.
        '''

        tests['test_phases']['setup']['testcases'].clear()
        
        if clear_executions:
        
            tests['test_phases']['execution'].clear()

            execution = Execution(1, "", [1])
            
            execution.create_execution()

            tests['test_phases']['execution'] = [
                    {"batch_id": 1,"executions": [execution.execution]}
            ]

        return tests


    def add_tests_to_testcases(
            self,
            tests: dict(), 
            tests_info: dict(), 
            intended_tests: dict(),
            connection_points = {},
            connection_point_values = {}
            ):
        '''
        Add developer given tests to the testcases

        Parameters
        ----------
        tests : dict
            Dictionary containing testing descriptors.
        tests_info : dict
            Dictionary containing tests info.
        intended_tests : bool
            Dictionary containing tests to be added.
        connection_points : dict
            Connection points infered from NSD(s)
        connection_point_values : dict
            Possible values for the connection points.
        
        Returns
        -------
        tests : dict
            Updated testing descriptors.
        '''

        # existing tests
        test_types = tests_info['tests']['testbed_itav']

        intended_test_types = [type for type in test_types 
                                if type in intended_tests['tests']]
        
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
                tag = ""
                
                if connection_points:
                    
                    if "injected_by_nods" in variable \
                        and variable['injected_by_nods'] \
                        and variable['injected_artifact_type'] == "connection_point":
                        print("True")

                        print(f"\nThe {variable['variable_name']} parameter must have a connection point injected")

                        print("\nThe following connection points were infered from the given NSD(s):")

                        for i, connection_point in enumerate(connection_points, 1):
                            print(f"{i} - {connection_point}")

                        cp = self.prompts.connection_point_to_inject(i)

                        print("\nThe following values can be injected into the connection point:")

                        for i, connection_point_value in enumerate(connection_point_values, 1):
                            print(f"{i} - {connection_point_value}")

                        value = self.prompts.value_to_inject_on_connection_point(i)
                            
                        tag = connection_points[int(cp) - 1][:-2] + "|" \
                                + connection_point_values[int(value) - 1] + "}}"
                    

                testcase.add_parameter({'key': variable['variable_name'], 'value': tag})

            # add testcase to tests
            tests['test_phases']['setup']['testcases'].append(testcase.testcase)

        return tests


    def infer_tags(self, network_service_descriptor: list()):
        '''
        Infer tags from given NSD(s)

        Parameters
        ----------
        network_service_descriptor : list[str]
            List with NSDs to be used to infer tags 

        Returns
        -------
        tags : dict
            Connection points infered.
        '''
        for descriptor in network_service_descriptor:
            parser = InjectedTagsParser(descriptor)
            parser.parse_descriptor()

        return parser.interfaces
