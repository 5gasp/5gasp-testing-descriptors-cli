# 5GASP CLI

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

Here are some examples:

1. Create a testing descriptor from a config file:

```python
python3 main.py create-tests --config-file "../../resources/config.yaml"
```

2. Infer tags from a NSD:

```python
python3 main.py create-tests --config-file "../../resources/config.yaml" --infer-tags-from-nsd "../../resources/hackfest_multivdu_nsd.yaml"
```

3. List all available tests:

```python
python3 main.py list-available-tests
```

## Documentation

For the documentation, the [Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator was used.

To create a new page, create a markdown file inside the */5gasp-cli/docs/* directory.

To generate the documentation for that file, inside the same directory, insert the file's name on the *index.rst* file (without the *.md* extension).

To build the documentation, run:

    1. make clean
    2. make html

Then, inside the same directory, open the **index.html** file:

    open _build/html/index.html
