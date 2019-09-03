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