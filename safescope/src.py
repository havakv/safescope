# -*- coding: utf-8 -*-

from __future__ import annotations
import inspect
from typing import Callable
from types import ModuleType
from safescope import _side_scope


class _LocalsCapture:
    def __enter__(self) -> _LocalsCapture:
        caller_frame = inspect.currentframe().f_back
        self.local_names = set(caller_frame.f_locals)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        caller_frame = inspect.currentframe().f_back
        for name in caller_frame.f_locals:
            if name not in self.local_names:
                self.capture(name, caller_frame.f_locals[name])

class imports(_LocalsCapture):
    namespace = _side_scope
    def capture(self, name:str , value: ModuleType):
        self.namespace.__dict__[name] = value


def safescope(func: Callable) -> Callable:
    """Decorator for preventing a function from using variables outside
    the function scope
    
    Arguments:
        func {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    func = type(func)(func.__code__, _side_scope.__globals__, func.__name__,
                      func.__defaults__, func.__closure__)
    return func
