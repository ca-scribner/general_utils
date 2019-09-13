import numpy as np

def polarToCart(r, theta, unit='deg'):
    if unit == 'deg':
        theta = np.deg2rad(theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def cartToPolar(x, y, unit='deg'):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    if unit == 'deg':
        theta = np.rad2deg(theta)
    return r, theta