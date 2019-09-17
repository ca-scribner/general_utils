import pytest
import numpy as np

from general_utils.math import cart_to_polar, polar_to_cart, floor_to, ceil_to

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

    assert cart_to_polar(settings['x'], settings['y'], unit=settings['unit']) == \
           pytest.approx((settings['r'], settings['theta']))
    assert polar_to_cart(settings['r'], settings['theta'], unit=settings['unit']) == \
           pytest.approx((settings['x'], settings['y']))
    temprt = cart_to_polar(settings['x'], settings['y'], unit=settings['unit'])
    tempxy = polar_to_cart(temprt[0], temprt[1], unit=settings['unit'])
    assert tempxy == pytest.approx((settings['x'], settings['y']))


@pytest.mark.parametrize(
    "settings",
    [
        {'x': 1.27, 'to_value': 0.05, 'result': 1.25},
        {'x': 1.27, 'to_value': 0.1, 'result': 1.2},
        {'x': 1.27, 'to_value': 0.3, 'result': 1.2},
        {'x': 1.27, 'to_value': 1.1, 'result': 1.1},
        {'x': 1.27, 'to_value': 1.5, 'result': 0.0},
        {'x': -1.27, 'to_value': 0.1, 'result': -1.3},
        {'x': 0, 'to_value': 0.1, 'result': 0.0},
    ]
)
def test_floor_to(settings):
    assert floor_to(settings['x'], settings['to_value']) == pytest.approx(settings['result'])


@pytest.mark.parametrize(
    "settings",
    [
        {'x': 1.25, 'to_value': 0.05, 'result': 1.25},
        {'x': 1.27, 'to_value': 0.1, 'result': 1.3},
        {'x': 1.27, 'to_value': 0.3, 'result': 1.5},
        {'x': 1.27, 'to_value': 1.1, 'result': 2.2},
        {'x': 1.27, 'to_value': 1.5, 'result': 1.5},
        {'x': -1.27, 'to_value': 0.1, 'result': -1.2},
        {'x': 0, 'to_value': 0.1, 'result': 0.0},
    ]
)
def test_ceil_to(settings):
    assert ceil_to(settings['x'], settings['to_value']) == pytest.approx(settings['result'])
