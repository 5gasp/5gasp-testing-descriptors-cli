# 5GASP Testing Descriptors CLI

The 5GASP Testing Descriptors CLI is a command-line interface designed to create 5GASP Testing Descriptors for Network Applications.

## Provided Capabilities

* List the 5GASP Testbeds
* List the Available Tests
* Create a Testing Descriptor

## How to run

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

## Documentation

For the documentation, the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator was used.

To create a new page, create a markdown file inside the */5gasp-cli/docs/* directory.

To generate the documentation for that file, inside the same directory, insert the file's name on the *index.rst* file (without the *.md* extension).

To build the documentation, run:

    1. make clean
    2. make html

Then, inside the same directory, open the **index.html** file:

    open _build/html/index.html

## Authors
* **Eduardo Santos**: [eduardosantoshf](https://github.com/eduardosantoshf)
* **Rafael Direito**: [rafael-direito](https://github.com/rafael-direito)
