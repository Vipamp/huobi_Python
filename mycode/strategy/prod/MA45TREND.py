'''
   @author: HeQingsong
   @date: 2019-11-28 17:48
   @filename: MacdCylinderDownUp.py
   @project: fin_quant
   @python version: 3.7 by Anaconda
   @description:
     使用 45 周期均线，判断上升拐头，进而判断趋势性买点，适用于小币，对于 BTC 这种大币不适用。

   todo 测试卖点策略，应该是在 45 周期均线出现下降拐头时，待验证
'''
from huobi.constant import CandlestickInterval
from mycode.calc.QuotationDF import StockQuotationDF
from mycode.strategy.common import get_rate_list


class MA45TREND:

    def __presolve__(self, df):
        """
        stock dataframe 数据预处理
        :param stock_df:
        :return:
        """
        df = StockQuotationDF().builder(df).ma([45]).todf()
        df['yes1_ma_45'] = df['ma_45'].shift(1)
        df['yes2_ma_45'] = df['ma_45'].shift(2)
        df['yes3_ma_45'] = df['ma_45'].shift(3)
        df['yes4_ma_45'] = df['ma_45'].shift(4)
        df['yes5_ma_45'] = df['ma_45'].shift(5)

        df['yes50_min_ma_45'] = df['ma_45'].rolling(45).min()

        df = df.sort_values(by=['id'], axis=0, ascending=[False])
        df['tom_max_close_5'] = df['close'].shift(1).rolling(50).max()
        df['tom_min_close_5'] = df['close'].shift(1).rolling(50).min()
        df = df.sort_values(by=['id'], axis=0, ascending=[True])
        df['future_rate'] = df['tom_max_close_5'] / df['close'] - 1
        return df

    def __buy_signal_judge__(self, row_values):
        cur_close = row_values['close']
        cur_ma_45 = row_values['ma_45']
        yes1_ma_45 = row_values['yes1_ma_45']
        yes2_ma_45 = row_values['yes2_ma_45']
        yes3_ma_45 = row_values['yes3_ma_45']
        yes4_ma_45 = row_values['yes4_ma_45']
        yes5_ma_45 = row_values['yes5_ma_45']

        if cur_ma_45 > yes1_ma_45 * 1.0003 > yes2_ma_45 * 1.00000009 > yes3_ma_45 * 1.000000000027 > yes4_ma_45 * 1.0000000000000081 \
                and yes4_ma_45 < yes5_ma_45 \
                and cur_close / cur_ma_45 < 1.05:
            return True
        return False


if __name__ == '__main__':
    get_rate_list('prod', 'MA45TREND', 'ringusdt', wtime=CandlestickInterval.MIN15, size=1000)
