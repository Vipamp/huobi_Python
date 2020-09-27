'''
   @author: HeQingsong
   @date: 2019-11-28 17:48
   @filename: MacdCylinderDownUp.py
   @project: fin_quant
   @python version: 3.7 by Anaconda
   @description:

   todo 增加 ma 或者 macd 辅助选币
'''
from huobi.constant import CandlestickInterval
from mycode.calc.QuotationDF import StockQuotationDF
from mycode.strategy.common import get_rate_list


class MA34TREND2:

    def __presolve__(self, df):
        """
        stock dataframe 数据预处理
        :param stock_df:
        :return:35
        """
        df = StockQuotationDF().builder(df).ma([13, 35, 55]).todf()
        df['yes1_ma_13'] = df['ma_13'].shift(1)
        df['yes2_ma_13'] = df['ma_13'].shift(2)
        df['yes3_ma_13'] = df['ma_13'].shift(3)
        df['yes4_ma_13'] = df['ma_13'].shift(4)
        df['yes5_ma_13'] = df['ma_13'].shift(5)

        df['yes1_ma_35'] = df['ma_35'].shift(1)
        df['yes2_ma_35'] = df['ma_35'].shift(2)
        df['yes3_ma_35'] = df['ma_35'].shift(3)
        df['yes4_ma_35'] = df['ma_35'].shift(4)
        df['yes5_ma_35'] = df['ma_35'].shift(5)

        df['yes1_ma_55'] = df['ma_55'].shift(1)
        df['yes2_ma_55'] = df['ma_55'].shift(2)
        df['yes3_ma_55'] = df['ma_55'].shift(3)
        df['yes4_ma_55'] = df['ma_55'].shift(4)
        df['yes5_ma_55'] = df['ma_55'].shift(5)

        df['yes1_close'] = df['close'].shift(1)
        df['yes2_close'] = df['close'].shift(2)
        df['tom1_close'] = df['close'].shift(-1)
        df['rate'] = df['tom1_close'] / df['close']

        df['yes1_volume'] = df['volume'].shift(1)

        df['yes50_min_ma_35'] = df['ma_35'].rolling(50).min()

        df = df.sort_values(by=['id'], axis=0, ascending=[False])
        df['future_rate'] = df['close'].shift(1).rolling(10).max() / df['close'] - 1
        df = df.sort_values(by=['id'], axis=0, ascending=[True])

        return df

    def __buy_signal_judge__(self, row_values):
        cur_ma_13 = row_values['ma_13']
        cur_ma_35 = row_values['ma_35']
        yes1_ma_13 = row_values['yes1_ma_13']
        yes2_ma_13 = row_values['yes2_ma_13']

        cur_ma_35 = row_values['ma_35']
        yes1_ma_35 = row_values['yes1_ma_35']
        yes2_ma_35 = row_values['yes2_ma_35']

        cur_ma_55 = row_values['ma_55']
        yes1_ma_55 = row_values['yes1_ma_55']
        yes2_ma_55 = row_values['yes2_ma_55']

        cur_close = row_values['close']
        yes1_close = row_values['yes1_close']
        yes2_close = row_values['yes2_close']

        yes1_volume = row_values['yes1_volume']
        cur_volume = row_values['volume']

        ma13fma35 = cur_ma_13 > cur_ma_35 and yes1_ma_13 < yes1_ma_35
        ma13up = cur_ma_13 > yes1_ma_13 > yes2_ma_13
        ma35up = cur_ma_35 > yes1_ma_35 > yes2_ma_35
        ma55up = cur_ma_55 > yes1_ma_55 > yes2_ma_55
        kfma13 = yes1_close < yes1_ma_13 and cur_close > yes1_ma_13
        if cur_close > yes1_close > yes2_close and cur_volume > yes1_volume:  # kfma13 and ma13up and ma35up and cur_ma_13 > cur_ma_35 and cur_close / yes1_close > 1.003:
            return True
        return False


# 13 金叉 35 日均线，55日均线向上。

if __name__ == '__main__':
    get_rate_list('MA34TREND2', 'btcusdt', wtime=CandlestickInterval.MIN15, size=1000)
