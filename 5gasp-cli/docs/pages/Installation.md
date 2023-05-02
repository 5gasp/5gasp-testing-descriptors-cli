# How to run

### Requirements

Before installing the requirements, the usage of a virtual environment is recommended.
To install the requirements, run:

    pip install -r requirements.txt

### Run

You can find the code inside the */5gasp-cli/src/* directory.
To list all CLI commands, run:

    python3 main.py --help

To list all parameters of a command, run:

    python3 main.py COMMAND --help

### CLI Commands

#### List all tests from a test bed

```python
python3 main.py list-testbeds
```

#### List all available tests

```python
python3 main.py list-available-tests
```

#### Generate a testing descriptor:

```python
python3 main.py create-testing-descriptor
```

This command has the following options:

* One or more NSDs (Network Service Descriptors) can be passed to infer connection point tags from, using the following command:

```python
python3 main.py create-testing-descriptor --infer-tags-from-nsd <nsd_location>
```

* The path of the generated descriptor can be passed using:

```python
python3 main.py create-testing-descriptor --output-filepath <path_to_file>
```

> **_NOTE:_** Both options can be used simultaneously