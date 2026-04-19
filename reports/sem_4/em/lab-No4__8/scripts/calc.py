# scripts/calc.py
import math
from scripts.protocol import p

# ЗАДАНИЯ 2 и 3 ПЕРПУТАНЫ МЕСТАМИ.
# ЗАГОЛОВКИ УСТАНОВЛЕНЫ ВЕРНО, А НАЗВАНИЯ
# ПЕРЕМЕННЫХ - НЕТ. ПРИ ТЕКУЩЕЙ КОНФИГУРАЦИИ
# ВСЕ КОРРЕКТНО

# Константы установки
mu0 = 4 * math.pi * 1e-7
R_T = 10.0
r_cp = 0.021
w1 = 100
w2 = 1330
C_I = 1e-6
R_I = 300e3
S = 1e-4

r = {
    'R_T': R_T,
    'r_cp': r_cp,
    'w1': w1,
    'w2': w2,
    'C_I': C_I,
    'R_I': R_I,
    'S': S,
    'mu0': mu0
}

# --- Задание 1: Основная кривая намагничивания ---
X = p['mc']['X']
Y = p['mc']['Y']
mx = p['prms']['mx']
my = p['prms']['my']

U_X =[x * mx for x in X]
U_Y = [y * my for y in Y]

H_m =[ux * w1 / (2 * math.pi * r_cp * R_T) for ux in U_X]
B_m =[uy * R_I * C_I / (w2 * S) for uy in U_Y]
mu_st =[b / (mu0 * h) if h != 0 else 0 for b, h in zip(B_m, H_m)]

r['U_X'] = U_X
r['U_Y'] = U_Y
r['H_m'] = H_m
r['B_m'] = B_m
r['mu_st'] = mu_st

r['tab1'] = [
    X,
    U_X,
    H_m,
    Y,
    U_Y,
    B_m,
    mu_st
]

# --- Задание 3: Эффективная магнитная проницаемость ---
f = p['me']['f']
U_in = p['me']['Uin']
U_R = p['me']['U_R']

U_L =[math.sqrt(uin**2 - U_R**2) for uin in U_in]
I = U_R / R_T
L =[ul / (2 * math.pi * f_val * I) for ul, f_val in zip(U_L, f)]
mu_ef =[2 * math.pi * l_val * r_cp / (mu0 * w1**2 * S) for l_val in L]

r['I'] = I
r['U_L'] = U_L
r['L'] = L
r['mu_ef'] = mu_ef

r['tab2'] =[
    f,
    [u * 1000 for u in U_in],  # Перевод в мВ для таблицы
    [U_R * 1000] * len(f),     # Перевод в мВ для таблицы
    [ul * 1000 for ul in U_L], # Перевод в мВ для таблицы
    L,
    mu_ef
]

# --- Задание 2: Магнитные потери ---
# ЗАГЛУШКИ: Заполните реальными площадями (в мм^2)
S_pixel = mx * my  # Площадь одной клетки
S_P = [  # Количество клеток определено на глаз
    S_pixel * 12,
    S_pixel * 13.5,
    S_pixel * 16.2,
    S_pixel * 19.9,
    S_pixel * 20.9
]
f_loss =[50, 200, 400, 600, 800]
d = p['prms']['d']

h1 = (mx * w1) / (R_T * 2 * math.pi * r_cp)
b1 = (my * C_I * R_I) / (w2 * S)

E =[(sp * h1 * b1) / (100 * d) for sp in S_P]

# Линейная регрессия E(f) = k * f + E_G
n = len(f_loss)
sum_f = sum(f_loss)
sum_E = sum(E)
sum_f2 = sum([f_val**2 for f_val in f_loss])
sum_fE = sum([f_val * e_val for f_val, e_val in zip(f_loss, E)])

k_loss = (n * sum_fE - sum_f * sum_E) / (n * sum_f2 - sum_f**2)
E_G = (sum_E - k_loss * sum_f) / n

E_BT =[e_val - E_G for e_val in E]
P_G =[E_G * f_val for f_val in f_loss]
P_BT =[ebt * f_val for ebt, f_val in zip(E_BT, f_loss)]

r['h1'] = h1
r['b1'] = b1
r['f_loss'] = f_loss
r['S_P'] = S_P
r['E'] = E
r['E_G'] = E_G
r['k_loss'] = k_loss
r['E_BT'] = E_BT
r['P_G'] = P_G
r['P_BT'] = P_BT

r['tab3'] = [
    f_loss,
    S_P,
    E,[E_G] * n,
    E_BT,
    P_G,
    P_BT
]