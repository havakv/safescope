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
    for name in func.__code__.co_names:
        try:
            eval(name, func.__globals__)
        except NameError:
            continue

        if callable(eval(name, func.__globals__)):
            call_list.append(name)
    return call_list

def _name_is_function(name, globals):
    '''If name is a function in global scope'''
    return eval(name, globals).__class__.__name__ not in\
                ['function', 'builtin_function_or_method']

def non_local_callable_class_objects(func):
    '''Returns list with names of objects that are callable, but not functions.
    '''
    func_names = non_local_callables(func)
    return [name for name in func_names if _name_is_function(name, func.__globals__)]

def non_local_non_callable_variables(func):
    '''Returns list with names of variables that are not callable from
    enclosing scopes.
    '''
    func_names = non_local_callables(func)
    non_callables = set(func.__code__.co_names) - set(func_names)

    source = inspect.getsource(func)
    return [name for name in non_callables
            if len(re.findall(r'[^\.]' + name + r'[^a-zA-z0-9_]', source)) > 0]
