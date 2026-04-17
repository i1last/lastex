import numpy as np
from scipy.signal import find_peaks
from scripts.calc_6 import ex6
from scripts.calc_1 import n
from scripts.calc_3 import freq

ex7 = {}

Im = ex6['Im']
ex7['w_c'] = freq['w_c']

def calc_spectrum_params(ti):
    res = {}
    res['A1_0'] = 0
    res['w_y1'] = 4 * np.pi / ti
    
    # Теоретическая ширина по огибающей
    res['w_sp_env'] = 20.0 / ti
    
    # Практическая ширина (поиск пика лепестка, ближайшего к 10% уровню)
    w_max = 5 * res['w_y1']
    w = np.linspace(1e-5, w_max, 5000)
    A1 = np.abs((4 * Im / w) * np.sin(w * ti / 4)**2)
    
    target = 0.1 * res['A1_0']
    peaks, _ = find_peaks(A1)
    
    # Находим индекс пика, амплитуда которого максимально близка к target
    idx_peak = peaks[np.argmin(np.abs(A1[peaks] - target))]
    res['w_sp'] = w[idx_peak]
    
    return res

ex7['ti1'] = calc_spectrum_params(n['ti1'])
ex7['ti2'] = calc_spectrum_params(n['ti2'])