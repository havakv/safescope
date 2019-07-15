"""This is a file for creating an extra scope"""

def __def_function__() -> None:
    """To get __globals__ for this scope."""
    pass

__globals__ = __def_function__.__globals__
