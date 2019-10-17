import numpy as np


def safe_astype(ds, dtype, always_convert_to_object=True):
    """
    Return a copy of a Pandas Series converted to a new dtype, actively preserving np.nan entries in the original data.
    
    This is useful to avoid things like how ds.astype(str) will convert np.nan entries into a string 'nan'.
    The output series may be of type object so that it can have mixed types (mix of string and np.nan (float), 
    for example)
    
    Args:
        ds (pandas.Series): Data to be converted
        dtype: Valid data type that pd.Series.astype() accepts
        always_convert_to_object (bool): If True, always return a series that is of dtype object
                                         If False, only return dtype of object if there are np.nan entries in the original data
        
    Return:
        (pd.Series): Converted data, likely of dtype object
    """
    ds = ds.copy()
    if always_convert_to_object or ds.isna().sum() > 0:
        ds = ds.astype(object)
        ds.loc[ds.notna()] = ds.loc[ds.notna()].astype(dtype)
    else:
        # Convert everything since there are no NaN
        ds = ds.astype(dtype)
    return ds


def get_zero_axes(df, return_sums=False, axis=1, isclose_kwargs=None):
    """
    Returns the name and integer index of all rows (or columns) that have an axis-wise sum of 0.

    Whether the sums equal zero are determined using np.isclose.  If isclose_kwargs==None, the default np.isclose
    tolerances will be applied.

    Optionally also returns the sums in a pd.Series

    Args:
        df (pd.DataFrame): DataFrame to be evaluated
        return_sums (Boolean): If True, returns an extra argument with the sums as a pd.Series
        axis (int): Integer axis passed to df.sum().  Must be 0 or 1 (DataFrame is only 2 dimensional).
                    Axis follows the pandas/numpy convention for axis numbering, which denotes which axis will be
                    collapsed during the operation.  For example:
                        axis==0: Results in get_zero_axes returning which columns sum to zero (because axis=0
                        denotes the 0th (rows) axes be collapsed)
                        axis==1: (DEFAULT) Results in get_zero_axes returning which rows sum to zero (because axis=1
                        denotes the 1th (columns) axes be collapsed)
        isclose_kwargs (dict): keyword arguments passed directly to np.isclose().  To override np.isclose defaults for \
                               testing if sum is 0, use these arguments (eg, set {'atol': 0.001})

    Returns:
        Tuple of:
            (np.array): Names of the empty rows (or columns, depending on axis)
            (np.array): Integer index of the empty rows (or columns, depending on axis)
            (pd.Series): (if return_sums==True) Series of the summed data used to compute names and integers
    """
    if isclose_kwargs is None:
        isclose_kwargs = {}

    if axis > 1:
        raise NotImplementedError("Got axis={axis}.  Function not tested for axis > 1")

    row_sums = df.sum(axis=axis)
    zero_bool = np.isclose(row_sums, 0.0, **isclose_kwargs)
    zero_names = row_sums.index[zero_bool].values
    zero_indices = np.arange(len(row_sums))[zero_bool]

    if return_sums:
        return zero_names, zero_indices, row_sums
    else:
        return zero_names, zero_indices
