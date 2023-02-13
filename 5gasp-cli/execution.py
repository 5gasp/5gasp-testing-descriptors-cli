# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-13 16:46:59
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-13 17:08:48

class Execution:
    '''
    Class representing Execution
    '''
    global execution
    
    def __init__(self, id: int, name: str, testcase_ids: list()):
        self.id = id
        self.name = name
        self.testcase_ids = testcase_ids
        self._execution = dict()
    
    def create_execution(self):
        '''
        Create a new execution
        '''
        self.execution = {
                'execution_id': self.id,
                'name': self.name,
                'testcase_ids': self.testcase_ids,
            }

    def add_testcase_id(self, testcase_id = int):
        '''
        Add a parameter to the testcase
        '''
        self.execution['testcase_ids'].append(testcase_id)

    @property # getter
    def execution(self):
        return self._execution