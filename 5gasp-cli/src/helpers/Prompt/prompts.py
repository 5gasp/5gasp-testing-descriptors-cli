# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-04 16:39:57
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-10 16:20:40

# OS 
import sys

class Prompts:

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
                print(f"\nERROR! The value must be \'y\' or \'n\'")
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
            opt = input("\nDo you wish to see some information about a test? [y/n]: ")

            if opt not in ["y", "n"]:
                print(f"\nERROR! The value must be \'y\' or \'n\'")
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
            cp = input("\nWhich connection point do you want to inject on the parameter? ")

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
            value = input("\nWhich value do you want to inject on the connection point? ")

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
            opt = input("\nDo you want to inject a connection point (1), or add the value manually (2)? ")

            if opt not in ["1", "2"]:
                print(f"\nERROR! The value must be \'1\' or \'2\'")
                continue
            else:
                if opt == "1":
                    return 1
                else:
                    value = input(f"Enter the value to manually inject: ")

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
            value = input("\nChoose the preferred test bed: ")

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
            opt = self.yes_and_no_prompt("Do you wish to manually set a parameter?")

            if opt == 0:
                break
            
            while True:
                parameter = input("\nChoose the parameter: ")

                is_valid = self.is_digit_and_in_range(parameter, i)

                if is_valid == 0:
                    value = input("Enter the value to inject on the parameter: ")
                    testcase.add_parameter(
                        {'key': test['test_variables'][int(parameter) - 1]['variable_name'],
                        'value': value}
                    )
                    break

        return testcase


            