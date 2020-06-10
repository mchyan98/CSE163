# -*- coding: utf-8 -*-
"""MachineLearningModel

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10oAg_48clLQmGuRp9vs7xiQsR9Sf_53b
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import os
import sklearn
import plotly.graph_objects as go
from datetime import datetime
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns

#Isolate 500 stocks in S&P 500
tickers = pd.read_csv('/content/drive/My Drive/CSE163 Final Project/CSE163/sp500 companies and sectors.csv')
tickers_sectors = tickers[['Symbol', 'Sector']]
tickers_sectors.head(5)

# Merges industry and day prices for S&P 500 stocks

sp_all = pd.read_csv('/content/drive/My Drive/CSE163 Final Project/CSE163/2013-2018/all_stocks_5yr.csv')
sp500_industry = tickers_sectors.merge(sp_all, left_on='Symbol', right_on='Name')
sp500_industry = sp500_industry.drop(['Name', 'volume'], axis=1)
sp500_industry.head(5)
sp500_groupby = sp500_industry.groupby(['Sector', 'date'], as_index=False)['close'].sum()
industries = sp500_industry.groupby('Sector')['close'].sum()
industries
sector_list = industries.index.tolist()
sector_list[1]
len(sector_list)

pd.options.mode.chained_assignment = None  # default='warn'
predict_sector(sp500_groupby, sector_list, '2016-02-08')

# function
def predict_sector(df, sector, date):
  fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(150,150))
  # plt.subplots_adjust(wspace=1)
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
        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(X_train, y_train)
        
        #print(model)
        expected = y_test
        predicted = model.predict(X_test)
        mse = np.mean((predicted - expected)**2)
        
        # plot original sector data 
        sns.set() 
        data['date'] = pd.to_datetime(data['date'])
        data['date'] = data['date'].apply(lambda v: v.toordinal())
        ax = sns.scatterplot(x='date', y='close', data=data, ax=axs[i,j])
        
        # plot ml line using linear regression
        line = Line2D(X_test, model.predict(X_test))
        ax.add_line(line)
        # Label Title and Axis
        ax.set_title(sector[count] + ' Sector data from 2013 - 2018 combined with Linear Regression ML model from date ' + date, fontsize=30)
        ax.set_xlabel('Date in ordinal numbers, mse value ' + str(mse), fontsize=30)
        ax.set_ylabel('Closing price daily of ' + sector[count] + ' Sector', fontsize=30)

        count += 1

