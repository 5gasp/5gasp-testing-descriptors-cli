# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-10 14:53:17
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-14 17:16:18

class Testcase:
    '''
    Class representing Testcase
    '''
    global testcase

    def __init__(self, id: int, type: str, name: str, description: str, 
                    scope: str = None):
        self.id = id
        self.type = type
        self.scope = scope if scope else " "
        self.name = name
        self.description = description
        self.parameters = []
        self._testcase = {}
    
    def create_testcase(self):
        '''
        Create a new testcase
        '''
        self.testcase = {
                'testcase_id': self.id,
                'type': self.type,
                'scope': self.scope,
                'name': self.name,
                'description': self.description,
                'parameters': self.parameters,
            }

    def add_parameter(self, parameter = {}):
        '''
        Add a parameter to the testcase
        '''
        self.testcase['parameters'].append(parameter)

    @property # getter
    def testcase(self):
        '''
        Get testcase
        '''
        return self._testcase
        