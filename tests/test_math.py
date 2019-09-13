import pytest
import numpy as np

from general_utils.math import cartToPolar, polarToCart

@pytest.mark.parametrize(
    "settings",
    [
        {'x': 1., 'y': 0., 'r': 1., 'theta': 0., 'unit': 'deg'},
        {'x': 1., 'y': 1., 'r': np.sqrt(2.), 'theta': 45., 'unit': 'deg'},
        {'x': 0., 'y': 1., 'r': 1., 'theta': 90., 'unit': 'deg'},
        {'x': -1., 'y': 1., 'r': np.sqrt(2.), 'theta': 135., 'unit': 'deg'},
        {'x': -1., 'y': 0., 'r': 1., 'theta': 180., 'unit': 'deg'},
        {'x': -1., 'y': -1., 'r': np.sqrt(2.), 'theta': -135., 'unit': 'deg'},
        {'x': 0., 'y': -1., 'r': 1., 'theta': -90., 'unit': 'deg'},
        {'x': 1., 'y': -1., 'r': np.sqrt(2.), 'theta': -45., 'unit': 'deg'},

        {'x': 1., 'y': 0., 'r': 1., 'theta': np.deg2rad(0.), 'unit': 'rad'},
        {'x': 1., 'y': 1., 'r': np.sqrt(2.), 'theta': np.deg2rad(45.), 'unit': 'rad'},
        {'x': 0., 'y': 1., 'r': 1., 'theta': np.deg2rad(90.), 'unit': 'rad'},
        {'x': -1., 'y': 1., 'r': np.sqrt(2.), 'theta': np.deg2rad(135.), 'unit': 'rad'},
        {'x': -1., 'y': 0., 'r': 1., 'theta': np.deg2rad(180.), 'unit': 'rad'},
        {'x': -1., 'y': -1., 'r': np.sqrt(2.), 'theta': np.deg2rad(-135.), 'unit': 'rad'},
        {'x': 0., 'y': -1., 'r': 1., 'theta': -np.deg2rad(90.), 'unit': 'rad'},
        {'x': 1., 'y': -1., 'r': np.sqrt(2.), 'theta': np.deg2rad(-45.), 'unit': 'rad'},
        #
        # {'x': -1., 'y': 0., 'r': 1., 'theta': 90., 'unit': 'deg'},
        # {'x': -1., 'y': -1., 'r': np.sqrt(2.0), 'theta': 135., 'unit': 'deg'},
        # {'x': 5., 'y': 3., 'r': np.sqrt(5**2 + 3**2), 'theta': 30.9637565, 'unit': 'deg'},
        # {'x': 1., 'y': 0., 'r': 1., 'theta': np.deg2rad(0.), 'unit': 'rad'},
        # {'x': 1., 'y': 1., 'r': np.sqrt(2.), 'theta': np.deg2rad(90.), 'unit': 'rad'},
        # {'x': -1., 'y': 0., 'r': 1., 'theta': np.deg2rad(180.), 'unit': 'rad'},
        # {'x': -1., 'y': -1., 'r': np.sqrt(2.0), 'theta': np.deg2rad(270.), 'unit': 'rad'},
        # {'x': 5., 'y': 3., 'r': np.sqrt(5**2 + 3**2), 'theta': np.deg2rad(30.9637565), 'unit': 'rad'},
    ]
)
def test_cartToPolar_polarToCart(settings):

    assert cartToPolar(settings['x'], settings['y'], unit=settings['unit']) == \
           pytest.approx((settings['r'], settings['theta']))
    assert polarToCart(settings['r'], settings['theta'], unit=settings['unit']) == \
           pytest.approx((settings['x'], settings['y']))
    temprt = cartToPolar(settings['x'], settings['y'], unit=settings['unit'])
    tempxy = polarToCart(temprt[0], temprt[1], unit=settings['unit'])
    assert tempxy == pytest.approx((settings['x'], settings['y']))
