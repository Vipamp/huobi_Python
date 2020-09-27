'''
   @author: HeQingsong
   @date: 2020-09-22 14:00
   @filename: common.py
   @project: huobi_Python
   @python version: 3.7 by Anaconda
   @description: 
'''
import math
import time

from huobi.constant import CandlestickInterval
from mycode.market.MarketQuotationUtils import get_market_quotation


def __strategy_obj(type, strategy_file_name):
    exec("from mycode.strategy.{type}.{strategy_file_name} import {strategy_file_name}".format(
        type=type, strategy_file_name=strategy_file_name))
    return eval(strategy_file_name + '()')


def get_buy_signal(type, strategy_name, quo_df):
    exchange_signal = []
    obj = __strategy_obj(type, strategy_name)
    quo_df = obj.__presolve__(quo_df)
    for row in quo_df.iterrows():
        if obj.__buy_signal_judge__(row[1]):
            exchange_signal.append(
                [time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(row[1]['id'])), row[1]['future_rate']])
    return exchange_signal


def get_rate_list(type, strategy_name, symbol, wtime=CandlestickInterval.MIN15, size=1000):
    stock_df = get_market_quotation(symbol, wtime, size)
    if stock_df.empty:
        return
    else:
        list = get_buy_signal(type, strategy_name, stock_df)
        sum_rate = 0
        for rate in list:
            sum_rate += rate[1] if not math.isnan(rate[1]) else 0
        print("symbol:{symbol}, sum_rate:{sum_rate} count:{count} avg rate:{avg_rate} rate list bellow!".format(
            symbol=symbol,
            count=len(list),
            sum_rate=sum_rate,
            avg_rate=sum_rate / max(len(list), 1))
        )
        for record in list:
            print(record)
