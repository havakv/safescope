# -*- coding: utf-8 -*-

'''Main module.'''
import inspect
import re

def assert_local_vars(func):
    '''Decorator that ensures that function func does not use
    variables from enclosing scopes.
    '''
    var_names = get_non_local_var_names(func)
    if len(var_names) > 0:
        raise ValueError('Variables: ' + '[' + ', '.join(var_names) + '] ' +
                         'not in local scope.')
    return func

def get_non_local_var_names(func):
    '''Returns list of variables used in func that are from
    enclosing scopes.
    '''
    obj_names = []
    obj_names += non_local_callable_class_objects(func)
    obj_names += non_local_non_callable_variables(func)
    return obj_names

def non_local_callables(func):
    '''Returns list with name of objects that are callable (functions)
    from the enclosing scopes.
    '''
    call_list = []
    candidates = set(func.__code__.co_names) - set(func.__code__.co_varnames)
    # for name in func.__code__.co_names:
    for name in candidates:
        try:
            eval(name, func.__globals__)
        except NameError:
            continue

        if callable(eval(name, func.__globals__)):
            call_list.append(name)
    return call_list

def _name_is_func_or_class(name, globals):
    '''If name is a function in global scope.'''
    return eval(name, globals).__class__.__name__ in\
                ['function', 'builtin_function_or_method', 'type', 'CPUDispatcher']

def non_local_callable_class_objects(func):
    '''Returns list with names of objects that are callable, but not functions.
    '''
    func_names = non_local_callables(func)
    return [name for name in func_names if not  _name_is_func_or_class(name, func.__globals__)]

def _name_is_module(name, globals):
    '''If name is a package in global scope.'''
    return eval(name, globals).__class__.__name__ == 'module'

def non_local_non_callable_variables(func):
    '''Returns list with names of variables that are not callable from
    enclosing scopes.
    '''
    func_names = non_local_callables(func)
    non_callables = set(func.__code__.co_names) -\
                    set(func.__code__.co_varnames) -\
                    set(func_names)
    # non_callables = set(func.__code__.co_names) - set(func_names)

    source = inspect.getsource(func)
    source = re.sub(r'^.*\n', '', source) # remove first line
    source = re.sub(r'^def .*\n', '', source) # remove def line (if it was not first)
    non_callables = [name for name in non_callables
                     if len(re.findall(r'[^\.]' + name + r'[^a-zA-z0-9_]', source)) > 0]

    if func.__code__.co_name in non_callables:
        non_callables.remove(func.__code__.co_name) # To handle recursion
    return [name for name in non_callables if not _name_is_module(name, func.__globals__)]
