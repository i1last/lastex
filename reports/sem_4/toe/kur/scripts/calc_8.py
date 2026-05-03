from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_3 import freq
from scripts.calc_2 import tf
import numpy as np

ex8 = {}

def get_H(w):
    """Комплексная частотная характеристика цепи"""
    s_var = 1j * w
    num = tf['N2'] * s_var**2 + tf['N0']
    den = tf['D3'] * s_var**3 + tf['D2'] * s_var**2 + tf['D1'] * s_var + tf['D0']
    return num / den

def get_I1(w, tu):
    """Комплексный спектр входного импульса"""
    w_safe = np.where(w == 0, 1e-10, w)
    val = (4 * Im / w_safe * np.sin(w_safe * 2*tu / 4)**2) * np.exp(1j * (np.pi/2 - w_safe * 2*tu / 2))
    val = np.where(w == 0, 0, val)
    return val

# Перенос базовых параметров
Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']
A0 = freq['A0']

# Значения амплитудного спектра входного сигнала на нулевой частоте (из п. 7)
ex8['A1_0_1'] = 0
ex8['A1_0_2'] = 0

# Значения амплитудного спектра реакции на нулевой частоте A2(0) = A1(0) * A(0)
ex8['A2_0_1'] = ex8['A1_0_1'] * A0
ex8['A2_0_2'] = ex8['A1_0_2'] * A0