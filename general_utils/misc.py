import collections
import six


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
