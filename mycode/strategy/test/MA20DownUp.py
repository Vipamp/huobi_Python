'''
   @author: HeQingsong
   @date: 2019-11-28 17:48
   @filename: MacdCylinderDownUp.py
   @project: fin_quant
   @python version: 3.7 by Anaconda
   @description:

   todo 增加 ma 或者 macd 辅助选币
'''


class MA20DownUp:

    def __presolve__(self, df):
        """
        stock dataframe 数据预处理
        :param stock_df:
        :return:
        """
        df['yes1_close'] = df['close'].shift(1)
        df['yes2_close'] = df['close'].shift(2)
        df['yes3_close'] = df['close'].shift(3)

        df['yes1_ma_5'] = df['ma_5'].shift(1)

        df['yes1_volume'] = df['volume'].shift(1)
        df['yes2_volume'] = df['volume'].shift(2)
        df['yes3_volume'] = df['volume'].shift(3)

        df['cur_rate_3d'] = df['close'] / df['yes3_close'] - 1
        df['max_price_yes20'] = df['close'].shift(1).rolling(24).max()
        df['min_price_yes20'] = df['close'].shift(1).rolling(24).min()
        df = df.sort_values(by=['id'], axis=0, ascending=[False])
        df['tom_max_close_3d'] = df['high'].shift(1).rolling(3).max()
        df = df.sort_values(by=['id'], axis=0, ascending=[True])
        df['tom_rate_3d'] = df['tom_max_close_3d'] / df['close'] - 1
        return df

    def __buy_signal_judge__(self, row_values):
        yes1_volume = row_values['yes1_volume']
        yes2_volume = row_values['yes2_volume']
        yes3_volume = row_values['yes3_volume']
        cur_rate_3d = row_values['cur_rate_3d']
        cur_close = row_values['close']
        ma_5 = row_values['ma_5']
        yes1_ma_5 = row_values['yes1_ma_5']
        max_price_yes20 = row_values['max_price_yes20']
        min_price_yes20 = row_values['min_price_yes20']
        if yes1_volume > yes2_volume and yes2_volume > yes3_volume and cur_rate_3d > 0.03 and ma_5 > yes1_ma_5 and max_price_yes20 / min_price_yes20 < 1.1:
            return True
        return False
