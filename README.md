# safescope
[![Build Status](https://travis-ci.org/havakv/safescope.svg?branch=master)](https://travis-ci.org/havakv/safescope)
[![PyPI](https://img.shields.io/pypi/v/safescope.svg)](https://pypi.org/project/safescope/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/safescope.svg)
[![Downloads](https://pepy.tech/badge/safescope)](https://pepy.tech/project/safescope)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://github.com/havakv/safescope/blob/master/LICENSE)

**safescope** is a small python package useful for development in jupyter notebooks.
The goal is to prevent functions from using global variables and instead raise a `NameError`.
This is achieved by  mimicking a module, and define all functions in that module (named `side_scope`).

## Example

The main part of **safescope** is the decorator `@safescope`. This mimics writing the function in a file `side_scope.py` and importing this function to the notebook. Hence, functions decorated with `@safescope` will not have access to variables declared in the notebook environment.

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

By using `Imports`, the imports are added to both the main scope and the `side_scope`, making them available for the functions decorated with `@safescope`.
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

**safescope** can either be installed from pypi with pip/pip3:
```bash
pip install safescope
```
or from github with:
```bash
pip install git+git://github.com/havakv/safescope.git
```
or from source by cloning the repo:
```bash
git clone https://github.com/havakv/safescope.git
cd safescope
python setup.py install
```

