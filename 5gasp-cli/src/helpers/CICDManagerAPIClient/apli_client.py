# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-04-06 14:55:17
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-06 16:13:06

import requests

class CICDManagerAPIClient:
    def __init__(self):
        self.base_url = "https://ci-cd-service.5gasp.eu/manager"
        
    def get_all_testbeds(self):
        '''
        Retrieves all testbeds from the CI/CD Manager API.

        Returns
        -------
            List of all testbeds.
        '''
        path = "testbeds/all"
        url = f"{self.base_url}/{path}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            return None
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Unknown Error: {err}")
            return None
        else:
            return response.json()['data']['testbeds']
        
    def get_all_tests(self):
        '''
        Retrieves all tests from the CI/CD Manager API.

        Returns
        -------
            List of all tests.
        '''
        path = "tests/all"
        url = f"{self.base_url}/{path}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            return None
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Unknown Error: {err}")
            return None
        else:
            return response.json()['data']['tests']
        
    
    def get_tests_per_testbed(self, testbed: str):
        '''
        Retrieves all testbeds from the CI/CD Manager API.

        Parameters
        ----------
        testbed : str
            Testbed

        Returns
        -------
            List of all testbeds.
        '''
        path = "tests/all"
        url = f"{self.base_url}/{path}"
        params = {"testbed": testbed}
        
        try:
            response = requests.get(url, params = params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            return None
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
            return None
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            return None
        except requests.exceptions.RequestException as err:
            print(f"Unknown Error: {err}")
            return None
        else:
            return response.json()['data']['tests']
