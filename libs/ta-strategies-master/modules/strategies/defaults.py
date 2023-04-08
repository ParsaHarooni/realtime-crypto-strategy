import pandas as pd
import definitions

# this will replace by the time frame in the database
active_config = {
    "tf": "1D",
    "exchange": "Bitfinex",
    "symbol": "LUNA/USD",
}

# DataFrame
df_data = pd.read_csv(definitions.TEMP_DATA_PATH + "LUNA1-USD.csv")
# TimeFrame data
tf_data = pd.read_csv(definitions.TEMP_DATA_PATH + "us30-h1_M5.csv")

ZIGZAG_THRESH = [0.2 ,0.5 ,1.0 ,1.5 ,2.0 ,2.5 ,3.0 ,3.5 ,4.0 ,5.0 ,6.0 ,7.0 ,8.0 ,9.0 ,10]

RES_SUP_CHECKPOINTS = [0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]

SQUARE_ADD_SUB_NUMBERS = [0.25,0.50,0.75,1,1.25,1.50,1.75,2]

SQUARE_MULTI_DIV_NUMBERS = [10,100,1000,10_000]

DEFAULT_CANDLES = ["2crows",
"3blackcrows",
"3inside",
"3linestrike",
"3outside",
"3starsinsouth",
"3whitesoldiers",
"abandonedbaby",
"advanceblock",
"belthold",
"breakaway",
"closingmarubozu",
"concealbabyswall",
"counterattack",
"darkcloudcover",
"doji",
"dojistar",
"dragonflydoji",
"engulfing",
"eveningdojistar",
"eveningstar",
"gapsidesidewhite",
"gravestonedoji",
"hammer",
"hangingman",
"harami",
"haramicross",
"identical3crows",
"inside",
"invertedhammer",
"marubozu",
"morningdojistar",
"morningstar"
]

DEFAULT_MOMENTUMS = ['ao','cci','macd','rsi','stoch','stochrsi','tsi','willr']

DEFAULT_OVERLAP = ['ema','fwma','ichimoku','midpoint','midprice','sma','sinwma','wma','adx','aroon','atr','bbands','true_range','mfi']

# XMA(N-C)<PRICE
# TODO FIX 987,1597 MA NUMBERS (RETERN THE ACUAL DATA FRAME ITSELF INSTEAD OF THE SPECIFIC NUMBER)
STATIC_MOVINGS_MA_NUMBERS = [10,30,100,5,20,50,200,13,21,34,55,89,144,233,377,610]

# EMA(N[ema][i] - C) > SMA(N[sma][i] - C)
STATIC_EMA_HIGHER_SMA_DICT = {
    'ema':[5,12,12,13,21,34,55,89],
    'sma':[55,50,50,21,34,55,89,144]
}

# xMA(N[0] - C) > xMA(N[1] - C)
STATIC_MA_HIGHER_MA = [[10,20,50,100],[20,50,100,200]]

# xMA(N[0][i] - C) > xMA(N[1][i] - C) > xMA(N[2][i] - C)
STATIC_MA_HIGHER_MA_HIGHER_MA = [[10,20,50],[20,50,100],[50,100,200]]

# TSI(25-13-13 - tsi) > TSI(25-13-13 - signal) && TSI(25-13-13 - tsi)> N[I]
TSI_INPUTS = [-30,-20,-10]