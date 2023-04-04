# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-01 16:31:36
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-04-04 01:19:51

# Python
from typing import List, Optional

# Typer
import typer

from TestingDescriptorGenerator.descriptor_generator import TestingDescriptorGenerator

app = typer.Typer(pretty_exceptions_show_locals = False)
state = {"verbose": False}


@app.command()
def create_tests(
    config_file: str = typer.Option(None, 
                                        help = "Name of the config file \
                                        containing the desired test' names"),
    output_filename: str = typer.Option("testing-descriptor.yaml", 
                                        help = "Output filename"),
    clear_executions: bool = typer.Option(False, 
                                        help = "Clear executions"),
    infer_tags_from_nsd: Optional[List[str]] = typer.Option(None)
    ):
    descriptor_generator = TestingDescriptorGenerator(state)
    descriptor_generator.create_testing_descriptor(
                            config_file, 
                            output_filename, 
                            clear_executions, 
                            infer_tags_from_nsd
                        )


@app.command()
def list_available_tests():
    '''
    List available tests to developer
    '''
    descriptor_generator = TestingDescriptorGenerator(state)
    descriptor_generator.list_available_tests()
     

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
