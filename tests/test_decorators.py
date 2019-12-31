import pytest
from general_utils.decorators import read_only_properties


class TestClass:
    def __init__(self):
        self.a = 1
        self.b = 2


def test_read_only_properties():
    """
    Test accessing and attempting to write a class wrapped read_only_properties decorator
    """
    unprotected = TestClass()
    ProtectedTestClass = read_only_properties('b')(TestClass)
    protected = ProtectedTestClass()

    assert 1 == unprotected.a
    assert 2 == unprotected.b

    new_a = 10
    unprotected.a = new_a
    protected.a = new_a
    assert new_a == unprotected.a
    assert new_a == protected.a

    with pytest.raises(AttributeError):
        protected.b = 10
