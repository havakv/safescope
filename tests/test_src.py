import pytest
from safescope import side_scope, safescope, Imports

def delete(*names):
    for name in names:
        side_scope.delete(name)
    for name in names:
        with pytest.raises(KeyError):
            side_scope.__dict__['name']

def test_add_remove_from_side_scope():
    import itertools
    side_scope.add('count', itertools.count)
    assert next(side_scope.count(5)) == 5
    side_scope.delete('count')
    with pytest.raises(AttributeError) as e:
        side_scope.count(5)
    assert str(e.value) == "module 'safescope.side_scope' has no attribute 'count'"
        

def test_removed_from_side_scope():
    with pytest.raises(AttributeError) as e:
        side_scope.count(5)
    assert str(e.value) == "module 'safescope.side_scope' has no attribute 'count'"

def test_imports():
    with pytest.raises(NameError):
        itertools
    with pytest.raises(NameError):
        functools
    with Imports():
        import itertools
        import functools
    assert itertools is not None
    assert functools is not None
    assert hasattr(side_scope, 'itertools')
    assert hasattr(side_scope, 'functools')
    delete('itertools', 'functools')

def test_imports_as():
    with Imports():
        import itertools as itools
        import functools as ftools
    assert itools is not None
    assert ftools is not None
    assert hasattr(side_scope, 'itools')
    assert hasattr(side_scope, 'ftools')
    delete('itools', 'ftools')

def test_imports_after():
    import itertools
    with pytest.raises(RuntimeError) as e:
        with Imports():
            import itertools
    assert str(e.value) == 'Nothing new registered. If imports allready exists, you need to first delete them to make this take effect.'

x = 5

def test_safescope_name_error():
    def foo():
        return x
    assert foo() == 5, 'Something wrong with setup of test'

    @safescope
    def foo2():
        return x

    with pytest.raises(NameError) as e:
        foo2()
    assert str(e.value) == "name 'x' is not defined"
    delete('foo2')

@safescope
def ss_returns_4():
    return 4

def test_safescope_working_func():
    assert ss_returns_4 is side_scope.ss_returns_4, 'Identical in both scopes'
    assert ss_returns_4() == side_scope.ss_returns_4(), 'Both works'

@safescope
def ss_calls_ss_returns_4():
    return ss_returns_4()

def test_safescope_2_funcs():
    global ss_calls_ss_returns_4
    assert ss_calls_ss_returns_4() == 4
    global ss_returns_4
    del ss_returns_4
    assert ss_calls_ss_returns_4() == 4
    del ss_calls_ss_returns_4
    assert side_scope.ss_calls_ss_returns_4() == 4

class Foo:
    def not_safe(self):
        self.x = x
        return self.x

    @safescope
    def safe(self):
        self.x = x
        return self.x

def test_class_method_name_error():
    foo = Foo()
    assert foo.not_safe() == 5
    with pytest.raises(NameError) as e:
        foo.safe()
    assert str(e.value) == "name 'x' is not defined"

class Foo2:
    @safescope
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @safescope
    def return_a(self):
        return self.a

    @safescope
    def return_a_plus_b_by_return_a(self):
        return self.return_a() + self.b

def test_class_method_calls_method():
    a, b = 3, 4
    foo = Foo2(a, b)
    assert foo.return_a() == 3
    assert foo.return_a_plus_b_by_return_a() == (a + b)
