from pandas import DataFrame
from modules.strategies.defaults import STATIC_MOVINGS_MA_NUMBERS


def get_default_movings(indicator_name :str , indicator_fn):
    import pandas as pd
    import pandas_ta as ta
    from modules.strategies.defaults import STATIC_MOVINGS_MA_NUMBERS

    df = pd.DataFrame()
    for n in STATIC_MOVINGS_MA_NUMBERS:
        name = indicator_name
        df[name] = indicator_fn(n)
    
    return df


def get_last_ma(number:int , df_data:DataFrame , ma_fn:any):
    from copy import copy
    import pandas as pd
    import pandas_ta as ta
    
    df_data = copy(df_data) # make a copy of the data frame
    # close_price = df_data.iloc[-1,4] # last row of the closing price

    return ma_fn(number).iloc[-1]

def all_static_ma_to_list(df_data:DataFrame ,ma_fn:any , numbers:list[int] = STATIC_MOVINGS_MA_NUMBERS):
    from copy import copy
    ma_list = list(map(lambda num: get_last_ma(num,df_data,ma_fn)  , numbers))
    return ma_list

def all_static_ma_to_new_df(df_data:DataFrame ,ma_fn:any , symbol:str):
    import pandas as pd
    
    columns = list(map(lambda num: symbol + 'MA_' + str(num) , STATIC_MOVINGS_MA_NUMBERS))
    ma_list = all_static_ma_to_list(df_data,ma_fn)
    
    data = list(map(lambda ma: [ma] ,ma_list))
    
    # {x : [1]}
    df_dict = dict(zip(columns , data))

    df = pd.DataFrame(df_dict)
    
    return df

def list_of_ma_lower_than_price(open_price :int ,ma_list :list):
    to_return = list(map(lambda ma: ma < open_price ,ma_list))
    return to_return

def dict_of_ma_status(df_data:DataFrame , ma_nested_list:list[list]):
    open_price = df_data.iloc[-1,1]

    sma_list = ma_nested_list[0]
    ema_list = ma_nested_list[1]
    wma_list = ma_nested_list[2]

    # ma lower than open price
    sma_status = list_of_ma_lower_than_price(open_price,sma_list)
    ema_status = list_of_ma_lower_than_price(open_price,ema_list)
    wma_status = list_of_ma_lower_than_price(open_price,wma_list)

    return {
        'SMA':sma_status,
        'EMA':ema_status,
        'WMA':wma_status
    }


# EMA(N[0] - C) > SMA(N[1] - C)
def list_of_ema_higher_sma_stat(df_data:DataFrame):
    from modules.strategies.defaults import STATIC_EMA_HIGHER_SMA_DICT

    ema_list = all_static_ma_to_list(df_data,df_data.ta.ema,STATIC_EMA_HIGHER_SMA_DICT['ema'])
    sma_list = all_static_ma_to_list(df_data,df_data.ta.sma,STATIC_EMA_HIGHER_SMA_DICT['sma'])

    status = list(map(lambda ema,sma: ema > sma ,ema_list,sma_list))
    return status

def list_of_xma_higher_xma(ma_fn :any):
    from modules.strategies import df_data
    from modules.strategies.defaults import STATIC_MA_HIGHER_MA

    ma0_list = all_static_ma_to_list(df_data,ma_fn,STATIC_MA_HIGHER_MA[0])
    ma1_list = all_static_ma_to_list(df_data,ma_fn,STATIC_MA_HIGHER_MA[1])

    status = list(map(lambda ma1,ma2: ma1 > ma2 ,ma0_list,ma1_list))
    return status

def list_of_xma_higher_xma_higher_xma(ma_fn :any):
    from modules.strategies import df_data
    from modules.strategies.defaults import STATIC_MA_HIGHER_MA_HIGHER_MA

    ma0_list = all_static_ma_to_list(df_data,ma_fn,STATIC_MA_HIGHER_MA_HIGHER_MA[0])
    ma1_list = all_static_ma_to_list(df_data,ma_fn,STATIC_MA_HIGHER_MA_HIGHER_MA[1])
    ma2_list = all_static_ma_to_list(df_data,ma_fn,STATIC_MA_HIGHER_MA_HIGHER_MA[2])

    status = list(map(lambda ma1,ma2,ma3: ma1 > ma2 > ma3 ,ma0_list,ma1_list,ma2_list))
    return status