'''
Jacob Chan, Michael Chyan, Michael Mok
CSE 163

This file cleans data and makes plots for the financial crisis.
'''
import pandas as pd
import os
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# Isolate 500 stocks in S&P 500

def clean_data():
    '''
    Cleans the sp500 companies and sectors dataset and joins it
    to the dataset with all stocks. Returns a tuple of a data
    frame and a dictonary of sectors.
    '''
    # Extract company tickers and sectors
    tickers = pd.read_csv('/CSE163/sp500 companies and sectors.csv')
    tickers_sectors = tickers[['Symbol', 'Sector']]

    # Create a dictionary for later use
    sector_dict = dict(zip(tickers_sectors.Symbol, tickers_sectors.Sector))

    # Join all company tickers with their sectors
    sp_all = pd.read_csv('/CSE163/2013-2018/all_stocks_5yr.csv')
    sp500_industry = tickers_sectors.merge(sp_all, left_on='Symbol',
                                           right_on='Name')
    sp500_industry = sp500_industry.drop(['Name', 'volume'], axis=1)
    sp500_industry.head(5)

    # Group companies by sectors sum their closing prices
    sp500_groupby = sp500_industry.groupby(['Sector', 'date'],
                                           as_index=False)['close'].sum()
    return sp500_groupby, sector_dict


# Financial Crisis Analysis
def financial_crisis(sector_dict):
    '''
    Takes in a dictionary of sectors and outputs a dictionary of data
    frames for each sector.
    '''
    df_dict = {}
    directory_name = '/CSE163/fh_20190420/full_history'
    for file_name in os.listdir(directory_name):
        if file_name.replace('.csv', '') in sector_dict:
            df = pd.read_csv(directory_name + '/' + file_name)
            df = df.drop(['volume'], axis=1)
            df['date'] = pd.to_datetime(df['date'])
            mask = (df['date'] > '2007-7-1') & (df['date'] <= '2011-7-1')
            df['sector'] = sector_dict[file_name.replace('.csv', '')]
            df = df.loc[mask]
            sector_name = sector_dict[file_name.replace('.csv', '')]
            if sector_name not in df_dict:
                df_dict[sector_name] = df.copy()
            else:
                df_dict[sector_name] = pd.concat((df_dict[sector_name], df))
                df_dict[sector_name] = df_dict[sector_name].groupby('date'). \
                    mean()
                df_dict[sector_name] = df_dict[sector_name].reset_index()
    return df_dict


def plot_industry(df_dict):
    '''
    Takes in a dictionary of dataframes. Graphs 11 plots of the adjusted
    closing price.
    '''
    for sector in df_dict:
        df_dict[sector].plot(x='date', y='adjclose', legend=False)
        plt.title(sector)
        plt.xlabel('Date')
        plt.ylabel('Adjusted Closing Price')
        plt.savefig()


def plot_candlestick_industry(df_dict):
    '''
    Takes in a dictionary of dataframes. Graphs 11  candlestick plots of
    the adjusted closing price.
    '''
    for sector in df_dict:
        fig = go.Figure(data=[go.Candlestick(x=df_dict[sector]['date'],
                        open=df_dict[sector]['open'],
                        high=df_dict[sector]['high'],
                        low=df_dict[sector]['low'],
                        close=df_dict[sector]['close'])])
        fig.update_layout(
            title=sector,
            xaxis_title='Date',
            yaxis_title='Adjusted Closing Price',
            xaxis_rangeslider_visible=False
        )
    fig.savefig()


def main():
    sp500_groupby, sector_dict = clean_data()
    df_dict = financial_crisis(sector_dict)
    plot_industry(df_dict)
    plot_candlestick_industry(df_dict)


if __name__ == '__main__':
    main()
