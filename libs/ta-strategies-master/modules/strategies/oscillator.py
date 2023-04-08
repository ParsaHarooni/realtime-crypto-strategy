from functools import partial
from copy import copy
import pandas as pd
import pandas_ta as ta

from . import defaults
from modules.utils.df_utils import copy_main_df_data

DataFrame = pd.DataFrame

"""
Rsi(14-c)>30 
Cci(20-c)>-100
Mfi(14-c)>20
Willr(14-c) >-80
Ao(c)>0

***

RSI(14-C)>50

Cci(20-c)>-50

"""


def get_rsi(df: DataFrame, length: int):
    return df.ta.rsi(length=length)


rsi_length_14 = partial(get_rsi, length=14)


def rsi_higher_n(df_data: DataFrame, n: int = 30, length: int = 14):
    df = copy_main_df_data(df_data)
    res = get_rsi(df_data, length)
    res = res.iloc[-1]

    return res > n


def get_cci(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.cci(length=20)


def cci_higher_n(df_data: DataFrame, n: int = 100, df_input: int = 20):
    df = copy_main_df_data(df_data)
    res = df.ta.cci(df_input).iloc[-1]

    return res > n


def mfi_higher_n(df_data: DataFrame, n: int = 20, df_input: int = 14):
    df = copy_main_df_data(df_data)
    res = df.ta.mfi(length=df_input).iloc[-1]

    return res > n


def get_willr(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.willr(length=14)


def willr_higher_n(df_data: DataFrame, n: int = -80, df_input: int = 14):
    df = copy_main_df_data(df_data)
    res = df.ta.willr(df_input).iloc[-1]

    return res > n


def ao_higher_n(df_data: DataFrame, n: int = 0):
    df = copy_main_df_data(df_data)
    res = df.ta.ao(fast=5, slow=34).iloc[-1]
    return res > n


"""

 TSI(25-13-13 - tsi) > TSI(25-13-13 - signal) && TSI(25-13-13 - tsi)> N[I]

"""


def get_tsi(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.tsi(fast=25, slow=13, signal=13)


def tsi_higher_n(df_data: DataFrame, tsi: any = 0, signal: any = 0, n: int = 0):
    # df = copy_main_df_data(df_data)

    # res = df.ta.tsi(25 , 13 , 13 , tsi) > df.ta.tsi(25 , 13 , 13 , signal)
    # final = df.ta.tsi(25 , 13 , 13 , tsi) > n

    return get_tsi(df_data)


def tsi_higher_n_list(
    tsi: any = 0, signal: any = 0, n_list: list[int] = defaults.TSI_INPUTS
):
    to_return = list(map(lambda n: tsi_higher_n(tsi, signal, n), n_list))
    return to_return


"""

AROON(15 - aroon up) > AROON(15 - aroon down) 

"""


def get_aroon(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.aroon(length=20)


def aroon_higher_aroon(
    df_data: DataFrame, aroon_up: int, aroon_down: int, numbers: list[int] = [15, 15]
):
    df = copy_main_df_data(df_data)
    res = df.ta.aroon(15, aroon_up) > df.ta.aroon(15, aroon_down)
    return res


"""


ADX(14-20 - di+) > ADX(14-20 - di-) && ADX(14-20)>25

"""


def get_adx(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.adx(length=14, lensig=20)


def adx_higer_n(df_data: DataFrame, plus_di: int, neg_di: int, n: int = 25):
    df = copy_main_df_data(df_data)
    adx = df.ta.adx(14, 20, plus_di) > df.ta.adx(14, 20, neg_di)
    res = adx and df.ta.adx(14, 20) > n
    return res


"""
Stoch(14- k =3 ) > stoch(14 - d =3 ) && stoch(14)>20

"""

# TODO https://github.com/mrjbq7/ta-lib/issues/502
def get_stoch(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.stoch()


def get_stoch_rsi(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.stochrsi(length=14, rsi_length=14, k=3, d=3)


def stoch_higer_n(df_data: DataFrame, n: int = 20):
    df = copy_main_df_data(df_data)
    stoch = df.ta.stoch(14, k=3) > df.ta.stoch(14, d=3) and df.ta.stoch(14) > n
    return stoch


"""
Stoch RSI ( 14 - 14 -  k = 3)  > Stoch RSI( 14 - 14 - d = 3 ) && stoch(14 - 14)>20

"""


def stoch_rsi_higer_n(df_data: DataFrame, n: int = 20):
    df = copy_main_df_data(df_data)
    stoch = (
        df.ta.stochrsi(14, 14, k=3) > df.ta.stochrsi(14, 14, d=3)
        and df.ta.stoch(14, 14) > n
    )
    return stoch


"""
M.A.C.D(12-26-9 - SIGNAL) > M.A.C.D(12-26-9 MACD) && M.A.C.D(12-26-9 - MACD)>0

"""


def get_macd(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.macd(fast=12, slow=26, signal=9)


def macd_status(df_data: DataFrame, signal, macd, n: int = 0):
    df = copy_main_df_data(df_data)
    macd = (
        df.ta.macd(12, 26, 9, signal=signal) > df.ta.macd(12, 26, 9)
        and df.ta.macd(12, 26, 9, signal=signal) > n
    )
    return macd


"""
M.A.C.D(12-26-9 - MACD)>0

"""


def macd_higher_n(df_data: DataFrame, macd, n: int = 0):
    df = copy_main_df_data(df_data)
    macd = df.ta.macd(12, 26, 9, macd) > n
    return macd


"""
BBANDS(20-2-0 - basis) < PRICE
"""


def get_bbands(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.bbands(length=20, std=2, ddof=0)


def bbands(df_data: DataFrame, basis, price):
    df = copy_main_df_data(df_data)
    bbands = df.ta.bbands(20, 2, 0, basis) < price
    return bbands


def get_ichimoku(df_data: DataFrame):
    df = copy_main_df_data(df_data)
    return df.ta.ichimoku(tenkan=9, kijun=26, include_chikou=True, senkou=52)


def ichimoku_stats(
    price: float, span_a: float, span_b: float, cnv_line: float, b_line: float
):
    """
    Ichimoku(9-26-52-26 - span a) > Ichimoku(9-26-52-26 - span B) &&  Ichimoku(9-26-52-26 - span a)<price
    Ichimoku(9-26-52-26 - span a) < Ichimoku(9-26-52-26 - span B) &&  Ichimoku(9-26-52-26 - span b)<price

    Ichimoku(9-26-52-26 - span a) < Ichimoku(9-26-52-26 - span B) && Ichimoku(9-26-52-26 - base line) > price
    Ichimoku(9-26-52-26 - span a) > Ichimoku(9-26-52-26 - span B) && Ichimoku(9-26-52-26 - base line) > price

    Ichimoku(9-26-52-26 - span a) < Ichimoku(9-26-52-26 - span B) && Ichimoku(9-26-52-26 - span b) > price

    Ichimoku(9-26-52-26 - span a) > Ichimoku(9-26-52-26 - span B) && Ichimoku(9-26-52-26 - conversion line) > price

    Ichimoku(9-26-52-26 - span a) < Ichimoku(9-26-52-26 - span B) && Ichimoku(9-26-52-26 - conversion line) > Ichimoku(9-26-52-26 - base line)

    Ichimoku(9-26-52-1 - span A) > Ichimoku(9-26-52-1 - span B)

    Ichimoku(9-26-52-1 - span A) < Ichimoku(9-26-52-1 - span B)  && Ichimoku(9-26-52-1 - base line) < PRICE


    """

    formula = []

    formula.append(span_a > span_b and span_a < price)
    formula.append(span_a < span_b and span_a < price)

    formula.append(span_a < span_b and b_line > price)
    formula.append(span_a > span_b and b_line > price)

    formula.append(span_a < span_b and span_b > price)

    formula.append(span_a > span_b and cnv_line > price)

    formula.append(span_a < span_b and cnv_line > b_line)

    formula.append(span_a < span_b)

    formula.append(span_a < span_b and b_line < price)

    return formula


"""

Cci(20-c)>0EMA(100-C)<PRICE && RSI(14-C)>50

EMA(56-C) < EMA(11-C) && EMA(26-C)< EMA(11-C)

50<Rsi(14-c)>20  && M.A.C.D(12-26-9 - SIGNAL) > M.A.C.D(12-26-9 - MACD(histogeram) )


"""


def get_all_oscills(df_data: DataFrame):
    toReturn = []

    toReturn.append(rsi_higher_n(df_data))
    toReturn.append(cci_higher_n(df_data))
    toReturn.append(mfi_higher_n(df_data))
    toReturn.append(willr_higher_n(df_data))
    toReturn.append(ao_higher_n(df_data))
    toReturn.append(ao_higher_n(df_data))
    # toReturn.append(tsi_higher_n_list(df_data))

    return toReturn
