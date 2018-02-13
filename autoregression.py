import boto3
from get_data import get_cols_of_multipe_days
from datetime import date, timedelta, datetime


from matplotlib import pyplot
import pandas as pd
from pandas.plotting import lag_plot
from pandas import concat
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AR






def find_columns_with_interval(interval, start_date=date(2010, 1, 1), end_date=date(2050, 12, 31)):




    columns = get_cols_of_multipe_days(start_date, end_date)
    if len(columns) == 0:
        return []

    base = columns[0][0]
    
    

    size = ((columns[-1][0] - columns[0][0]) / interval/60 + 1)

    ret = [[0]] * int(size)

    


    for col in columns:
        index = int(int(col[0] - base) / interval / 60)

        if col[0] > ret[index][0]:
            ret[index] = col

    


    for i in range(0, len(ret)-1):
        if ret[i] == [0]:
            ret[i] = ret[i-1]
    

    """
    Note: Time is trash, DO NOT USE!!!!
    """
    y=np.array([np.array(xi) for xi in ret])


    content = [('Open', y[:, 1]), ('Volumn', y[:, 6]), ('Weighted Price', y[:, 7])]
    df = pd.DataFrame.from_items(content)
    print df

    # lag_plot(df['Open'], 1)



    # plot_acf(df['Open'], lags=50)


    # create lagged dataset
    dataframe = concat([df['Open'].shift(1), df['Open']], axis=1)
    dataframe.columns = ['t-1', 't+1']
    # split into train and test sets
    X = dataframe.values



    train, test = X[1:int(len(X)*0.8)], X[int(len(X)*0.8): ]

    train_X, train_y = train[:,0], train[:,1]
    test_X, test_y = test[:,0], test[:,1]
    
    # persistence model
    def model_persistence(x):
        return x
    
    # walk-forward validation
    predictions = list()
    for x in test_X:
        yhat = model_persistence(x)
        predictions.append(yhat)
    test_score = mean_squared_error(test_y, predictions)
    print('Test MSE: %.3f' % test_score)
    # plot predictions vs expected
    pyplot.plot(test_y)
    pyplot.plot(predictions, color='yellow')
    pyplot.show()
    













    # split dataset
    X = df['Open'].values
    train, test = X[1:int(len(X)*0.8)], X[int(len(X)*0.8): ]



    # train autoregression
    model = AR(train)
    model_fit = model.fit()




    print('Lag: %s' % model_fit.k_ar)
    print('Coefficients: %s' % model_fit.params)


    # make predictions
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    # for i in range(len(predictions)):
    #     print('predicted=%f, expected=%f' % (predictions[i], test[i]))
    error = mean_squared_error(test, predictions)
    print('Test MSE: %.3f' % error)
    # plot results
    pyplot.plot(test)
    pyplot.plot(predictions, color='green')

    pyplot.show()

        
if __name__ == "__main__":
    find_columns_with_interval(10, date(2017, 10,1), date(2017,12,31))