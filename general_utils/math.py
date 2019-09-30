import numpy as np
import math


def polar_to_cart(r, theta, unit='deg'):
    if unit == 'deg':
        theta = np.deg2rad(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


def cart_to_polar(x, y, unit='deg'):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if unit == 'deg':
        theta = np.rad2deg(theta)
    return r, theta


def floor_to(x, to_value=0.05):
    """
    Floors x to the nearest multiple of to_value

    For example, floor_to(1.27, 0.05) evaluates to 1.25

    Args:
        x (float): Value to floor
        to_value (float): Value to floor to a multiple of

    Returns:
        (float)
    """
    return x // to_value * to_value


def ceil_to(x, to_value=0.05):
    """
    Ceils x to the nearest multiple of to_value

    For example, floor_to(1.27, 0.05) evaluates to 1.30

    Args:
        x (float): Value to floor
        to_value (float): Value to ceil to a multiple of

    Returns:
        (float)
    """
    return math.ceil(x / to_value) * to_value


def normalized_log(x):
    """
    Returns a the normalized value of the log for all numbers in x

    Useful for getting a weighting scheme that penalizes small classes less than sample-weighting, but
    more than arithmatic weighting

    When computing logs, 1 is added to all elements to avoid giving groups with a single sample a weight of 0
    """
    x = np.asarray(x)
    logx = np.log(x + 1)
    return logx / logx.sum()
