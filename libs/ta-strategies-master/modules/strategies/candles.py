from pandas import DataFrame

from modules.utils.df_utils import df_to_dict, df_to_json
from .defaults import DEFAULT_CANDLES

def cdls_to_json(df: DataFrame , names:list[str] = DEFAULT_CANDLES):
    import pandas_ta as ta
    # use all or selected cdl patterns
    cdls = df.ta.cdl_pattern(name=names)
    # convert to json
    to_return = df_to_json(cdls , list(df['Date']))

    return to_return

def cdls_to_dict(df: DataFrame , names:list[str] = DEFAULT_CANDLES):
    import pandas_ta as ta
    # use all or selected cdl patterns
    cdls = df.ta.cdl_pattern(name=names)
    # convert to json
    to_return = df_to_dict(cdls , list(df['Date']))

    return to_return