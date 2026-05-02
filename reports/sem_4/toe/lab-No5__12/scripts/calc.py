# scripts/calc.py
import numpy as np
from scripts.protocol import p

r = {'part1': {}, 'part2': {}, 'part3': {}}

# --- Часть 1: Цепь первого порядка ---
R1 = 5e3
C1 = 200e-12
r['part1']['R'] = R1
r['part1']['C'] = C1
r['part1']['tau'] = R1 * C1
r['part1']['p1'] = -1 / r['part1']['tau']

# --- Часть 2: Цепь второго порядка ---
L2 = 360e-6
C2 = 200e-12
R2_list =[4000, 670, 100]
r['part2']['R'] = R2_list
r['part2']['L'] = L2
r['part2']['C'] = C2

alpha =[1 / (2 * R * C2) for R in R2_list]
w0_sq = 1 / (L2 * C2)
r['part2']['w0'] = float(np.sqrt(w0_sq))

p1_real, p1_imag = [],[]
p2_real, p2_imag = [],[]

for a in alpha:
    disc = a**2 - w0_sq
    if disc >= 0:
        p1_real.append(float(-a + np.sqrt(disc)))
        p1_imag.append(0.0)
        p2_real.append(float(-a - np.sqrt(disc)))
        p2_imag.append(0.0)
    else:
        p1_real.append(float(-a))
        p1_imag.append(float(np.sqrt(-disc)))
        p2_real.append(float(-a))
        p2_imag.append(float(-np.sqrt(-disc)))

r['part2']['alpha'] = alpha
r['part2']['p1_real'] = p1_real
r['part2']['p1_imag'] = p1_imag
r['part2']['p2_real'] = p2_real
r['part2']['p2_imag'] = p2_imag

# --- Часть 3: Цепь высокого порядка ---
f_arr = np.array(p['bd']['f'])
H_arr = np.array(p['bd']['Hu'])
H_max = H_arr[0]
H_level = H_max / np.sqrt(2)

# Линейная интерполяция для поиска частоты среза (массив частот инвертируется для корректной работы np.interp)
f_cp = float(np.interp(H_level, H_arr[::-1], f_arr[::-1]))
r['part3']['f_cp'] = f_cp
r['part3']['H_max'] = float(H_max)
r['part3']['H_level'] = float(H_level)

t_u_list =[2e-6, 10e-6]
r['part3']['t_u'] = t_u_list
r['part3']['df_sp'] =[1 / t for t in t_u_list]

r['part3']['U0_2'] = t_u_list[0]
r['part3']['Upi_2'] = 2 * t_u_list[0] / np.pi
r['part3']['U0_10'] = t_u_list[1]
r['part3']['Upi_10'] = 2 * t_u_list[1] / np.pi