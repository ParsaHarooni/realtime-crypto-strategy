"""divergence's based on rsi,macd and stoch inds.

    Parameters
    ----------
    zigzags : list
        peaks or valleys last 2 row's
    ind_res : list
        resault's of first and second row of given indicators

    Returns
    ------
    divergence stat : bool
        ZigZag1stRow(+1) > ZigZag2ndRow(+1) && + inds1stRow(c,14) < +inds2ndRow(c,14)
"""

def negative_normal_divergence(zigzag_peaks: list, ind_res: list):
    return bool(zigzag_peaks[0] < zigzag_peaks[1] and ind_res[0] > ind_res[1])

def negative_hidden_divergence(zigzag_peakss: list, ind_res: list):
    return bool(zigzag_peakss[0] > zigzag_peakss[1] and ind_res[0] < ind_res[1])

def positive_normal_divergence(zigzag_valleys: list, ind_res: list):
    return bool(zigzag_valleys[0] > zigzag_valleys[1] and ind_res[0] < ind_res[1])

def positive_hidden_divergence(zigzag_valleys: list, ind_res: list):
    return bool(zigzag_valleys[0] < zigzag_valleys[1] and ind_res[0] > ind_res[1])

