# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-18 15:26:20
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-20 15:53:20

# OS
import sys

# Python
from pprint import pprint

#ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError

yaml = YAML(typ = "safe") # safe mode - loads a document without resolving unknown tags

class InjectedTagsParser:
    """
    Injected Tags Parser Class
    """
    def __init__(self, filename: str):
        """
        Constructor
        """
        self.filename = filename
        self._interfaces = []

    def parse_descriptor(self):
        '''
        Retrieves all the tags from the given descriptor
        '''
        try:
            with open(self.filename, "r") as file:
                descriptor = yaml.load(file)
        except FileNotFoundError as e:
            print(f"Error! File {self.filename} not found!")
            return sys.exit(0)

        for network_service in descriptor['nsd']['nsd']:
            ns_id = network_service['id']

            # get only the default df
            df = [df for df in network_service['df'] if df['id'] == 'default-df']

            for vnf in df[0]['vnf-profile']:
                vnf_id = vnf['vnfd-id']
                
                for constituent in vnf['virtual-link-connectivity']:
                    interface_id = constituent['constituent-cpd-id'][0]\
                                                ['constituent-cpd-id']
                                            
                    self.interfaces.append(
                        "{{" + f"{ns_id}|{vnf_id}|{interface_id}" + "}}"
                    )

    @property # getter
    def interfaces(self):
        '''
        Get interfaces
        '''
        return self._interfaces