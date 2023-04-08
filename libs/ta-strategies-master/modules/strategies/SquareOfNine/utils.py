from functools import partial
import modules.strategies.defaults as defs


def pivots_sqrt_list(pivot: int, count_list: list = defs.SQUARE_MULTI_DIV_NUMBERS):
    import math

    list_by_multi = map(lambda num: math.sqrt(pivot * num), count_list)
    list_by_divide = map(lambda num: math.sqrt(pivot / num), count_list)

    list_by_multi = list(list_by_multi)
    list_by_divide = list(list_by_divide)

    return {"list_by_multi": list_by_multi, "list_by_divide": list_by_divide}


def check_nine_square(count_num, sqrt, check_peak: bool):
    to_return = sqrt - count_num if check_peak else sqrt + count_num
    to_return = to_return ** 2
    return to_return


map_peak_square = partial(check_nine_square, check_peak=False)
map_valley_square = partial(check_nine_square, check_peak=True)


def pivots_nine_square(pivot: float, map_func, count_list=defs.SQUARE_ADD_SUB_NUMBERS):
    sqrt_list = pivots_sqrt_list(pivot)

    list_by_multi = map(map_func, count_list, sqrt_list["list_by_multi"])
    list_by_divide = map(map_func, count_list, sqrt_list["list_by_divide"])

    list_by_multi = list(list_by_multi)
    list_by_divide = list(list_by_divide)

    return {"list_by_multi": list_by_multi, "list_by_divide": list_by_divide}

get_peaks_square = partial(pivots_nine_square,map_func=map_peak_square)
get_valley_square = partial(pivots_nine_square,map_func=map_valley_square)