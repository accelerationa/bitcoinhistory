from datetime import date, timedelta
import numpy as np
from get_data import get_avalible_json_files, get_cols_of_multipe_days, get_open_prices_of_one_day

def get_variance_for_open_prices_in_one_day(filename):
    open_prices = get_open_prices_of_one_day(filename)
    variance = np.var(open_prices)
    return variance, len(open_prices)


def get_variance_open_prices_by_day(start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):
    """get the variance of open prices by days
    returns the variance of each day in a dict
    return structure {'date': {
        'variance': variance
        'data_number': number of datas used to get this variance
    }}
    data_number is used to prevent if in one day, there are too few data
    """

    dict_variance = {}
    filenames = get_avalible_json_files(start_date, end_date)
    _i = 0
    for filename in filenames:
        _date = start_date + timedelta(days=_i)
        _i += 1
        variance, data_number = get_variance_for_open_prices_in_one_day(filename)
        dict_variance[str(_date)] = {'variance': variance, 'data_number': data_number}
    return dict_variance


def get_variance_open_prices_through_days(start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):
    """get the variance of open prices through days
    returns only one variance
    """

    open_prices = []
    filenames = get_avalible_json_files(start_date, end_date)
    for filename in filenames:
        open_prices = open_prices + get_open_prices_of_one_day(filename)
    variance = np.var(open_prices)
    return variance


if __name__ == "__main__":
    get_variance_open_prices_through_days(date(2015, 11, 1), date(2015, 11, 4))