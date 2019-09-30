import pytest
import pandas as pd
import numpy as np

from general_utils.pandas import get_zero_axes

from contextlib import contextmanager


# Helpers
@contextmanager
def does_not_raise():
    yield


@pytest.fixture
def build_random_df():
    d = [
        {'Col0': 0.2, 'Col1': 0.8, 'Col2': 0.0},
        {'Col0': 0.0, 'Col1': 0.0, 'Col2': 0.000000001},
        {'Col0': 0.3, 'Col1': 0.7, 'Col2': 0.0},
        {'Col0': 0.0, 'Col1': 0.0, 'Col2': 0.0},
        {'Col0': 0.5, 'Col1': 0.5, 'Col2': 0.0},
    ]
    rows = [f'Row{i}' for i in range(len(d))]
    df = pd.DataFrame(d, index=rows)
    return df


@pytest.mark.parametrize(
    "isclose_kwargs,axis,expected",
    (
        # col-wise tests
        # Test with default isclose values
        (
            {},
            0,
            {
                'zero_names': np.array(['Col2']),
                'zero_indices': np.array([2]),
                'row_sums': np.array([1.0, 2.0, 0.000000001]),
                'raises': does_not_raise(),
            }
         ),
        # Test with overridden isclose values
        (
            {'atol': 1e-10},
            0,
            {
                'zero_names': np.array([]),
                'zero_indices': np.array([]),
                'row_sums': np.array([1.0, 2.0, 0.000000001]),
                'raises': does_not_raise(),
            }
         ),

        # row-wise tests
        # Test with default isclose values
        (
            {},
            1,
            {
                'zero_names': np.array(['Row1', 'Row3']),
                'zero_indices': np.array([1, 3]),
                'row_sums': np.array([1.0, 0.000000001, 1., 0., 1.]),
                'raises': does_not_raise(),
            }
         ),
        # Test with overridden isclose values
        (
            {'atol': 1e-10},
            1,
            {
                'zero_names': np.array(['Row3']),
                'zero_indices': np.array([3]),
                'row_sums': np.array([1.0, 0.000000001, 1., 0., 1.]),
                'raises': does_not_raise(),
            }
        ),
    )
)
def test_get_zero_axes(build_random_df, isclose_kwargs, axis, expected):
    df = build_random_df
    print(df)

    with expected['raises']:
        zero_names, zero_indices, row_sums = get_zero_axes(df, return_sums=True, isclose_kwargs=isclose_kwargs, axis=axis)

        print(zero_names)
        assert np.all(expected['zero_names'] == zero_names)
        assert np.all(expected['zero_indices'] == zero_indices)
        assert np.all(expected['row_sums'] == pytest.approx(row_sums))

# NOTE: return_sums argument for get_zero_axes is not captured in this test suite
