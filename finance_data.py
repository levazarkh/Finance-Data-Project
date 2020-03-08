from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns


start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)

# Bank of America
BAC = data.DataReader("BAC", 'yahoo', start, end)

# CitiGroup
C = data.DataReader("C", 'yahoo', start, end)

# Goldman Sachs
GS = data.DataReader("GS", 'yahoo', start, end)

# JPMorgan Chase
JPM = data.DataReader("JPM", 'yahoo', start, end)

# Morgan Stanley
MS = data.DataReader("MS", 'yahoo', start, end)

# Wells Fargo
WFC = data.DataReader("WFC", 'yahoo', start, end)

#creating a list of ticker symbols (as strings)
tickers = ['BAC', 'C', 'GS', 'JMP', 'MS', 'WFC']

#concatenating bank dataframes together to a single data frame
bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)

bank_stocks.columns.names = ['Bank Ticker','Stock Info']
print(bank_stocks.head())

#max closing stock price
bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()

#creating empty DataFrame 'returns'
returns = pd.DataFrame()

#getting returns for each bank
for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
print(returns.head())

#returns[1:]
sns.pairplot(returns[1:])
plt.show()

# Best Single Day Gain
# citigroup stock split in May 2011, but also JPM day after inauguration.
print(returns.idxmax())

print(returns.std()) # Citigroup riskiest

returns.ix['2015-01-01':'2015-12-31'].std() # Very similar risk profiles, but Morgan Stanley or BofA

#creating plot for Morgan Stanley returns
sns.distplot(returns.ix['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=100)
plt.show()

#creating plot for CitiGroup returns
sns.distplot(returns.ix['2008-01-01':'2008-12-31']['C Return'],color='red',bins=100)
plt.show()

#plot showing close price for each bank for the entire time
bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()
plt.show()

#plot for 30 day average against the close price for Bank of America's stock for 2008 year
plt.figure(figsize=(12,6))
BAC['Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].ix['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()
plt.show()

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)
plt.show()



