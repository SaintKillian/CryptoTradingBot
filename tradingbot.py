from binance import Client
import pandas as pd
import time
from datetime import datetime
import re
import matplotlib.pyplot as plt

apiFolder = 'apiKey'
candle_names = ["Open time", "Open", "High", "Low", "Close", "Volume", "Kline Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume"]

# Returns a pandas dataframe for a symbol
#   start,end - str in the format  "1 Feb, 2022" or time in milliseconds 
#   interval Client.KLINE_INTERVAL_4HOUR
def getDataForTicker(client, symbol, interval, start, end):
    df = pd.DataFrame(client.get_historical_klines(symbol, interval, start, end))
    df.drop(11, axis=1, inplace=True) # remove useless column
    df.columns = candle_names
    df['Open time'] = df['Open time'].apply(lambda x : datetime.fromtimestamp(x/1000.0))
    for item in candle_names[1:]:
        df[item] = pd.to_numeric(df[item])
    return df

def displayDataFrame(df, short=12, long=24):
    plt.plot(df['Open time'], df['Close'], color='green')
    plt.plot(df['Open time'], df['Close'].rolling(long).mean(), color='red', label='EMA_Long')
    plt.plot(df['Open time'], df['Close'].rolling(short).mean(), color='blue', label='EMA_Short')
    plt.plot
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Get api keys
    with open(apiFolder) as f:
        for n, line in enumerate(f):
            if n == 0:
                api_key = re.match('public: (.*)', line).group(1)
            elif n == 1:
                api_secret = re.match('secret: (.*)', line).group(1)

    client = Client(api_key, api_secret) 
    df = getDataForTicker(client, "ETHUSDT", Client.KLINE_INTERVAL_1DAY, "1 Feb, 2022", str(time.time()*1000))
    print(df['Close'])
    displayDataFrame(df)