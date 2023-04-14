# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-04 01:14:05
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-14 18:26:08

# OS
import sys

#ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

yaml = YAML()
yaml.default_flow_style = False

class FileReader:
    def __init__(self):
        self.RESOURCES_DIR = "../../resources/"

    def read_intended_tests(self, config_file):
        '''
        Read the intended tests from a config file

        Parameters
        ----------
        config_file : str
            Path to the configuration file

        Returns
        -------
        test_information : dict
            Dictionary containing tests information from test_information.yaml.
        '''
        try:
            with open(config_file, "r") as stream:
                try:
                    intended_tests = yaml.load(stream) # dict
                except YAMLError as exc:
                    print(exc)
        except FileNotFoundError as e:
            print(f"Error! File {config_file} not found!")
            return sys.exit(0)
        
        return intended_tests
        
    def read_tests_info(self):
        '''
        Read tests information from test_information.yaml

        Returns
        -------
        test_information : dict
            Dictionary containing tests information from test_information.yaml.
        '''
        try:
            with open(self.RESOURCES_DIR + "test_information.yaml", "r") as stream:
                try:
                    test_information = yaml.load(stream)
                except YAMLError as exc:
                    print(exc)
        except FileNotFoundError as e:
            print(f"Error! File test_information.yaml not found!")
            return sys.exit(0)

        return test_information


    def read_testing_descriptors(self):
        '''
        Read testing descriptors from testing_descriptor_nods.yaml
        
        Returns
        -------
        testing_descriptor_nods : dict
            Dictionary containing the testing descriptors.
        '''
        try:
            with open(self.RESOURCES_DIR + "testing-descriptor_nods.yaml", "r") as stream:
                try:
                    testing_descriptor_nods = yaml.load(stream)
                except YAMLError as exc:
                    print(exc)
        except FileNotFoundError as e:
            print(f"Error! File testing-descriptor_nods.yaml not found!")
            return sys.exit(0)

        return testing_descriptor_nods

    def read_connection_point_values(self):
        '''
        Read connection point values from connection_point_values.yaml
        
        Returns
        -------
        connection_point_values : dict
            Dictionary containing the connection point values.
        '''
        try:
            with open(self.RESOURCES_DIR + "connection_point_values.yaml", "r") as stream:
                try:
                    connection_point_values = yaml.load(stream)
                except YAMLError as exc:
                    print(exc)
        except FileNotFoundError as e:
            print(f"Error! File connection_point_values.yaml not found!")
            return sys.exit(0)

        return connection_point_values['values']
    

    def read_inputs(self):
        '''
        Read inputs for prompts from inputs.yaml
        
        Returns
        -------
        inputs : dict
            Dictionary containing the inputs' strings.
        '''
        try:
            with open("helpers/Prompt/inputs.yaml", "r") as inputs_file:
                inputs = yaml.load(inputs_file)
        except FileNotFoundError as e:
            print(e)
            return sys.exit(0)
        
        return inputs