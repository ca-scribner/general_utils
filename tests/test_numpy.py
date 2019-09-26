import pytest
import numpy as np

from general_utils.numpy import get_length_from_unicode_dtype, safe_insert_string


@pytest.mark.parametrize(
    "dtype, expected_length",
    (
        (np.dtype(('U', 1)), 1),
        (np.dtype(('U', 5)), 5),
        (np.dtype(('U', 10)), 10),
        (np.dtype(('U', 100)), 100),
    )
)
def test_get_length_from_unicode_dtype_1(dtype, expected_length):
    assert expected_length == get_length_from_unicode_dtype(dtype)


@pytest.mark.parametrize(
    "dtype",
    (
        np.dtype(('int', 32)),
    )
)
def test_get_length_from_unicode_dtype_exception(dtype):
    with pytest.raises(ValueError):
        get_length_from_unicode_dtype(dtype)


@pytest.mark.parametrize(
    "a, index, val, a_expected",
    (
        (np.array(('a', 'b', 'c')), 0, 'aaa', np.array(('aaa', 'b', 'c'))),
        (np.array(('a', 'b', 'c')), slice(1, None), 'xxx', np.array(('a', 'xxx', 'xxx'))),
        (np.array(('a', 'b', 'c')), 0, '0', np.array(('0', 'b', 'c'))),
    )
)
def test_safe_insert_string(a, index, val, a_expected):
    a_new = safe_insert_string(a, index, val)
    print(a_expected)
    print(a_new)
    assert np.all(a_expected == a_new)
