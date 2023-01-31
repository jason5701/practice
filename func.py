import numpy as np

def buy_sell(signal, col1,col2):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1 # a flag for the trend upward/downward

  # loop through the length of the data set
  for i in range(0, len(signal)):
    # if obv > obv_ema and flag != 1 then buy else sell
    if signal[col1][i] > signal[col2][i] and flag != 1:
      sigPriceBuy.append(signal['Close'][i])
      sigPriceSell.append(np.nan)
      flag = 1

    #else if obv < obv_ema and flag != 0 then sell else buy
    elif signal[col1][i] < signal[col2][i] and flag != 0:
      sigPriceSell.append(signal['Close'][i])
      sigPriceBuy.append(np.nan)
      flag = 0

    #else obv == obv_ema so append NaN
    else:
      sigPriceBuy.append(np.nan)
      sigPriceSell.append(np.nan)

  return (sigPriceBuy, sigPriceSell)

# simple moving verage SMA
def SMA(data, period=30, column='Close'):
  return data[column].rolling(window=period).mean()

# exponential moving veratge, EMA
def EMA(data, period=20, column='Close'):
  return data[column].ewm(span=period, adjust=False).mean()

# MACD
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
  # fast moving average
  ShortEMA = EMA(data, period_short, column=column)

  # slow moving average
  LongEMA = EMA(data, period_long, column=column)

  # calculate moving average
  data['MACD'] = ShortEMA - LongEMA

  # calculate signals
  data['Signal_Line'] = EMA(data, period_signal, column='MACD')

  return data

# RSI
def RSI(data, period=14, column='Close'):
  delta = data[column].diff(1)
  delta = delta.dropna() # or delta[1:]

  up = delta.copy() # copy delta value
  down = delta.copy() # copy delta value

  up[up<0] = 0
  down[down>0]=0
  data['up']=up
  data['down']=down

  AVG_Gain = SMA(data, period, column='up')
  AVG_Loss = abs(SMA(data, period, column='down'))
  RS = AVG_Gain/AVG_Loss

  RSI = 100 - (100.0/(1.0+RS))
  data['RSI'] = RSI

  return data