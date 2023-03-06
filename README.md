# 5GASP CLI

## How to run

### Requirements

Before installing the requirements, the usage of a virtual environment is recommended.
To install the requirements, run:

    pip install -r requirements.txt

### Run

You can find the code inside the */5gasp-cli/docs/src/* directory.
To list all CLI commands, run:

    python3 main.py --help

To list all parameters of a command, run:

    python3 main.py COMMAND --help

## Documentation

For the documentation, the (Sphinx)[https://www.sphinx-doc.org/en/master/] documentation generator was used.

To create a new page, create a markdown file inside the */5gasp-cli/docs/* directory.

To generate the documentation for that file, inside the same directory, insert the file's name on the *index.rst* file (without the *.md* extension).

To build the documentation, run:

    1. make clean
    2. make html

Then, inside the same directory, open the **index.html** file:

    open _build/html/index.html