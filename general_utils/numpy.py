import numpy as np


SIZEOF_NUMPY_UNICODE_CHAR = np.dtype('U1').itemsize


def safe_insert_string(a, index, val):
    """
    Returns a copy of a with a[index]=val in a way that will automatically increase the unicode length of a if necessary

    Args:
        a (np.array): Array to be copied and modified.  Should be of a string-like dtype
        index (valid np.array index): Any type that can be used like a[index]
        val (str): Data to be set in array a.  Should be string, but may be coerced to a string automatically if not
                   a string.

    Returns:
        (np.array): Copy of array a with a[index]=val
    """
    # FUTURE: In numpy 1.19, np.can_cast(from_, to_, kind='same') will identify if casting from one type to another will
    # result in a truncation.  That can simplify this function
    if a.dtype.char == 'U':
        a = a.copy()
        # Get larger of dtypes for a and val and upcast a if necessary
        a_length = get_length_from_unicode_dtype(a.dtype)
        val_length = get_length_from_unicode_dtype(np.array([val], dtype='U').dtype)
        if val_length > a_length:
            a = a.astype(f'U{val_length}')
        a[index] = val
        return a
    else:
        raise ValueError("Array a is not a string-like numpy array")


def get_length_from_unicode_dtype(dtype):
    """
    Returns the length of a numpy unicode dtype

    For example, dtype="<U10" returns 10.

    This same method might work for other types, but this has not been tested and will raise a ValueError

    Args:
        dtype (numpy.dtype): Numpy dtype to be inspected

    Returns:
        (int): Length of the dtype
    """

    if dtype.char == 'U':
        return dtype.itemsize // SIZEOF_NUMPY_UNICODE_CHAR
        # return int(dtype.descr[0][1][2:])  # Old method that seems less robust but does work
    else:
        raise ValueError("dtype must be a string-like numpy dtype")