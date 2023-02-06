import typer
import yaml
from pprint import pprint

app = typer.Typer()
state = {"verbose": False}


@app.command()
def create_tests(
    test_description: str, 
    config_file: str = typer.Option(...)
    ):
    '''
    Create tests descriptor from a given config.yaml containing the intended tests
    '''

    if state["verbose"]: print("Reading configuration file...")

    with open(config_file, "r") as stream:
        try:
            content = yaml.safe_load(stream) # dict
        except yaml.YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Configuration file read!")

    intended_tests = content['tests']   

    tests_info = read_tests_info(intended_tests)

    tests = read_testing_descriptors()

    tests['test_phases']['setup']['testcases'] = [test for test in tests_info]

    if state["verbose"]: print("Creating tests file...")

    with open("testing-descriptor.yaml", "w") as file:
        try:
            t = yaml.dump(
                tests, 
                file, 
                sort_keys = False, 
                default_flow_style = False,)
        except yaml.YAMLError as exc:
            print(exc)

    if state["verbose"]: print("Tests file created!")
    

def read_tests_info(tests: str):
    '''
    Read tests information from test_information.yaml
    '''

    with open("helpers/test_information.yaml", "r") as stream:
        try:
            test_information = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    tests_info = [test_information['tests']['testbed_itav'][test] for test in tests]

    return tests_info


def read_testing_descriptors():
    '''
    Read testing descriptors from testing_descriptor_nods.yaml
    '''

    with open("helpers/testing-descriptor_nods.yaml", "r") as stream:
        try:
            testing_descriptor_nods = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    return testing_descriptor_nods
        

@app.callback()
def main(verbose: bool = False):
    """
    5GASP CLI
    """
    if verbose:
        #print("Will write verbose output")
        state["verbose"] = True


if __name__ == "__main__":
    app()