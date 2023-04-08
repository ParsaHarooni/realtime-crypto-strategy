# Core modules
import time
import copy
from functools import partial

# 3rd party modules
import pandas as pd
import pandas_ta as ta

# Local Modules
import modules.utils as utils
import modules.strategies.zigzag as zigzag
import modules.strategies.movings as movings
import modules.strategies.defaults as defaults
import modules.strategies.oscillator as oscillator
import modules.strategies.divergence as divergence
import modules.strategies.SquareOfNine as nine_sqr
import modules.strategies.ResistantNSupport as rs

# import modules.strategies.HarmonicPatterns as hp

# Check for time taken to run the script
start_time = time.time()

# *Strategy Notif
init_notif = partial(utils.set_notif, configs=defaults.active_config)

df_data = defaults.df_data
# basic indicators defined in defaults.py
df_base_inds = copy.copy(df_data)
# *default momentums and overlaps
ta_list = map(
    lambda i: {"kind": i}, defaults.DEFAULT_MOMENTUMS + defaults.DEFAULT_OVERLAP
)
ta_list = list(ta_list)
# *Create the main Strategy
MainStrategy = ta.Strategy(name="DEFS_INDS", ta=ta_list)

# Run the main Strategy
df_base_inds.ta.strategy(MainStrategy)
# Candles Strategy
df_cdls = copy.copy(df_data)
df_cdls = df_cdls.ta.cdl_pattern(name=defaults.DEFAULT_CANDLES)
# Static MA
df_sma = movings.all_static_ma_to_new_df(df_data, df_data.ta.sma, "S")
df_ema = movings.all_static_ma_to_new_df(df_data, df_data.ta.ema, "E")
df_wma = movings.all_static_ma_to_new_df(df_data, df_data.ta.wma, "W")
df_all_static_ma = pd.concat([df_sma, df_ema, df_wma], ignore_index=True)
# Concatenate all indicators in to one data frame
df_final = pd.concat([df_base_inds, df_cdls, df_all_static_ma], ignore_index=True)
# only save last 50 row
df_final = df_final.iloc[-50:]
# Check All MA are lower than open price
sma_list = df_sma.values[0]
ema_list = df_ema.values[0]
wma_list = df_wma.values[0]
ma_status = movings.dict_of_ma_status(df_data, [sma_list, ema_list, wma_list])
# *ZigZag threshs
close_prices = df_data["Close"]


def map_threshs(thresh: int, df: pd.DataFrame = df_data, column: str = "Close"):
    # x = df[column]
    pivots = zigzag.peak_valley_pivots(close_prices.values, thresh, -thresh)
    return list(pivots)


# OutPut : {cols:ZIGZAG_THRESH,data:[[],[],[]]}
pivots = map(lambda n: map_threshs(n), defaults.ZIGZAG_THRESH)
pivots = list(pivots)
# TODO: USE DATAFRAME INSTEAD OF DICT
pivots = {"columns": defaults.ZIGZAG_THRESH, "data": pivots}
# Last 2 Peaks of each pivots by defaults.ZIGZAG_THRESH
peaks_indicies = list(
    map(lambda pivot: zigzag.get_peaks_indices(pivot), pivots["data"])
)
last_2_peaks = list(map(lambda p: p[-2:], peaks_indicies))
# Last 2 Valleys of each pivots by defaults.ZIGZAG_THRESH
valleys_indicies = list(
    map(lambda pivot: zigzag.get_valleys_indices(pivot), pivots["data"])
)
last_2_valleys = list(map(lambda v: v[-2:], valleys_indicies))
# Store peaks N valleys on pivots object
pivots.update(
    {
        "last_peaks_index": last_2_peaks,
        "last_valleys_index": last_2_valleys,
    }
)
# *Peak +1
# *Valley -1
rsi_len14 = oscillator.rsi_length_14(df_data)
# !! use only 1 column to get peaks N valleys
# MACD_12_26_9
macd = oscillator.get_macd(df_data)
macd = macd["MACD_12_26_9"]
# STOCHk_14_3_3
stoch = oscillator.get_stoch(df_data)
stoch = stoch["STOCHd_14_3_3"]


# TODO:USE MAP INSTEAD OF FORLOOP
# TODO:CHECK STOCH,RSI AND MACD LIST LENGth BEFOR peaks N valleys MAP
# Add peak's price to the pivots dict
prices_list = []
rsi_len14_list = []
macd_list = []
stoch_list = []
for idx, peak in enumerate(pivots["last_peaks_index"]):
    valley_len = len(peak)
    # ignore if peak is [0]
    if valley_len != 1 and peak[0] != 0:
        price_first = close_prices[peak[0]]
        price_last = close_prices[peak[1]]

        rsi_first = rsi_len14.iloc[peak[0]]
        rsi_last = rsi_len14.iloc[peak[1]]

        # !! USE 1D LIST
        macd_list.append([macd.iloc[peak[0]], macd.iloc[peak[1]]])
        # stoch_list.append([stoch.iloc[peak[0]], stoch.iloc[peak[1]]])

        prices_list.append([price_first, price_last])
        rsi_len14_list.append([rsi_first, rsi_last])
pivots.update(
    {
        "peaks_price_points": prices_list,
        "rsi14_peaks_points": rsi_len14_list,
        "macd_peaks_points": macd_list,
        "stoch_peaks_points": stoch_list,
    }
)

# Add valley's price to the pivots dict
prices_list = []
rsi_len14_list = []
macd_list = []
stoch_list = []
for idx, valley in enumerate(pivots["last_valleys_index"]):
    valley_len = len(valley)
    # ignore if valley is [0]
    if valley_len != 1 and valley[0] != 0:
        price_first = close_prices[valley[0]]
        price_last = close_prices[valley[1]]

        rsi_first = rsi_len14.iloc[valley[0]]
        rsi_last = rsi_len14.iloc[valley[1]]

        macd_list.append([macd.iloc[valley[0]], macd.iloc[valley[1]]])
        # stoch_list.append([stoch.iloc[valley[0]], stoch.iloc[valley[1]]])

        prices_list.append([price_first, price_last])
        rsi_len14_list.append([rsi_first, rsi_last])
pivots.update(
    {
        "valleys_price_points": prices_list,
        "rsi14_valleys_points": rsi_len14_list,
        "macd_valleys_points": macd_list,
        "stoch_valleys_points": stoch_list,
    }
)

# *Divergence
init_notif("Divergence")

peaks_prices = pivots["peaks_price_points"]
valleys_prices = pivots["valleys_price_points"]

rsi_peaks = pivots["rsi14_peaks_points"]
rsi_valleys = pivots["rsi14_valleys_points"]

macd_peaks = pivots["macd_peaks_points"]
macd_valleys = pivots["macd_valleys_points"]

stoch_peaks = pivots["stoch_peaks_points"]
stoch_valleys = pivots["stoch_valleys_points"]

# negative normal N hidden divergence
rsi_nnd_list = map(divergence.negative_normal_divergence, peaks_prices, rsi_peaks)
rsi_nhd_list = map(divergence.negative_hidden_divergence, peaks_prices, rsi_peaks)

macd_nnd_list = map(divergence.negative_normal_divergence, peaks_prices, macd_peaks)
macd_nhd_list = map(divergence.negative_hidden_divergence, peaks_prices, macd_peaks)

stoch_nnd_list = map(divergence.negative_normal_divergence, peaks_prices, stoch_peaks)
stoch_nhd_list = map(divergence.negative_hidden_divergence, peaks_prices, stoch_peaks)
# positive normal N hidden divergence
rsi_pnd_list = map(divergence.positive_normal_divergence, valleys_prices, rsi_valleys)
rsi_phd_list = map(divergence.positive_hidden_divergence, valleys_prices, rsi_valleys)

macd_pnd_list = map(divergence.positive_normal_divergence, valleys_prices, macd_valleys)
macd_phd_list = map(divergence.positive_hidden_divergence, valleys_prices, macd_valleys)

stoch_pnd_list = map(
    divergence.positive_normal_divergence, valleys_prices, stoch_valleys
)
stoch_phd_list = map(
    divergence.positive_hidden_divergence, valleys_prices, stoch_valleys
)
# Convert divergences map obj to list
rsi_nnd_list = list(rsi_nnd_list)
rsi_nhd_list = list(rsi_nhd_list)
rsi_pnd_list = list(rsi_pnd_list)
rsi_phd_list = list(rsi_phd_list)

macd_nnd_list = list(macd_nnd_list)
macd_nhd_list = list(macd_nhd_list)
macd_pnd_list = list(macd_pnd_list)
macd_phd_list = list(macd_phd_list)

stoch_nnd_list = list(stoch_nnd_list)
stoch_nhd_list = list(stoch_nhd_list)
stoch_pnd_list = list(stoch_pnd_list)
stoch_phd_list = list(stoch_phd_list)

# *SquareOfNine
init_notif("SquareOfNine")

get_peaks_nine_sqr = partial(utils.map_2d_lists, map_fn=nine_sqr.get_peaks_square)
get_valleys_nine_sqr = partial(utils.map_2d_lists, map_fn=nine_sqr.get_valley_square)

peaks_nine_square = map(get_peaks_nine_sqr, peaks_prices)
valleys_nine_square = map(get_valleys_nine_sqr, valleys_prices)

peaks_nine_square = list(peaks_nine_square)
valleys_nine_square = list(valleys_nine_square)

# *Resisstant&Support
init_notif("Resisstant&Support")

map_2d_pivots_lvls = partial(utils.map_2d_lists, map_fn=rs.get_peaks_lvl)
map_2d_valleys_lvls = partial(utils.map_2d_lists, map_fn=rs.get_valleys_lvl)

peaks_price_lvls = map(map_2d_pivots_lvls, peaks_prices)
valleys_price_lvls = map(map_2d_valleys_lvls, valleys_prices)

peaks_price_lvls = list(peaks_price_lvls)
valleys_price_lvls = list(valleys_price_lvls)

# *Harmonic Pattern
init_notif("HarmonicPattern")
# hp.run(df_data)

# *Ichimoku
init_notif("Ichimoku")
ich = oscillator.get_ichimoku(df_data)

# spanA, spanB, tenkan_sen(conversion line), kijun_sen(base line),and chikou_span columns
ich = ich[0]

price = 2.0

span_a = ich["ISA_9"]
span_b = ich["ISB_26"]
cnv_line = ich["ITS_9"]
b_line = ich["IKS_26"]

ich_stats = map(
    lambda a, b, cnv, bl: oscillator.ichimoku_stats(price, a, b, cnv, bl),
    span_a,
    span_b,
    cnv_line,
    b_line,
)
ich_stats = list(ich_stats)

print("done. %s" % (time.time() - start_time))

# TODO:Check if a strategy got True status

to_send = {}

to_send.update({"ichimoku": ich_stats})

to_send.update(
    {
        "resisstantNSupport": {
            "valleys": valleys_price_lvls,
            "peaks": peaks_price_lvls,
        },
    }
)

to_send.update(
    {
        "squareOfNine": {"valleys": valleys_nine_square, "peaks": peaks_nine_square},
    }
)

divergences_data = []

divergences_data.append(
    {
        "name": "nnd",
        "description": "negative normal divergence",
        "stoch": stoch_nnd_list,
        "macd": macd_nnd_list,
        "rsi": rsi_nnd_list,
    }
)

divergences_data.append(
    {
        "name": "nhd",
        "description": "negative hidden divergence",
        "stoch": stoch_nhd_list,
        "macd": macd_nhd_list,
        "rsi": rsi_nhd_list,
    },
)

divergences_data.append(
    {
        "name": "pnd",
        "description": "positive normal divergence",
        "stoch": stoch_pnd_list,
        "macd": macd_pnd_list,
        "rsi": rsi_pnd_list,
    }
)

divergences_data.append(
    {
        "name": "phd",
        "description": "positive hidden divergence",
        "stoch": stoch_phd_list,
        "macd": macd_phd_list,
        "rsi": rsi_phd_list,
    },
)
