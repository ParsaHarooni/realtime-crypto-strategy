from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import modules.utils as utils

PEAK = 1
VALLEY = -1

get_peaks_indices = partial(utils.list_of_element_occurrences,element=PEAK)
get_valleys_indices = partial(utils.list_of_element_occurrences,element=VALLEY)

def plot_pivots(X, pivots):
    plt.xlim(0, len(X))
    plt.ylim(X.min()*0.99, X.max()*1.01)
    plt.plot(np.arange(len(X)), X, 'k:', alpha=0.5)
    plt.plot(np.arange(len(X))[pivots != 0], X[pivots != 0], 'k-')
    plt.scatter(np.arange(len(X))[pivots == 1], X[pivots == 1], color='g')
    plt.scatter(np.arange(len(X))[pivots == -1], X[pivots == -1], color='r')
