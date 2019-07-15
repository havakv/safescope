# -*- coding: utf-8 -*-

import inspect
from safescope import side_scope


class Imports:
    """Context manager used for adding import to both global scope and
    `side_scope`.

    Example:
        from safescope import Imports, side_scope

        with Imports():
            import numpy as np
            import pandas as pd
        
        all(np.arange(5) == side_scope.np.arange(5)) # return True
    
    """
    namespace = side_scope
    def capture(self, name , value):
        self.namespace.__dict__[name] = value

    def __enter__(self):
        caller_frame = inspect.currentframe().f_back
        self.local_names = set(caller_frame.f_locals)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        caller_frame = inspect.currentframe().f_back
        changes = 0
        for name in caller_frame.f_locals:
            if name not in self.local_names:
                self.capture(name, caller_frame.f_locals[name])
                changes += 1
        if changes == 0:
            raise RuntimeError("Nothing new registered. If imports allready exists, "+
                               "you need to first delete them to make this take effect.")
        return False


def safescope(func):
    """Decorator for declaring function in `side_scope` in stead of global scope.
    This prevents the use of global variables.

    Example:
        x = 5
        @safescope
        def foo():
            print(x)
        
        foo() # NameError: name 'x' is not defined
    """
    func = type(func)(func.__code__, side_scope.__globals__, func.__name__,
                      func.__defaults__, func.__closure__)
    side_scope.add(func.__name__, func)
    return func

def _add_to_side_scope(name, value):
    """Add `value` to side_scope with name `name`.
    
    Arguments:
        name {str} -- Name of variable/function/import, etc.
        value {Any} -- Function/variable/import, etc.
    
    Example:
        import numpy
        side_scope.add('np', numpy)
        side_scope.np.arange(5)
    """
    side_scope.__dict__[name] = value

def _delete_from_side_scope(name):
    """Delete `name` from side_scope.
    
    Arguments:
        name {str} -- Name of variable/function/import, etc.
    """
    side_scope.__dict__.pop(name)

_add_to_side_scope('add', _add_to_side_scope)
_add_to_side_scope('delete', _delete_from_side_scope)

