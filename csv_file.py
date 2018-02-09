import csv
from datetime import date
from get_data import get_cols_of_multipe_days


def write_to_csv(start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):
    content = get_cols_of_multipe_days(start_date, end_date)
    content = [['TimeStamp', 'Open', 'High', 'Low', 'Close', 'Volumn - BTC', \
                        'Volumn - Currency', 'Weighted Price (USD)']] + content
    csvfile = open('bitcoin_history_data.csv', 'w')
    with csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(content)
    print "Writing complete"



if __name__ == "__main__":
    # write_to_csv(date(2010, 1, 1), date(2014, 12, 31))
    write_to_csv(date(2017, 1, 1), date(2017, 1, 5))
    