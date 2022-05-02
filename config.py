from numpy import loadtxt
from functools import cache

class Config:
    def __init__(self):
        pass
    
    def get_connection_username(self):
        username = loadtxt('config.txt', dtype='str')[0]
        return username
    
    def get_connection_password(self):
        password = loadtxt('config.txt', dtype='str')[1]
        return password
    
    def get_trade_actives(self):
        desired_actives = loadtxt('desired_actives.txt', dtype='str')
        return desired_actives