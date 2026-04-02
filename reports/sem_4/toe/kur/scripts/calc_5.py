import numpy as np
import cmath
import math
from scipy import signal
# Предполагаем, что эти данные импортируются корректно
from scripts.calc_2 import tf
from scripts.calc_4 import mat

# Вспомогательные данные для формул (alpha, beta)
# Обычно они берутся из вещественных и мнимых частей полюсов
fact = {
    'alpha1': abs(tf['p1_re']),
    'alpha2': abs(tf['p2_re']),
    'beta2':  abs(tf['p2_im'])
}

ex5 = {}
h_t = {}
h1_t = {}

# 1. Формируем полюса и нули
z1 = complex(0, tf['z1_im'])
z2 = complex(0, -tf['z1_im'])
p1 = tf['p1_re']
p2 = complex(tf['p2_re'], tf['p2_im'])
p3 = complex(tf['p2_re'], -tf['p2_im']) # сопряженный

# --- Расчет H(s) ---
num_h = np.poly([z1, z2])
den_h = np.poly([p1, p2, p3])
res_h, poles_h, _ = signal.residue(num_h, den_h)

# Маппинг Ak (зависит от порядка poles_h, scipy обычно сортирует их)
# Для надежности найдем индексы по значению полюсов
idx1 = np.argmin(np.abs(poles_h - p1))
idx2 = np.argmin(np.abs(poles_h - p2))

ex5['A1'] = res_h[idx1].real
ex5['A2'] = {'c': res_h[idx2]}
ex5['A2']['r'], phi_rad = cmath.polar(res_h[idx2])
ex5['A2']['phi'] = math.degrees(phi_rad)
ex5['A2']['mag'] = 2 * abs(res_h[idx2])
ex5['A3'] = {'c': res_h[idx2].conjugate(), 'r': ex5['A2']['r'], 'phi': -ex5['A2']['phi']}

# Оригинал h(t)
h_t['a'] = ex5['A1']
h_t['b'] = p1
h_t['c'] = ex5['A2']['mag']
h_t['d'] = p2.real
h_t['e'] = p2.imag
h_t['f'] = abs(ex5['A2']['phi'])

# --- Расчет H1(s) = H(s)/s ---
# Полюса: 0, p1, p2, p3
den_h1 = np.poly([0, p1, p2, p3])
res_h1, poles_h1, _ = signal.residue(num_h, den_h1)

# Маппинг Bk
idx_b1 = np.argmin(np.abs(poles_h1 - 0))   # B1 для 1/s
idx_b2 = np.argmin(np.abs(poles_h1 - p1))  # B2 для 1/(s+p1)
idx_b3 = np.argmin(np.abs(poles_h1 - p2))  # B3 для 1/(s+p2)

ex5['B1'] = res_h1[idx_b1].real
ex5['B2'] = res_h1[idx_b2].real
ex5['B3'] = {'c': res_h1[idx_b3]}
ex5['B3']['r'], b_phi_rad = cmath.polar(res_h1[idx_b3])
ex5['B3']['phi'] = math.degrees(b_phi_rad)
ex5['B3']['mag'] = 2 * abs(res_h1[idx_b3])
ex5['B4'] = {'c': ex5['B3']['c'].conjugate(), 'r': ex5['B3']['r'], 'phi': -ex5['B3']['phi']}

# Оригинал h1(t)
h1_t['a'] = ex5['B1']
h1_t['b'] = ex5['B2']
h1_t['c'] = p1
h1_t['d'] = ex5['B3']['mag']
h1_t['e'] = p2.real
h1_t['f'] = p2.imag
h1_t['g'] = ex5['B3']['phi']

# --- Численный метод (Эйлер) ---
ex5['tau1'] = 1 / abs(p1)
ex5['tau2'] = 1 / abs(p2.real)
ex5['T2'] = 2 * np.pi / abs(p2.imag)

dt_calc = 0.2 * min(ex5['tau1'], ex5['tau2'], ex5['T2'] / 4)
ex5['dt'] = round(dt_calc, 3) if dt_calc > 0.001 else 0.001
ex5['t_max'] = 5 * max(ex5['tau1'], ex5['tau2']) # берем с запасом для ПП
steps = int(ex5['t_max'] / ex5['dt'])

# Начальные условия
x = np.array([0.0, 0.0, 0.0]) # [uC1, iL1, iL2]
A_mat = np.array([
    [mat['A11'], mat['A12'], mat['A13']],
    [mat['A21'], mat['A22'], mat['A23']],
    [mat['A31'], mat['A32'], mat['A33']]
])
B_mat = np.array([mat['B11'], mat['B21'], mat['B31']])
F = 1.0

# Фиксация первых шагов для отчета
def get_dx(curr_x):
    return A_mat @ curr_x + B_mat * F

dx0 = get_dx(x)
ex5['x1_1'], ex5['x2_1'], ex5['x3_1'] = x + ex5['dt'] * dx0

dx1 = get_dx(np.array([ex5['x1_1'], ex5['x2_1'], ex5['x3_1']]))
ex5['x1_2'], ex5['x2_2'], ex5['x3_2'] = np.array([ex5['x1_1'], ex5['x2_1'], ex5['x3_1']]) + ex5['dt'] * dx1

# Аналитическая функция h1(t)
def h1_an(t):
    return h1_t['a'] + h1_t['b'] * np.exp(h1_t['c'] * t) + \
           h1_t['d'] * np.exp(h1_t['e'] * t) * np.cos(np.radians(h1_t['f'] * math.degrees(t) + h1_t['g']))
# Поправка: частота в h1_t['f'] уже в рад/с, t в секундах.
def h1_analytical(t):
    return h1_t['a'] + h1_t['b'] * math.exp(h1_t['c'] * t) + \
           h1_t['d'] * math.exp(h1_t['e'] * t) * math.cos(h1_t['f'] * t + math.radians(h1_t['g']))

# Цикл Эйлера для таблицы
euler_t, euler_x1, euler_x2, euler_x3, euler_an = [], [], [], [], []
print_step = max(1, steps // 12) # Примерно 10-15 строк

curr_x = np.array([0.0, 0.0, 0.0])
for i in range(steps + 1):
    t = i * ex5['dt']
    if i % print_step == 0:
        euler_t.append(t)
        euler_x1.append(curr_x[0])
        euler_x2.append(curr_x[1])
        euler_x3.append(curr_x[2])
        euler_an.append(h1_analytical(t))
    
    curr_x = curr_x + ex5['dt'] * get_dx(curr_x)

ex5['euler_t'], ex5['euler_x1'], ex5['euler_x2'], ex5['euler_x3'], ex5['euler_an'] = euler_t, euler_x1, euler_x2, euler_x3, euler_an