import numpy as np
from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_2 import tf
from scripts.calc_6 import reaction
from scripts.calc_8 import get_H, get_I1

ex9 = {}
Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']
t_offset_for_demo = 0.75

# --- Параметры для численного интегрирования ---
w_max_1 = 100.0 / (2*tu1)
w_max_2 = 100.0 / (2*tu2)
N_w = 5000

# --- Расчет для tu1 ---
w_arr1 = np.linspace(0, w_max_1, N_w)
H_w1 = get_H(w_arr1)

# Спектр меандра
w_safe1 = np.where(w_arr1 == 0, 1e-10, w_arr1)
I1_meandr_w1 = get_I1(w_safe1, tu1)

# Вычисление спектра реакции I2(jw) = I1(jw) * H(jw)
I2_w1 = I1_meandr_w1 * H_w1

# Демонстрационный расчет
t_demo1 = tu1 * t_offset_for_demo
integrand_demo1 = np.abs(I2_w1) * np.cos(w_arr1 * t_demo1 + np.angle(I2_w1))
ex9['i2_approx_demo1'] = np.trapezoid(integrand_demo1, w_arr1) / np.pi
ex9['i2_exact_demo1'] = reaction(t_demo1, tu1)

# --- Расчет для tu2 ---
w_arr2 = np.linspace(0, w_max_2, N_w)
H_w2 = get_H(w_arr2)

# Спектр меандра
w_safe2 = np.where(w_arr2 == 0, 1e-10, w_arr2)
I1_meandr_w2 = get_I1(w_safe2, tu2)

# Вычисление спектра реакции I2(jw) = I1(jw) * H(jw)
I2_w2 = I1_meandr_w2 * H_w2

t_demo2 = tu2 * t_offset_for_demo
integrand_demo2 = np.abs(I2_w2) * np.cos(w_arr2 * t_demo2 + np.angle(I2_w2))
ex9['i2_approx_demo2'] = np.trapezoid(integrand_demo2, w_arr2) / np.pi
ex9['i2_exact_demo2'] = reaction(t_demo2, tu2)