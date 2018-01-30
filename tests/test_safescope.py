#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `safescope` package."""

import re
import pytest

from safescope import safescope

glob_a = 0
glob_b = 1

def func_with_glob():
    c = 0
    return glob_a + glob_b

class Foo(object):
    def bar(self):
        return 0

def func_with_class():
    c = Foo()
    return glob_a + c

def foo():
    return 0

def func_with_func():
    c = foo()
    return glob_a + c

def func_with_module():
    c = re.LOCALE
    return glob_b + c

obj = Foo()

def func_with_object():
    c = obj.bar()
    return glob_b + c

class ClassWithVar(object):
    def __init__(self, a):
        self.a = a
        self.glob_b = glob_b


class TestGetNonLocalVarNames(object):
    def test_func_with_glob(self):
        res = safescope.get_non_local_var_names(func_with_glob)
        assert sorted(res) == ['glob_a', 'glob_b']

    def test_func_with_class(self):
        res = safescope.get_non_local_var_names(func_with_class)
        assert res == ['glob_a']

    def test_func_with_func(self):
        res = safescope.get_non_local_var_names(func_with_func)
        assert res == ['glob_a']

    def test_func_with_module(self):
        res = safescope.get_non_local_var_names(func_with_module)
        assert res == ['glob_b']

    def test_func_with_object(self):
        res = safescope.get_non_local_var_names(func_with_object)
        assert sorted(res) == ['glob_b', 'obj']

    def test_class_with_var(self):
        res = safescope.get_non_local_var_names(ClassWithVar.__init__)
        assert res == ['glob_b']
