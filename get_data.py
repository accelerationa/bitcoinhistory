from datetime import date, timedelta
import os.path

FILE_PREFIX = 'data/bitstampUSD-'
FILE_SUFFIX = '.json'

def get_avalible_json_files(start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):
    delta = end_date - start_date 
    filenames = []
    for i in range(delta.days + 1):
        _date = start_date + timedelta(days=i)
        filename = FILE_PREFIX + str(_date) + FILE_SUFFIX
        filename = filename.replace('-01', '-1').replace('-02', '-2').replace('-03', '-3')\
                .replace('-04', '-4').replace('-05', '-5')\
                .replace('-06', '-6').replace('-07', '-7') \
                .replace('-08', '-8').replace('-09', '-9')
        if os.path.isfile(filename):
            filenames.append(filename)
    return filenames


def get_cols_of_one_day_from_json(filename):
    _file = open(filename, "r")
    json = _file.read()
    if json == '[]':
        return []
    strs = json.split('],[')
    datas = []
    cols = []
    for item in strs:
        datas.append(item.replace("]", "").replace("[", ""))
    for data in datas:
        col = []
        for _it in data.split(','):
            if _it.strip() != '':
                col.append(float(_it))
        if 1.7e+308 not in col:
            cols.append(col)
    return cols


def get_open_prices_of_one_day(filename):
    cols = get_cols_of_one_day_from_json(filename)
    open_prices = []
    for col in cols:
        open_prices.append(col[1])
    return open_prices

def get_cols_of_multipe_days(start_date, end_date):
    content = []
    filenames = get_avalible_json_files(start_date, end_date)
    for filename in filenames:
        content = content + get_cols_of_one_day_from_json(filename)
    return content


if __name__ == "__main__":
    # get_cols_of_one_day_from_json('data/bitstampUSD-2015-9-14.json')
    # get_open_prices_of_one_day('data/bitstampUSD-2015-9-14.json')
    # get_avalible_json_figles()

    get_cols_of_multipe_days(date(2017, 1, 1), date(2017, 1, 5))
    