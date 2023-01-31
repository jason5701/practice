import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from func import MACD, RSI, SMA, EMA

plt.style.use('fivethirtyeight')

df = yf.download('068270.KS', start='2020-11-01', end='2023-01-30')
df['Date'] = df.index
# print(df.head())

df = MACD(df, period_long=26, period_short=12, period_signal=9)
df = RSI(df, period=14)
df['SMA'] = SMA(df, period=30)
df['EMA'] = EMA(df, period=20)
# print(df.tail())

column_list = ['MACD','Signal_Line']
df[column_list].plot(figsize=(12.2,6.4)) # plot the data
plt.title('MACD for CELTRION')
plt.ylabel('WON Price (won)')
# plt.show()

column_list = ['SMA','Close']
df[column_list].plot(figsize=(12.2,6.4))
plt.title('SMA for CELTRION')
plt.ylabel('WON Price (won)')
# plt.show()

column_list = ['EMA', 'CLose']
df[column_list].plot(figsize=(12.2,6.4))
plt.title('EMA for CELTRION')
plt.ylabel('WON Price (won)')

column_list = ['RSI']
df[column_list].plot(figsize=(12.2,6.4))
plt.title('RSI for CELTRION')
plt.ylabel('WON Price (won)')