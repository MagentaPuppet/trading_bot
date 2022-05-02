#!/usr/bin/env python3
#analyze2.py
import finplot as fplt
import numpy as np
import pandas as pd
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

class Back_test:
    def __init__(self):
        pass
    
    def view_back_test_charts(self):
        start_date = '2019-01-01'
        df = yf.download('BTC-USD', start=start_date)

        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()

        df = df.dropna()

        df_open_close = df[['Open', 'Close', 'MA20', 'MA50']]
        df = df[['Close', 'MA20', 'MA50']]

        Buy = []
        Sell = []
        win_buy = [] 
        lose_buy = []
        neither_buy = [] 
        win_sell = []
        lose_sell = []
        neither_sell = []
        index_win_buy = [] 
        index_lose_buy = []
        index_neither_buy = [] 
        index_win_sell = []
        index_lose_sell = []
        index_neither_sell = []
        profit = 0
        
        for i in range(len(df)):
            if df.MA20.iloc[i] > df.MA50.iloc[i] \
            and df.MA20.iloc[i-1] < df.MA50.iloc[i-1]:
                Buy.append(i)
                if df_open_close.Close.iloc[i] > df_open_close.Open.iloc[i]:
                    win_buy.append(df_open_close.Close.iloc[i])
                    index_win_buy.append(i)
                    profit += 1
                elif df_open_close.Close.iloc[i] < df_open_close.Open.iloc[i]:
                    lose_buy.append(df_open_close.Close.iloc[i])
                    index_lose_buy.append(i)
                    profit -= 1
                else:
                    neither_buy.append(df_open_close.Close.iloc[i])
                    index_neither_buy.append(i)
            elif df.MA20.iloc[i] < df.MA50.iloc[i] \
            and df.MA20.iloc[i-1] > df.MA50.iloc[i-1]:
                Sell.append(i) 
                if df_open_close.Close.iloc[i] < df_open_close.Open.iloc[i]:
                    win_sell.append(df_open_close.Close.iloc[i])
                    index_win_sell.append(i)
                    profit += 1
                elif df_open_close.Close.iloc[i] > df_open_close.Open.iloc[i]:
                    lose_sell.append(df_open_close.Close.iloc[i])
                    index_lose_sell.append(i)
                    profit -= 1
                else:
                    neither_sell.append(df_open_close.Close.iloc[i])   
                    index_neither_sell.append(i)
        
        
        
        
        plt.figure(figsize = (20, 5))        
        plt.plot(df['Close'], label = 'Asset price', c = 'blue', alpha = 0.5)
        plt.plot(df['MA20'], label = 'MA20', c = 'k', alpha = 0.9)
        plt.plot(df['MA50'], label = 'MA50', c = 'magenta', alpha = 0.9)
        plt.scatter(df.iloc[index_win_buy].index, win_buy, marker = '^', color = 'g', s = 100)
        plt.scatter(df.iloc[index_lose_buy].index, lose_buy, marker = '^', color = 'r', s = 100)
        plt.scatter(df.iloc[index_neither_buy].index, neither_buy, marker = '^', color = 'magenta', s = 100)
        plt.scatter(df.iloc[index_win_sell].index, win_sell, marker = 'v', color = 'g', s = 100)
        plt.scatter(df.iloc[index_lose_sell].index, lose_sell, marker = 'v', color = 'r', s = 100)
        plt.scatter(df.iloc[index_neither_sell].index, neither_sell, marker = 'v', color = 'magenta', s = 100)
        plt.legend()
        print(f'From {start_date} to today {date.today()}, you would have had {(profit/len(Buy))*100} % in profit')
        if profit == 0:
            print("At least you wouldn't have lost money!")
        elif profit > 0:
            print("You could have been rich!")
        else:
            print("You dodged a bullet there, didn't you?")
        plt.show()
    
if __name__ == "__main__":
    pass