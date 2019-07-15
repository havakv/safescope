# safescope
[![Build Status](https://travis-ci.org/havakv/safescope.svg?branch=master)](https://travis-ci.org/havakv/safescope)
![PyPI](https://img.shields.io/pypi/v/safescope.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/safescope.svg)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://github.com/havakv/safescope/blob/master/LICENSE)

**safescope** is a small python package useful for development in jupyter notebooks.
The goal is to prevent function from using global variables, and in stead raise a `NameError`.
This is achieved by  mimicking a module, and define all functions in that module (named `side_scope`).

## Example

The main part of **safescope** is the decorator `@safescope`. This mimics actually writing the function in a file `side_scope.py`, and importing the function to the notebook. Hence, functions decorated with `@safescope` will not have access to variables declared in the notebook.

In the example below, only `foo(1)`  will execute, as `bar(1)` returns a `NameError`.
```python
from safescope import safescope

x = 9

def foo(y):
    return x + y

@safescope
def bar(y):
    return x + y

foo(1) # Returns  10
bar(1) # Raise "NameError: name 'x' is not defined"
```

By using `Imports`, the import are added to both the main scope and the `side_scope`, and can therefore be used by functions decorated with `@safescope`.
```python
from safescope import safescope, Imports

with Imports():
    import numpy as np

@safescope
def arange(n):
    return np.arange(n)

arange(4) # Returns array([0, 1, 2, 3])
```

## Installation

Next, **safescope** can be installed from pypi:
```bash
pip3 install -U safescope
```
or from github with pip:
```bash
pip3 install git+git://github.com/havakv/safescope.git
```
or by cloning the repo:
```bash
git clone https://github.com/havakv/safescope.git
cd safescope
python setup.py install
```

