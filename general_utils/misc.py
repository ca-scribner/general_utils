import collections
import six
import time
import re


def is_iterable(arg):
    """
    Returns whether an argument is an iterable but not a string

    From stackoverflow: "how to tell a varaiable is iterable but not a string"

    Args:
        arg: some variable to be tested

    Returns:
        (bool)
    """
    return (
        isinstance(arg, collections.Iterable)
        and not isinstance(arg, six.string_types)
        )


class Timer:
    def __init__(self):
        """
        Construct a simple timer class
        """
        self.reference_time = None
        self.reset()

    def elapsed(self):
        """
        Return the time elapsed between when this object was instantiated (or last reset) and now

        Returns:
            (float): Time elapsed in seconds
        """
        return time.perf_counter() - self.reference_time

    def reset(self):
        """
        Reset the reference timepoint to now

        Returns:
            None
        """
        self.reference_time = time.perf_counter()


def network_path_to_python(path):
    """
    Convert a network path (right click, copy network path) to a path that works in python

    Args:
        path (str): Path, like "file://somewhere/some%20thing.txt"

    Returns:
        (str): Path in format that will work inside Python, eg:
                    "file://somewhere/some%20thing.txt"
               becomes
                    "file:\\somewhere\some thing.txt"
    """
    path = re.sub(r'file:', '', path)
    path = re.sub(r'/',  "\\\\" , path)
    path = re.sub(r'%20', ' ', path)
    return path
