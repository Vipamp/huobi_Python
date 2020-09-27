'''
   @author: HeQingsong
   @date: 2020-09-20 13:41
   @filename: MarketQuotationUtils.py
   @project: huobi_Python
   @python version: 3.7 by Anaconda
   @description: 
'''
from huobi.client.market import MarketClient, CandlestickInterval
from huobi.exception.huobi_api_exception import HuobiApiException

import pandas as pd

market_client = MarketClient()

'''
返回格式：
[
    {'id': 1600581600, 'open': 0.005888, 'close': 0.005847, 'low': 0.005833, 'high': 0.005888, 'amount': 196284.1214, 'vol': 1147.6254458782, 'count': 55}, 
    {'id': 1600580700, 'open': 0.00588, 'close': 0.005873, 'low': 0.005873, 'high': 0.005916, 'amount': 83578.0374, 'vol': 492.5054534462, 'count': 45}, 
]
'''


def get_market_quotation(symbol, wtime, size=1000):
    try:
        list_obj = market_client.get_candlestick(symbol, wtime, size)
        df_list = []
        list_length = len(list_obj)
        for i in range(0, list_length):
            obj = list_obj[list_length - i - 1]
            df_list.append([obj.id, obj.open, obj.close, obj.low, obj.high, obj.amount, obj.vol, obj.count])
        df = pd.DataFrame(df_list, columns=['id', 'open', 'close', 'low', 'high', 'amount', 'volume', 'count'])
    except HuobiApiException:
        df = pd.DataFrame()
    return df


if __name__ == '__main__':
    df = get_market_quotation('btcusdt')
    print(df)
