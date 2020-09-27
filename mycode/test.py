'''
   @author: HeQingsong
   @date: 2020-09-19 21:18
   @filename: test.py
   @project: huobi_Python
   @python version: 3.7 by Anaconda
   @description: 
'''

from huobi.client.generic import GenericClient, CandlestickInterval
from huobi.client.market import MarketClient
from mycode.market import MarketQuotationUtils

generic_client = GenericClient()
market_client = MarketClient()


# def test(symbol):
#     list = MarketQuotationUtils.get_market_quotation(symbol, size=2)
#     if list != None and len(list) == 2:
#         cur = list[0]
#         last1 = list[1]
#         if last1.vol != 0 and cur.vol / last1.vol > 2 and cur.close / last1.close > 1.01:
#             print(symbol)
#
#
# if __name__ == '__main__':
#     symbol_list = BasicInfoUtils.get_all_symbol()
#     print(symbol_list)
#     for symbol in symbol_list:
#         if symbol[len(symbol) - 4:] == 'usdt':
#             test(symbol)

def test(symbol):
    list = MarketQuotationUtils.get_market_quotation(symbol, wtime=CandlestickInterval.MIN15, size=2000)
    if list != None and len(list) > 0:
        for i in range(5, len(list) - 2):
            cur = list[i]
            last1 = list[i + 1]
            last2 = list[i + 2]
            if last1.vol != 0 and cur.vol / last1.vol > 5 and last1.vol / last2.vol > 5 and cur.close / last1.close > 1.04:
                rate = max(list[i - 1].close, list[i - 2].close, list[i - 3].close) / cur.close - 1
                print("%s:%s:$d", symbol, i, rate)


if __name__ == '__main__':
    test('reqbtc')
    # symbol_list = BasicInfoUtils.get_all_symbol()
    # print(symbol_list)
    # for symbol in symbol_list:
    #     if symbol[len(symbol) - 4:] == 'usdt':
    #         test(symbol)
