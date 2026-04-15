import numpy as np
from scripts.protocol import p

r = {}

# --- Задание 1: Начальный участок статической характеристики ---
r['sc_R'] = np.array(p['sc']['R'])
r['sc_Rp'] = np.array(p['sc']['Rp'])

# --- Задание 2: Инструментальная погрешность ---
# Для диапазона 20 кОм (макс. 19.99 кОм) N_max = 2000
r['ie_range'] = 20000 # Ом
r['ie_q'] = r['ie_range'] / 2000 # Ом (10 Ом)

r['ie_R'] = np.array(p['ie']['R'])
r['ie_Rp'] = np.array(p['ie']['Rp'])
# Расчет абсолютной инструментальной погрешности (ф-ла 1)
r['ie_dR'] = r['ie_Rp'] - 0.5 * r['ie_q'] - r['ie_R']

# --- Задание 3: Аддитивная и мультипликативная составляющие ---
# Линейная аппроксимация dR = a + b * R
b, a = np.polyfit(r['ie_R'], r['ie_dR'], 1)
r['b'] = b
r['a'] = a
# Нормировка аддитивной составляющей на квант текущего предела
r['a_norm'] = a / r['ie_q'] 

# --- Задание 4: Погрешность измерения резисторов (по паспорту GDM-8135) ---
r['res_names'] = []
r['res_ranges'] = []
r['res_Rp'] = []
r['res_abs'] = []
r['res_rel'] = []
r['res_final'] = []

for key, val in p['r'].items():
    R_p_kohm = val['Rp']
    R_p = R_p_kohm * 1000 # Ом
    rng_kohm = val['range']
    rng = rng_kohm * 1000 # Ом
    
    # Разрешение k (квант) для GDM-8135
    k = rng / 2000 # Ом
    
    # Погрешность по паспорту: +-(0.002*X + 1*k) для пределов до 2 МОм
    abs_err = 0.002 * R_p + 1.0 * k
    rel_err = (abs_err / R_p) * 100
    
    r['res_names'].append(key)
    r['res_ranges'].append(rng_kohm)
    r['res_Rp'].append(R_p_kohm)
    r['res_abs'].append(abs_err / 1000) # в кОм для таблицы
    r['res_rel'].append(rel_err)
    r['res_final'].append(f"{R_p_kohm:.3f} \\pm {abs_err/1000:.3f}")

# Переменные для примера расчета в отчете
r['ex_R_p'] = p['r']['RN1']['Rp'] * 1000
r['ex_k'] = (p['r']['RN1']['range'] * 1000) / 2000
r['ex_abs'] = 0.002 * r['ex_R_p'] + 1.0 * r['ex_k']

# Вручную округлим по правилам округления погрешностей
val_rounded1 = round(r['res_Rp'][0], 1)
err_rounded1 = round(r['res_abs'][0], 1)
r['res_final'][0] = f"{val_rounded1:.3f} \\pm {err_rounded1:.3f}"

val_rounded2 = round(r['res_Rp'][1], 2)
err_rounded2 = round(r['res_abs'][1], 2)
r['res_final'][1] = f"{val_rounded2:.3f} \\pm {err_rounded2:.3f}"