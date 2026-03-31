# scripts/calc_5.py
import numpy as np
import cmath
from scripts.calc_2 import tf
from scripts.calc_4 import mat

res = {}

p1 = tf['p1_re']
p2 = complex(tf['p2_re'], tf['p2_im'])

# Функция вычисления производной знаменателя D'(s) для нахождения вычетов
def D_prime(s):
    return 3 * tf['D3'] * s**2 + 2 * tf['D2'] * s + tf['D1']

# Вычеты для импульсной характеристики h(t)
# Формула: Res(p_k) = N(p_k) / D'(p_k)
A1 = (tf['N2'] * p1**2 + tf['N0']) / D_prime(p1)
A2 = (tf['N2'] * p2**2 + tf['N0']) / D_prime(p2)

res['A1_r'] = A1.real
res['A2_r'] = A2.real
res['A2_i'] = A2.imag
res['A2_mag_half'] = abs(A2)
res['A2_mag'] = 2 * abs(A2)
res['A2_arg'] = np.degrees(cmath.phase(A2))

# Вычеты для переходной характеристики h1(t) = H(s)/s
# Полюсы: 0, p1, p2, p3
B0 = tf['N0'] / tf['D0']
B1 = A1 / p1
B2 = A2 / p2

res['B0'] = B0
res['B1_r'] = B1.real
res['B2_r'] = B2.real
res['B2_i'] = B2.imag
res['B2_mag_half'] = abs(B2)
res['B2_mag'] = 2 * abs(B2)
res['B2_arg'] = np.degrees(cmath.phase(B2))

# Параметры численного метода Эйлера
res['tau1'] = 1 / abs(tf['p1_re'])
res['tau2'] = 1 / abs(tf['p2_re'])
res['T2'] = 2 * np.pi / abs(tf['p2_im'])

dt_calc = 0.2 * min(res['tau1'], res['tau2'], res['T2'] / 4)
res['dt'] = round(dt_calc, 3)
if res['dt'] == 0: res['dt'] = 0.001

res['t_max'] = 3 * max(res['tau1'], res['tau2'])
steps = int(res['t_max'] / res['dt'])

# Инициализация переменных состояния
x1, x2, x3 = 0.0, 0.0, 0.0
input_F = 1.0

# Фиксация первых двух шагов для демонстрации в отчете
res['dx1_0'] = mat['A11']*x1 + mat['A12']*x2 + mat['A13']*x3 + mat['B11']*input_F
res['dx2_0'] = mat['A21']*x1 + mat['A22']*x2 + mat['A23']*x3 + mat['B21']*input_F
res['dx3_0'] = mat['A31']*x1 + mat['A32']*x2 + mat['A33']*x3 + mat['B31']*input_F

res['x1_1'] = x1 + res['dt'] * res['dx1_0']
res['x2_1'] = x2 + res['dt'] * res['dx2_0']
res['x3_1'] = x3 + res['dt'] * res['dx3_0']

res['dx1_1'] = mat['A11']*res['x1_1'] + mat['A12']*res['x2_1'] + mat['A13']*res['x3_1'] + mat['B11']*input_F
res['dx2_1'] = mat['A21']*res['x1_1'] + mat['A22']*res['x2_1'] + mat['A23']*res['x3_1'] + mat['B21']*input_F
res['dx3_1'] = mat['A31']*res['x1_1'] + mat['A32']*res['x2_1'] + mat['A33']*res['x3_1'] + mat['B31']*input_F

res['x1_2'] = res['x1_1'] + res['dt'] * res['dx1_1']
res['x2_2'] = res['x2_1'] + res['dt'] * res['dx2_1']
res['x3_2'] = res['x3_1'] + res['dt'] * res['dx3_1']

# Аналитическая функция h1(t)
def h1_an(t):
    return res['B0'] + res['B1_r'] * np.exp(tf['p1_re'] * t) + \
           res['B2_mag'] * np.exp(tf['p2_re'] * t) * np.cos(tf['p2_im'] * t + np.radians(res['B2_arg']))

# Формирование данных для таблицы LaTeX
euler_t, euler_x1, euler_x2, euler_x3, euler_an = [], [], [], [],[]
print_step = max(1, steps // 15)

x1, x2, x3 = 0.0, 0.0, 0.0
for i in range(steps + 1):
    t = i * res['dt']
    
    if i % print_step == 0 or i == steps:
        euler_t.append(t)
        euler_x1.append(x1)
        euler_x2.append(x2)
        euler_x3.append(x3)
        euler_an.append(h1_an(t))
        
    dx1 = mat['A11']*x1 + mat['A12']*x2 + mat['A13']*x3 + mat['B11']*input_F
    dx2 = mat['A21']*x1 + mat['A22']*x2 + mat['A23']*x3 + mat['B21']*input_F
    dx3 = mat['A31']*x1 + mat['A32']*x2 + mat['A33']*x3 + mat['B31']*input_F
    
    x1 += res['dt'] * dx1
    x2 += res['dt'] * dx2
    x3 += res['dt'] * dx3

res['euler_t'] = euler_t
res['euler_x1'] = euler_x1
res['euler_x2'] = euler_x2
res['euler_x3'] = euler_x3
res['euler_an'] = euler_an