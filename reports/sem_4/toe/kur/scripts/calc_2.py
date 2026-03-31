import numpy as np
from scripts.calc_1 import n

tf = {}

# Коэффициенты числителя N(s) = N2*s^2 + N0
tf['N2'] = n['L1'] * n['C1'] * n['R1']
tf['N0'] = n['R1']

# Коэффициенты знаменателя D(s) = D3*s^3 + D2*s^2 + D1*s + D0
tf['D3'] = n['L1'] * n['L2'] * n['C1']
tf['D2'] = n['L1'] * n['C1'] * n['R2'] + n['L2'] * n['C1'] * n['R1'] + n['L1'] * n['C1'] * n['R1']
tf['D1'] = n['L2'] + n['R1'] * n['R2'] * n['C1']
tf['D0'] = n['R2'] + n['R1']

# Расчет корней знаменателя (полюсов) через numpy
den_coeffs = [tf['D3'], tf['D2'], tf['D1'], tf['D0']]
roots = np.roots(den_coeffs)

# Сортировка корней: 1 вещественный, 2 комплексно-сопряженных
real_roots =[r for r in roots if abs(r.imag) < 1e-10]
complex_roots = [r for r in roots if abs(r.imag) >= 1e-10]

p1 = real_roots[0].real
p2 = complex_roots[0]
if p2.imag < 0:
    p2 = np.conj(p2) # Гарантируем, что p2 имеет положительную мнимую часть
p3 = np.conj(p2)

tf['p1_re'] = p1
tf['p1_im'] = 0.0
tf['p2_re'] = p2.real
tf['p2_im'] = p2.imag
tf['p3_re'] = p3.real
tf['p3_im'] = p3.imag

# Расчет нулей
num_coeffs = [tf['N2'], 0, tf['N0']]
z_roots = np.roots(num_coeffs)
tf['z1_im'] = abs(z_roots[0].imag)
tf['z2_im'] = -tf['z1_im']

# Практическая длительность переходного процесса
min_re = min(abs(tf['p1_re']), abs(tf['p2_re']))
tf['t_pp'] = 3 / min_re