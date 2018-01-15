=========
safescope
=========


.. image:: https://img.shields.io/pypi/v/safescope.svg
        :target: https://pypi.python.org/pypi/safescope

.. image:: https://img.shields.io/travis/havakv/safescope.svg
        :target: https://travis-ci.org/havakv/safescope

.. image:: https://readthedocs.org/projects/safescope/badge/?version=latest
        :target: https://safescope.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/havakv/safescope/shield.svg
     :target: https://pyup.io/repos/github/havakv/safescope/
     :alt: Updates


Python package for preventing use of variables from enclosing scope.


* Free software: BSD license
* Documentation: https://safescope.readthedocs.io.


Features
--------

This is a package that can be used for preventing functions from using global variables,
or variables from enclosing scopes.
The functionality is only meant for use in notebooks, and not real code.
Arguably, use of this package incurrage bad programming habits...

Quickstart:

.. code-block:: python
   from safescope import assert_local_v
   a 
   @assert_local_vars
   def foo():
       b = 5
       return a + b

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

