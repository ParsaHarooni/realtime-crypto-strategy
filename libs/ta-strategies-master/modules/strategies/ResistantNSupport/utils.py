from functools import partial
import modules.utils as utils
import modules.strategies.defaults as defs

CHECKPOINTS = defs.RES_SUP_CHECKPOINTS


def price_levels(pivot: float, check_peak: bool):
    # Percentage of prices
    prices_list = map(lambda point: utils.cal_perc(pivot, point), CHECKPOINTS)
    prices_list = list(prices_list)
    # peak - n% OR valley + n%
    lvls = map(lambda price: price if check_peak else pivot + price, prices_list)
    lvls = list(lvls)

    return lvls


get_peaks_lvl = partial(price_levels, check_peak=True)
get_valleys_lvl = partial(price_levels, check_peak=False)
