# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-04 16:39:57
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-20 17:23:35

# OS 
import os
import sys
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.console import Group

# ruamel.yaml
from ruamel.yaml import YAML

from ..FileReader.reader import FileReader

yaml = YAML()


def tests_per_testbed_prompt():
    console = Console()    
    group = Group(
    Align.center("[b]In 5GASP, each testbed has its own specific tests.[/b]"),
    Align.center(" "),
    Align.center("Thus, we don't provide and overall view of the tests we " +
                 "have in our ecosystem, but rather a testbed-level view " +
                 "of the tests."),
    Align.center("[b]This way, you must first choose a testbed on where " +
                 "yourNetApp shall be deployed, valdiated and certified.[/b]"),
    Align.center("Only after choosing the testbed you may list the tests " +
                 "available in that facility."),
    )
    console.print(
        Align.center(
            Panel(
                renderable=group,
                title="5GASP's Tests",
                expand=True
            )
        )
    )

def tests_testbeds_list_prompt():
    console = Console()
    console.print(
        Align.center(
            "\n[b]Testbeds Available for Network Applications Testing:[/b]\n"
        )
    )
    
def display_tests_for_testbed(testbed):
    console = Console()
    console.print(
        "\n[b]" +
        f"The Testbed '{testbed}' provides the following tests:".title() +
        "[/b]\n"
    )
    
def do_you_wish_to_see_test_information_prompt():
    console = Console()
    console.print(
        "\n[b]You can see additional information about each of the tests.\n"+
        "If you don't want to do so, just type 'exit'.[b]"
    )
    
    
class Prompts:

    def __init__(self):
        reader = FileReader()
        self.inputs = reader.read_inputs()

    def yes_and_no_prompt(self, prompt: str):
        '''
        Prompt

        Parameters
        ----------
        prompt: str
            Text to be prompted

        Returns
        -------
        opt : bool
            1 if yes else 0
        '''
        while True:
            opt = input(f"\n{prompt} [y/n]: ")

            if opt not in ["y", "n"]:
                print("\n" + self.inputs['error_y_or_n'])
                continue
            else:
                return 0 if opt == "n" else 1
            

    def info_about_test(self, i: int):
        '''
        Prompt

        Parameters
        ----------
        i: int
            Range of values to accept

        Returns
        -------
        test_number : int
            Number of the test
        '''
        while True:
            opt = input("\n" + self.inputs['info_about_test'])

            if opt not in ["y", "n"]:
                print("\n" + self.inputs['error_y_or_n'])
                continue
            else:
                if opt == "n":
                    sys.exit(0)
                else:
                    while True:
                        test_number = input(f"Choose the test: [1 - {i}]: ")
                        
                        is_valid = self.is_digit_and_in_range(test_number, i)

                        if is_valid:
                            continue
                        else: 
                            break
                return test_number
            

    def connection_point_to_inject(self, i: int):
        '''
        Prompt

        Parameters
        ----------
        i: int
            Range of values to accept

        Returns
        -------
        cp : int
            Connection point on which to inject a value
        '''
        while True:
            cp = input("\n" + self.inputs['cp_to_inject'])

            is_valid = self.is_digit_and_in_range(cp, i)

            if is_valid:
                continue
            else: 
                return cp
    
    
    def value_to_inject_on_connection_point(self, i: int):
        '''
        Prompt

        Parameters
        ----------
        i: int
            Range of values to accept

        Returns
        -------
        value : int
            Value to inject on the connection point
        '''
        while True:
            value = input("\n" + self.inputs['cp_value'])

            is_valid = self.is_digit_and_in_range(value, i)

            if is_valid:
                continue
            else: 
                return value
            
    def connection_point_or_manually(self):
        '''
        Prompt

        Parameters
        ----------
        i: int
            Range of values to accept

        Returns
        -------
        value : str
            1 if connection point, the value to inject if manually
        '''
        while True:
            opt = input("\n" + self.inputs['inject_cp_or_manually'])

            if opt not in ["1", "2"]:
                print("\n" + self.inputs['error_1_or_2'])
                continue
            else:
                if opt == "1":
                    return 1
                else:
                    value = input(self.inputs['cp_value'])

                return value
            
    
    def is_digit_and_in_range(self, value: str, i):
        '''
        Verify if given value is digit and in range(1, i + 1)

        Parameters
        ----------
        value : str
            Value to be verified
        i : int
            Range of values to accept
        
        Returns
        -------
        1 if not valid, 0 if valid
        '''
        if not value.isdigit():
            print(f"\nERROR! The value must be between 1 - {i}")
            return 1
        else:
            if int(value) not in range(1, i + 1):
                print(f"\nERROR! The value must be between 1 - {i}")
                return 1
            else:
                return 0
            
    
    def choose_testbed(self, i: int):
        '''
        Prompt

        Parameters
        ----------
        i: int
            Range of values to accept

        Returns
        -------
        value : int
            Testbed
        '''
        while True:
            value = input("\n" + self.inputs['preferred_testbed'])

            is_valid = self.is_digit_and_in_range(value, i)

            if not is_valid:
                return int(value)

    
    def configure_testcase_parameter(self, test, testcase, i):
        '''
        Prompt

        Parameters
        ----------
        test: dict
            Dictionary containing testing descriptors.
        testcase: Testcase
            Testcase to inject values
        i: int
            Range of values to accept

        Returns
        -------
        value : int
            Testcase
        '''
        while True:
            opt = self.yes_and_no_prompt(self.inputs['manually_set_param'])

            if opt == 0:
                break
            
            while True:
                parameter = input("\n" + self.inputs['choose_param'])

                is_valid = self.is_digit_and_in_range(parameter, i)

                if is_valid == 0:
                    value = input(self.inputs['value_to_inject'])
                    testcase.add_parameter(
                        {'key': test['test_variables'][int(parameter) - 1]['variable_name'],
                        'value': value}
                    )
                    break

        return testcase

    def choose_until_valid_value(self, prompt: str, valid_values: list,
                                 show_valid_values: bool = False):

        if show_valid_values:
            prompt = f"{prompt} [{', '.join(valid_values)}]: "

        while True:
            value = input("\n" + prompt)

            if value in valid_values:
                return value

            print("Invalid value")
