import os
import logging
from socket import create_connection
import time

from iqoptionapi.stable_api import IQ_Option
from config import Config

import pandas as pd
import schedule
import requests
import graph
import pandas as pd
import finplot as fplt
from back_test import Back_test

class Starter():
    def __init__(self):
        self.config = Config()
        self.username = self.config.get_connection_username()
        self.password = self.config.get_connection_password()
        self.api = IQ_Option(
            self.username,
            self.password
        )
    
    def create_connection(self):        
        try:
            check, reason = self.api.connect() # try to connect
        except Exception as e:
            print('Error: ', e)
        
        if check: # if initially connected
            print("Connection initialized.")         
            if self.api.check_connect == False: # if not currently connected
                print("Websocket did not respond.")
            else:
                print("Connection successful!")
            
        else:
            print("No response. Check your network and try again!")
        
        return check, reason
    
    def update_balance(self):
        self.api.connect()
        self.balance = self.api.get_balance() # get current balance
        return self.balance
    
    def change_balance_mode(self, balance_mode):
        self.api.change_balance(balance_mode)
        self.balance = self.api.get_balance()
        
        print(f"Changed balance to {balance_mode}. Balance is {self.balance}")
        
        return balance_mode, self.balance
    
    def check_open_markets(self):
        all_markets = self.api.get_all_open_time()
        current_open_markets = []
        actives_not_open = []

        for dirr in (['binary','turbo']):
            for symbol in all_markets[dirr]: 
                if all_markets[dirr][symbol]['open'] == True:
                    current_open_markets.append(symbol)

        for active in self.config.get_trade_actives():
            if active not in current_open_markets:
                actives_not_open.append(active)
        
        current_open_markets = list(set(self.config.get_trade_actives()) - set(actives_not_open))

        if actives_not_open:
            print(f"{actives_not_open}: {len(actives_not_open)} desired markets not open right now")
            print(f"{current_open_markets}: {len(current_open_markets)} desired markets open")
        else:
            print("All symbols open",self.actives)
        
        self.actives = current_open_markets
        if current_open_markets == []:
            print('Market closed for all actives')
            return None
        time.sleep(2)
        return self.actives
    
    def buy(self):
        self.api.connect() 
        self.api.buy(1000, "EURUSD", "call", 1)
        print("Buy Order Executed. Please wait for expiration...")
    
    def sell(self):
        self.api.connect()
        self.api.buy(1000, "EURUSD", "put", 1)
        print("Sell Order Executed. Please wait for expiration...")
        
class Strategy():
    def __init__(self):
        num = 1
        symbols = Config().get_trade_actives()
        intervals = ['1m'] #, '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d'
        for i in symbols:
            print(f'{num}. {i}')
            break
        index = int(input("Pick from the list of actives: "))
        self.symbol = f'{symbols[index - 1]}T'
        
        num = 1
        for i in intervals:
            print(f'{num}. {i}')
            break
        index = int(input("Pick a timeframe to trade on (minutes): "))
        
        print("Waiting for the next candle...")
        self.interval = intervals[index - 1]
        
    def strategy(self):
        
        url = 'https://www.binance.com/api/v3/klines?symbol=%s&interval=%s&limit=%s' % (self.symbol, self.interval, 1000)
        print('loading market data %s %s' % (self.symbol, self.interval))
        df = requests.get(url).json()
        df = pd.DataFrame(df)        

        df['MA20'] = df[4].rolling(2).mean()
        df['MA50'] = df[4].rolling(5).mean()

        df = df.dropna()

        df = df[['MA20', 'MA50']]
 
        print("running...")
        balance = Starter().update_balance

        if df.MA20.iloc[-1] > df.MA50.iloc[-1] \
        and df.MA20.iloc[-2] < df.MA50.iloc[-2]:
            Starter().buy()
            time.sleep(60)
            new_balance = Starter().update_balance()
            if new_balance > balance:
                status = "win"
                profit = new_balance - balance
            elif new_balance < balance:
                status = "loss"
                profit = new_balance - balance
            else:
                status = 'stalemate'
                profit = 0
            print(f"That was a {status}.\nProfit: {profit}.\nYour new balance is {balance}")
                
        elif df.MA20.iloc[-1] < df.MA50.iloc[-1] \
        and df.MA20.iloc[-2] > df.MA50.iloc[-2]:
            Starter().sell()
        
        """self.config = Config()
        self.api = IQ_Option(
            self.config.username,
            self.config.password
        )"""
        
    

    def start_strategy(self):
        while True:
            if time.strftime("%S") == "01":
                self.strategy()
                time.sleep(50)
                self.start_strategy()
        """self.strategy()
        schedule.every(60).seconds.do(self.strategy)
        
        while 1:
            schedule.run_pending()
            time.sleep(1)"""

def _create_starter():
    return Starter()

def message_prompt(message):
    answer = int(input(message + "\n1. View Graph\n2. Start Bot\n3. Backtest\n4. Exit\nEnter: "))
    if answer == 1:
        graph.create_graph()       
    elif answer == 2:
        print("Starting bot...")
        Strategy().start_strategy()
    elif answer == 4:
        quit()
    elif answer == 3:
        Back_test().view_back_test_charts()
    else:
        print("Invalid input")
        message = "\nLook at the available options. Einstein!\nWhat do you want to do?\nEnter: "
        message_prompt(message)
        

def start():
    MODE = ["PRACTICE", "REAL"]
    starter = _create_starter()
    starter.create_connection()
    starter.update_balance()
    balance_mode = int(input("Choose your balance mode (Pick a number):\n1. Practice\n2. Real\nEnter: "))
    if balance_mode == 2:
        print("Defaulted to Practice. I can't have you messing with my real account!")
    starter.change_balance_mode(MODE[0])
    starter.check_open_markets()
    message_prompt("What do you want to do?")
    #starter.buy()

app = start()

if __name__ == "__main__":
    app