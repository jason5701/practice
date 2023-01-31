import matplotlib.pyplot as plt
import yfinance as yf
from func import buy_sell

plt.style.use('fivethirtyeight')

df = yf.download('068270.KS', start='2022-10-01', end='2023-01-30')
df['Date'] = df.index
# print(df.head())

plt.figure(figsize=(12.2,4.5)) # width = 12.2in, height = 4.5
plt.plot( df['Close'], label='Close') # plt.plot( X-Axis, Y-Axis, line_width, alpha_for_blending, label)
plt.xticks(rotation=45)
plt.title('Close Price History')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Price USD ($)', fontsize=18)
# plt.show()

OBV = []
OBV.append(0)
for i in range(1, len(df.Close)):
  # if the closing price is adove the prior close price
  if df.Close[i] > df.Close[i-1]:
    # then: current obv = previous obv + current volume
    OBV.append(OBV[-1] + df.Volume[i])
  elif df.Close[i] < df.Close[i-1]:
    OBV.append(OBV[-1] - df.Volume[i])
  else:
    OBV.append(OBV[-1])

# add obv column to pd.dataframe 
df['OBV'] = OBV

# calculate moving value
df['OBV_EMA'] = df['OBV'].ewm(com=20).mean()
# print(df)

plt.figure(figsize=(12.2,4.5)) # width = 12.2in, height = 4.5
plt.plot( df['OBV'], label='OBV', color='orange') # plt.plot( X-Axis, Y-Axis, line_width, alpha_for_blending, label)
plt.plot( df['OBV_EMA'], label='OBV_EMA', color='purple') # plt.plot( X-Axis, Y-Axis, line_width, alpha_for_blending, label)
plt.xticks(rotation=45)
plt.title('OBV/OBV_EMA')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Price USD ($)', fontsize=18)
# plt.show()

x = buy_sell(df, 'OBV','OBV_EMA')
df['Buy_Signal_Price'] = x[0]
df['Sell_Signal_Price'] = x[1]

plt.figure(figsize=(12.2,4.5))
plt.scatter( df.index, df['Buy_Signal_Price'], label='Buy_signal', marker='^',color='green', alpha=1)
plt.scatter( df.index, df['Sell_Signal_Price'],label='Sell_signal', marker='v',color='red', alpha=1)
plt.plot( df['Close'], label='Colse Price', alpha = 0.35)
plt.xticks(rotation=45)
plt.title('the stock buy / sell signals')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Price USD ($)', fontsize=18)
plt.legend(loc='upper left')
plt.show()