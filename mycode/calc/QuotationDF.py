'''
   @author: HeQingsong
   @date: 2019-11-25 23:38
   @filename: StockDF.py
   @project: fin_quant
   @python version: 3.7 by Anaconda
   @description:
    计算好的股票行情数据 dataframe 封装，dataframe列名如下：
    1. 基本信息：    ['name', 'open', 'close', 'high', 'low', 'volume', 'amount', 'rate', 'amplitude', 'turnover_rate']
    2. MACD 指标：  ['DIFF', 'DEA', 'middle', 'MACD', 'macd_cylinder']
    3. CCI 指标：   ['middle_14_sma', 'cci_14', 'middle_88_sma', 'cci_88']
    4. MA 指标：    ['ma_5' 'ma_10',  'ma_20', 'ma_30',  'ma_60', 'ma_120']
    5. 价格指标：   ['min_price_5', 'max_price_5', 'max_price_10', 'min_price_10','max_price_20', 'min_price_20','max_price_30', 'min_price_30','max_price_60', 'min_price_60','max_price_120', 'min_price_120']
    6. 交易量指标：  ['vol_5','max_vol_5', 'std_vol_5', 'vol_10', 'max_vol_10', 'std_vol_10', 'vol_20', 'max_vol_20', 'std_vol_20']
    7. 换手率指标： ['turnover_rate', 'avg_torate_5', 'avg_torate_10', 'avg_torate_20']
'''

import pandas as pd
from stockstats import StockDataFrame

from mycode.market.MarketQuotationUtils import get_market_quotation

calc_columns_format_dict = {
    'cci': 'cci_{period}',
    'kdj': 'kdjk',
    'macd': 'macd',
    'wr': 'wr_{period}'
}


class StockQuotationDF:
    stock_df = None

    def builder(self, stock_df):
        self.stock_df = StockDataFrame.retype(stock_df)
        return self

    def __base_calc(self, type, params_dict={}):
        column = calc_columns_format_dict[type].format_map(params_dict)
        self.stock_df[column]

    def cci(self, period_list):
        for period in period_list:
            self.__base_calc('cci', {'period': period})
        return self

    def kdj(self):
        self.__base_calc('kdj')
        return self

    def macd(self):
        self.__base_calc('macd')
        return self

    def ma(self, period_list):
        for ma in period_list:
            self.stock_df['ma_' + str(ma)] = self.stock_df['close'].rolling(ma).mean()
            self.stock_df['max_price_' + str(ma)] = self.stock_df['close'].rolling(ma).max()
            self.stock_df['min_price_' + str(ma)] = self.stock_df['close'].rolling(ma).min()
        return self

    def vol(self, period_list):
        for vol in period_list:
            self.stock_df['vol_' + str(vol)] = self.stock_df['volume'].rolling(vol).mean()
            self.stock_df['avg_vol_' + str(vol)] = self.stock_df['vol_' + str(vol)].rolling(vol).mean()
            self.stock_df['max_vol_' + str(vol)] = self.stock_df['volume'].rolling(vol).max()
            self.stock_df['min_vol_' + str(vol)] = self.stock_df['volume'].rolling(vol).min()
            self.stock_df['std_vol_' + str(vol)] = self.stock_df['vol_' + str(vol)] / self.stock_df[
                'avg_vol_' + str(vol)].rolling(vol).std()
        return self

    def todf(self):
        res_df = pd.DataFrame(self.stock_df)
        if 'macd' in res_df.columns:
            res_df.rename(columns={'macd': 'DIFF', 'macds': 'DEA'}, inplace=True)
            res_df['MACD'] = 2 * res_df['macdh']
            res_df = res_df.drop(['macdh'], axis=1)
            res_df['macd_cylinder'] = res_df['DIFF'] - res_df['DEA']
        res_df = res_df.fillna(0)
        return res_df


if __name__ == '__main__':
    stock_df = get_market_quotation('btcusdt')
    stock_df = StockQuotationDF().builder(stock_df).ma([5, 10, 20, 30, 60]).todf()
    print(stock_df)
