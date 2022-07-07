import numpy as np
from numpy.lib.stride_tricks import as_strided
import pandas as pd
from pandas.tseries.offsets import BDay


def roll(*args, **kwargs):
    """
    Calculates a given statistic across a rolling time period.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~empyrical.stats.cum_returns`.
    factor_returns (optional): float / series
        Benchmark return to compare returns against.
    function:
        the function to run for each rolling window.
    window (keyword): int
        the number of periods included in each calculation.
    (other keywords): other keywords that are required to be passed to the
        function in the 'function' argument may also be passed in.

    Returns
    -------
    np.ndarray, pd.Series
        depends on input type
        ndarray(s) ==> ndarray
        Series(s) ==> pd.Series

        A Series or ndarray of the results of the stat across the rolling
        window.

    """
    func = kwargs.pop("function")
    window = kwargs.pop("window")
    if len(args) > 2:
        raise ValueError("Cannot pass more than 2 return sets")

    if len(args) == 2:
        if not isinstance(args[0], type(args[1])):
            raise ValueError("The two returns arguments are not the same.")

    if isinstance(args[0], np.ndarray):
        return _roll_ndarray(func, window, *args, **kwargs)
    return _roll_pandas(func, window, *args, **kwargs)


def up(returns, factor_returns, **kwargs):
    """
    Calculates a given statistic filtering only positive factor return periods.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~empyrical.stats.cum_returns`.
    factor_returns (optional): float / series
        Benchmark return to compare returns against.
    function:
        the function to run for each rolling window.
    (other keywords): other keywords that are required to be passed to the
        function in the 'function' argument may also be passed in.

    Returns
    -------
    Same as the return of the function
    """
    func = kwargs.pop("function")
    returns = returns[factor_returns > 0]
    factor_returns = factor_returns[factor_returns > 0]
    return func(returns, factor_returns, **kwargs)


def down(returns, factor_returns, **kwargs):
    """
    Calculates a given statistic filtering only negative factor return periods.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~empyrical.stats.cum_returns`.
    factor_returns (optional): float / series
        Benchmark return to compare returns against.
    function:
        the function to run for each rolling window.
    (other keywords): other keywords that are required to be passed to the
        function in the 'function' argument may also be passed in.

    Returns
    -------
    Same as the return of the 'function'
    """
    func = kwargs.pop("function")
    returns = returns[factor_returns < 0]
    factor_returns = factor_returns[factor_returns < 0]
    return func(returns, factor_returns, **kwargs)


def _roll_ndarray(func, window, *args, **kwargs):
    data = []
    for i in range(window, len(args[0]) + 1):
        rets = [s[i - window : i] for s in args]
        data.append(func(*rets, **kwargs))
    return np.array(data)


def _roll_pandas(func, window, *args, **kwargs):
    data = {}
    index_values = []
    for i in range(window, len(args[0]) + 1):
        rets = [s.iloc[i - window : i] for s in args]
        index_value = args[0].index[i - 1]
        index_values.append(index_value)
        data[index_value] = func(*rets, **kwargs)
    return pd.Series(data, index=type(args[0].index)(index_values))


def get_utc_timestamp(dt):
    """
    Returns the Timestamp/DatetimeIndex
    with either localized or converted to UTC.

    Parameters
    ----------
    dt : Timestamp/DatetimeIndex
        the date(s) to be converted

    Returns
    -------
    same type as input
        date(s) converted to UTC
    """

    dt = pd.to_datetime(dt)
    try:
        dt = dt.tz_localize("UTC")
    except TypeError:
        dt = dt.tz_convert("UTC")
    return dt


def rolling_window(array, length, mutable=False):
    """
    Restride an array of shape

        (X_0, ... X_N)

    into an array of shape

        (length, X_0 - length + 1, ... X_N)

    where each slice at index i along the first axis is equivalent to

        result[i] = array[length * i:length * (i + 1)]

    Parameters
    ----------
    array : np.ndarray
        The base array.
    length : int
        Length of the synthetic first axis to generate.
    mutable : bool, optional
        Return a mutable array? The returned array shares the same memory as
        the input array. This means that writes into the returned array affect
        ``array``. The returned array also uses strides to map the same values
        to multiple indices. Writes to a single index may appear to change many
        values in the returned array.

    Returns
    -------
    out : np.ndarray

    Example
    -------
    >>> from numpy import arange
    >>> a = arange(25).reshape(5, 5)
    >>> a
    array([[ 0,  1,  2,  3,  4],
           [ 5,  6,  7,  8,  9],
           [10, 11, 12, 13, 14],
           [15, 16, 17, 18, 19],
           [20, 21, 22, 23, 24]])

    >>> rolling_window(a, 2)
    array([[[ 0,  1,  2,  3,  4],
            [ 5,  6,  7,  8,  9]],
    <BLANKLINE>
           [[ 5,  6,  7,  8,  9],
            [10, 11, 12, 13, 14]],
    <BLANKLINE>
           [[10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19]],
    <BLANKLINE>
           [[15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24]]])
    """
    if not length:
        raise ValueError("Can't have 0-length window")

    orig_shape = array.shape
    if not orig_shape:
        raise IndexError("Can't restride a scalar.")
    elif orig_shape[0] < length:
        raise IndexError(
            "Can't restride array of shape {shape} with"
            " a window length of {len}".format(
                shape=orig_shape,
                len=length,
            )
        )

    num_windows = orig_shape[0] - length + 1
    new_shape = (num_windows, length) + orig_shape[1:]

    new_strides = (array.strides[0],) + array.strides

    out = as_strided(array, new_shape, new_strides)
    out.setflags(write=mutable)
    return out
