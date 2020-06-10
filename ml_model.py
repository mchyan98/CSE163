'''
Jacob Chan, Michael Chyan, Michael Mok
CSE 163 Project

This file includes the functions that cleans the datasets, creates the
machine learning models, and plots them on a graph.
'''
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns


def prepare_sp_data(tickers, sp_all):
    '''
    Takes in two dataframes. One is the sp500 companies and sectors.
    The other is the stock prices. It returns a tuple of two data
    frames.
    '''
    # isolate 500 stocks in S&P 500
    tickers_sectors = tickers[['Symbol', 'Sector']]

    # Merges industry and day prices for S&P 500 stocks
    sp500_industry = tickers_sectors.merge(sp_all, left_on='Symbol',
                                           right_on='Name')
    sp500_industry = sp500_industry.drop(['Name', 'volume'], axis=1)
    sp500_groupby = sp500_industry.groupby(['Sector', 'date'],
                                           as_index=False)['close'].sum()
    industries = sp500_industry.groupby('Sector')['close'].sum()
    sector_list = industries.index.tolist()
    sector_list[1]
    return sp500_groupby, sector_list


def predict_sector(df, sector, date):
    '''
    Takes in the dataframe of industries by their daily closing market
    price, a list of sectors for all the industries, and a date that
    sections off training and test data. It will plot a linear
    regression model on top of day to day industry data. The linear
    regression is a machine learning model.
    '''
    fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(150, 150))
    count = 0
    for i in range(3):
        for j in range(4):
            if count < 11:
                data = df[df['Sector'] == sector[count]]
                data = data.drop(['Sector'], axis=1)
                data['date'] = pd.to_datetime(data['date'])

                # section off train and test data
                train = data[data['date'] <= date]
                test = data[data['date'] > date]

                # convert date time to float
                train['date'] = train['date'].apply(lambda v: v.toordinal())
                test['date'] = test['date'].apply(lambda v: v.toordinal())

                # Set x and y variables for linear regression
                X_train = train[['date']]
                y_train = train['close']
                X_test = test[['date']]
                y_test = test['close']

                # Linear Regression ML Model
                model = LinearRegression()
                model.fit(X_train, y_train)

                expected = y_test
                predicted = model.predict(X_test)
                mse = np.mean((predicted - expected)**2)

                # plot original sector data
                data['date'] = pd.to_datetime(data['date'])
                data['date'] = data['date'].apply(lambda v: v.toordinal())
                ax = sns.scatterplot(x='date', y='close',
                                     data=data, ax=axs[i, j])

                # plot ml line using linear regression
                line = Line2D(X_test, model.predict(X_test))
                ax.add_line(line)
                # Label Title and Axis
                ax.set_title(sector[count] + ' Sector data from 2013 - \
                             2018 combined with Linear Regression ML \
                             model from date ' + date, fontsize=30)
                ax.set_xlabel('Date in ordinal numbers, mse value ' +
                              str(mse), fontsize=30)
                ax.set_ylabel('Closing price daily of ' +
                              sector[count] + ' Sector', fontsize=30)

                count += 1


def main():
    tickers = pd.read_csv('sp500 companies and sectors.csv')
    sp_all = pd.read_csv('2013-2018/all_stocks_5yr.csv')
    pd.options.mode.chained_assignment = None  # default='warn'
    sp500_groupby, sector_list = prepare_sp_data(tickers, sp_all)
    predict_sector(sp500_groupby, sector_list, '2016-02-08')
    plt.savefig('ml_regression.png')


if __name__ == '__main__':
    main()
