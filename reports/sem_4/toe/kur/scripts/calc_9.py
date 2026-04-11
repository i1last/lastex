import numpy as np
from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_2 import tf
from scripts.calc_6 import reaction

ex9 = {}
Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']

# --- Параметры для численного интегрирования ---
w_max_1 = 100.0 / tu1
w_max_2 = 100.0 / tu2
N_w = 5000

# --- Расчет для tu1 ---
w_arr1 = np.linspace(0, w_max_1, N_w)
s_var1 = 1j * w_arr1
num1 = tf['N2'] * s_var1**2 + tf['N0']
den1 = tf['D3'] * s_var1**3 + tf['D2'] * s_var1**2 + tf['D1'] * s_var1 + tf['D0']
H_w1 = num1 / den1

# Спектр одиночного импульса
w_safe1 = np.where(w_arr1 == 0, 1e-10, w_arr1)
I1_imp_w1 = (2 * Im / w_safe1) * np.sin(w_safe1 * tu1 / 2) * np.exp(-1j * w_safe1 * tu1 / 2)
I1_imp_w1[0] = Im * tu1

# Спектр меандра
I1_meandr_w1 = I1_imp_w1 * (1 - 2 * np.exp(-1j * w_arr1 * tu1) + np.exp(-1j * w_arr1 * 2 * tu1))
I2_w1 = I1_meandr_w1 * H_w1

# Демонстрационный расчет
t_demo1 = tu1 * 1.5
integrand_demo1 = np.abs(I2_w1) * np.cos(w_arr1 * t_demo1 + np.angle(I2_w1))
ex9['i2_approx_demo1'] = np.trapezoid(integrand_demo1, w_arr1) / np.pi
ex9['i2_exact_demo1'] = reaction(t_demo1, tu1)

# --- Расчет для tu2 ---
w_arr2 = np.linspace(0, w_max_2, N_w)
s_var2 = 1j * w_arr2
num2 = tf['N2'] * s_var2**2 + tf['N0']
den2 = tf['D3'] * s_var2**3 + tf['D2'] * s_var2**2 + tf['D1'] * s_var2 + tf['D0']
H_w2 = num2 / den2

w_safe2 = np.where(w_arr2 == 0, 1e-10, w_arr2)
I1_imp_w2 = (2 * Im / w_safe2) * np.sin(w_safe2 * tu2 / 2) * np.exp(-1j * w_safe2 * tu2 / 2)
I1_imp_w2[0] = Im * tu2

I1_meandr_w2 = I1_imp_w2 * (1 - 2 * np.exp(-1j * w_arr2 * tu2) + np.exp(-1j * w_arr2 * 2 * tu2))
I2_w2 = I1_meandr_w2 * H_w2

t_demo2 = tu2 * 1.5
integrand_demo2 = np.abs(I2_w2) * np.cos(w_arr2 * t_demo2 + np.angle(I2_w2))
ex9['i2_approx_demo2'] = np.trapezoid(integrand_demo2, w_arr2) / np.pi
ex9['i2_exact_demo2'] = reaction(t_demo2, tu2)