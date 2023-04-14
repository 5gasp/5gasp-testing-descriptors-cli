# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-03 23:41:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-14 18:28:36

# OS
import os
from re import sub

# Python
from typing import List, Optional

# ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

# Modules
from modules.Testcase.testcase import Testcase
from modules.Execution.execution import Execution

# Helpers
from helpers.DescriptorParser.parser import InjectedTagsParser
from helpers.FileReader.reader import FileReader
from helpers.Prompt.prompts import Prompts
from helpers.CICDManagerAPIClient.apli_client import CICDManagerAPIClient

yaml = YAML()
yaml.default_flow_style = False

class TestingDescriptorGenerator:
    def __init__(self, state):
        self.state = state
        self.file_reader = FileReader()
        self.prompts = Prompts()
        self.api_client = CICDManagerAPIClient()
        self.inputs = self.file_reader.read_inputs()

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
        connection_points = []
        connection_point_values = {}
        
        if infer_tags_from_nsd:
            infering = True
            descriptors = [os.path.basename(path) for path in infer_tags_from_nsd]
            connection_points = self.infer_tags(infer_tags_from_nsd)
            connection_point_values = self.file_reader.read_connection_point_values()

        else:
            opt = self.prompts.yes_and_no_prompt(
                    "\n" + self.inputs['continue_without_nsd']
                )

            if opt == 0:
                infering = True
                
                d = input(self.inputs['descriptors_location'])
                descriptors = [os.path.basename(path) for path in d.split(",")]

                connection_points = self.infer_tags(d.split(","))
                connection_point_values = self.file_reader.read_connection_point_values()

        intended_tests = self.file_reader.read_intended_tests(config_file)

        # user's input - network application's name
        netapp_name = input(self.inputs['network_app_name'])
        
        # user's input - test bed
        testbeds = self.api_client.get_all_testbeds()
        print("\n")
        
        for i, testbed in enumerate(testbeds, 1):
            print(f"Available testbeds: {testbed['name']} ({i})")
            
        testbed = self.prompts.choose_testbed(i)
        testbed_name = testbeds[testbed - 1]['id']

        # user's input - descriptor's description 
        description = input(
            "\n" + self.inputs['descriptor_description']
        )

        # testing descriptor from testing-descriptor_nods.yaml
        tests = self.file_reader.read_testing_descriptors()

        # tests info from test_information.yaml
        tests_info = self.file_reader.read_tests_info()

        # descriptor with cleared test cases
        cleared_tests = self.reset_sections(tests, clear_executions)
        
        netapp_name = '_'.join(
                            sub(
                                '([A-Z][a-z]+)', 
                                r' \1', 
                                sub(
                                    '([A-Z]+)', 
                                    r' \1', 
                                    netapp_name.replace('-', ' ')
                                )
                            ).split()).lower()

        cleared_tests['test_info']['netapp_id'] = netapp_name
        cleared_tests['test_info']['testbed_id'] = testbed_name
        cleared_tests['test_info']['description'] = description

        configure_testcase = self.prompts.yes_and_no_prompt(
                                self.inputs['configure_a_testcase']
                            )
        
        if configure_testcase:
            # add intended tests to testcases
            descriptor = self.add_tests_to_testcases(
                            cleared_tests, 
                            tests_info, 
                            intended_tests, 
                            connection_points,
                            connection_point_values
                        )
        else:
            descriptor = cleared_tests

        # save data to the descriptor
        generated_descriptor_path = "../../generated_descriptor/"
        with open(generated_descriptor_path + output_filename, "w") as file:
            try:
                yaml.dump(descriptor, file)
            except YAMLError as exc:
                print(exc)
            

    def list_available_tests(self):
        '''
        List available tests to developer
        '''
        tests = self.file_reader.read_tests_info()['tests']['testbed_itav']

        tests_list = [test for test in tests]
        
        print("\nThe following tests can be injected on the testing descriptor:\n")
        
        for i, test in enumerate(tests, 1):
            print(f"{i} - {test}")
            
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

        del tests['test_info']['network_service_id']

        # clear testcases
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
        connection_points : list
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

            print(f"\n\tTest: {test['name']}")
            print(f"\n\tType: {test['test_type']}")
            print(f"\n\tDescription: {test['description']}")
            print("\n\tParameters: " 
                  + ", ".join(
                    [variable['variable_name'] \
                    for variable in test['test_variables']]
                    )
                )
            opt = self.prompts.yes_and_no_prompt(
                "\n" + self.inputs['configure_this_testcase']
            )

            if opt == 0:
                continue

            testcase = Testcase(
                            id = i,
                            type = test['test_type'],
                            name = test['name'],
                            description = test['description'],
                        )

            testcase.create_testcase()

            # add parameters to testcase
            t = self.add_parameters_to_testcase(
                                                    test,
                                                    connection_points, 
                                                    connection_point_values, 
                                                    testcase
                                                )
            # add testcase to tests
            tests['test_phases']['setup']['testcases'].append(t.testcase)

        return tests
    

    def add_parameters_to_testcase(
            self, 
            test,
            connection_points, 
            connection_point_values, 
            testcase
        ):
        '''
        Add parameter to the testcase

        Parameters
        ----------
        test: dict
            Dictionary containing testing descriptors.
        connection_points : list
            Connection points infered from NSD(s).
        connection_point_values : dict
            Possible values for the connection points.
        testcase: dict
            Testcase 
        
        Returns
        -------
        testcase : dict
            Updated testcase.
        '''
        for variable in test['test_variables']:
            tag = ""

            if connection_points \
                and "injected_by_nods" in variable \
                and variable['injected_by_nods'] \
                and variable['injected_artifact_type'] == "connection_point":

                print(f"\nThe {variable['variable_name']} parameter must have a connection point injected")
                print("\nThe following connection points were infered from the given NSD(s):")

                for i, connection_point in enumerate(connection_points, 1):
                    print(f"{i} - {connection_point}")

                opt = self.prompts.connection_point_or_manually()
                
                if opt == 1:
                    cp = self.prompts.connection_point_to_inject(i)

                    print("\nThe following values can be injected into the connection point:")

                    for i, connection_point_value in enumerate(connection_point_values, 1):
                        print(f"{i} - {connection_point_value}")

                    value = self.prompts.value_to_inject_on_connection_point(i)
                        
                    tag = connection_points[int(cp) - 1][:-2] + "|" \
                            + connection_point_values[int(value) - 1] + "}}"
                else:
                    tag = opt
            
            testcase.add_parameter({'key': variable['variable_name'], 'value': tag})

        i = 0
        print("\nThe testcase has also the following parameters:\n")
        for variable in test['test_variables']:
            if not "injected_by_nods" in variable or \
                ("injected_by_nods" in variable and not variable['injected_by_nods']):
                    i += 1
                    print(f"{i} - {variable['variable_name']}")

        testcase = self.prompts.configure_testcase_parameter(test, testcase, i)

        return testcase


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
