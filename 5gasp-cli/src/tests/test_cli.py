# -*- coding: utf-8 -*-
# @Author: Eduardo Santos
# @Date:   2023-02-10 17:15:58
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-10 18:19:31

from typer.testing import CliRunner

from main import app

runner = CliRunner()

def test_cli():
    '''
    Test CLI
    '''
    result = runner.invoke(app, ["--verbose", 
                                "create-tests", 
                                "example of a test", 
                                "--config-file", 
                                "config.yaml",
                                "--output-filename",
                                "test_output.yaml"]
                            )
    
    assert result.exit_code == 0
    assert "Tests file created!" in result.stdout