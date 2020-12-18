# Analysis of S&P 500 from February 2013 to February 2018
### By Jacob Chan, Michael Chyan, Michael Mok

## Instructions:
* Run the ml_model.py file
* Run part_2_data_cleaning.py file

## Project Setup:
### Datasets

The [first dataset](https://www.kaggle.com/camnugent/sandp500) we are using is the historical stock prices from 2013 to 2018. It includes the open, high, low, close prices and volume for the day.

The [second dataset](https://datahub.io/core/s-and-p-500-companies-financials/r/1.html) we are using is to help us connect the industries and companies within the S&P 500, since our first dataset does not provide that. For our analysis we will mainly look at the top 250 companies to hopefully take account for companies that fall in and out of the S&P 500. (But we are open to ideas to work with this). This data set is from two years ago and we are mainly wanting the columns of industry and name of company to join to our other dataset.

This [dataset](https://www.kaggle.com/qks1lver/amex-nyse-nasdaq-stock-histories?) includes all historical data (up to 2019) from the NYSE, NASDAQ, and AmEx exchanges. With this information, we have a lot more historical data that can be used to evaluate performance in specific time periods of interest. In our case, we can compare current times with the 2008 housing financial crash.

This [dataset](https://finance.yahoo.com/quote/%5EGSPC/history?period1=1431561600&period2=1589414400&interval=1d&filter=history&frequency=1d) is for our personal interest because we wanted to extend our machine learning model all the way out to 2020 which is outside the scope of our main dataset. This required us to find another dataset to compare the overall trend of stocks in the S&P 500 to the S&P 500 index.

Our [final report](https://github.com/michaelchyan/CSE163/blob/master/Final%20Report.pdf) can be found here and is where we explain our findings.

### Libraries

In this project we used:
* pandas
* sklearn
* plotly
* datetime
* numpy
* matplotlib
* seaborn
* os
