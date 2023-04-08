from copy import copy
from operator import le
from pandas import DataFrame

def df_to_json(df:DataFrame , dates:list = None):
    import json

    # split it to arrays for a better performance
    res = df.to_json(orient="split")

    # add dates list to the json data
    parsed = json.loads(res)
    if(dates): parsed['dates'] = dates 

    to_return = json.dumps(parsed, indent=4)
    return to_return


def df_to_dict(df:DataFrame , dates:list = None):
    import json

    # split it to arrays for a better performance
    res = df.to_dict(orient="split")

    # add dates list to the json data
    if(dates): res['dates'] = dates 

    return res

def copy_main_df_data(df_data:DataFrame):
    
    return copy(df_data)