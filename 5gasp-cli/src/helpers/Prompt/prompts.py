# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-04 16:39:57
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-04 16:44:52

# OS 
import sys

class Prompts:

    def continue_without_nsd(self):
        while True:
            opt = input("\nAre you sure you want to continue without providing a NSD? [y/n]: ")

            if opt not in ["y", "n"]:
                print(f"\nERROR! The value must be \'y\' or \'n\'")
                continue
            else:
                return opt
            

    def info_about_test(self, i: int):
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
        while True:
            cp = input("\nWhich connection point do you want to inject on the parameter? ")

            is_valid = self.is_digit_and_in_range(cp, i)

            if is_valid:
                continue
            else: 
                return cp
    
    
    def value_to_inject_on_connection_point(self, i: int):
        while True:
            value = input("\nWhich value do you want to inject on the connection point? ")

            is_valid = self.is_digit_and_in_range(value, i)

            if is_valid:
                continue
            else: 
                return value
            
    
    def is_digit_and_in_range(self, value: str, i):
        '''
        Verify if given value is digit and in range(1, i + 1)

        Parameters
        ----------
        value : str
            Value to be verified
        i : int
            Maximum range
        
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