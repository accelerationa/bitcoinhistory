import boto3
from get_data import get_cols_of_multipe_days
from datetime import date, timedelta, datetime

def write_item_to_ddb(item):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('BitcoinHistoryData')


    response = table.put_item(
        Item = item
    )


def create_item_for_ddb(col):
    if len(col) < 8:
        print 'Error: unexpected column.'
        return
    item = {}
    item['Time'] = str(col[0])
    item['Open'] = str(col[1])
    item['High'] = str(col[2])
    item['Low'] = str(col[3])
    item['Close'] = str(col[4])
    item['Volumn_BTC'] = str(col[5])
    item['Volumn_Currency'] = str(col[6])
    item['WeightedPrice_USD '] = str(col[7])

    return item

def bulk_write_to_ddb(start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):
    columns = get_cols_of_multipe_days(start_date, end_date)

    for col in columns:
        try:
            print 'Writing %s' % datetime.fromtimestamp(float(col[0])).isoformat()
            write_item_to_ddb(create_item_for_ddb(col))
        except:
            pass

if __name__ == "__main__":
    bulk_write_to_ddb()