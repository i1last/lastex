import numpy as np
from scripts.protocol import p

r = {}
f_arr = np.array(p['ad']['f'])

# 1. АЧХ (Коэффициенты передачи)
r['K_dc'] = np.array(p['ad']['Udc']) / p['ad']['Uin']
r['K_ic'] = np.array(p['ad']['Uic']) / p['ad']['Uin']
r['K_actdc'] = np.array(p['ad']['Uactdc']) / p['ad']['Uin']
r['K_actic'] = np.array(p['ad']['Uactic']) / p['ad']['Uin']

# 2. Графическое определение граничных частот
# Пассивные цепи
level_passive = 1 / np.sqrt(2)
r['f_n_gr_graph_dc'] = np.interp(level_passive, r['K_dc'], f_arr)
r['f_v_gr_graph_ic'] = np.interp(level_passive, r['K_ic'][::-1], f_arr[::-1])

# Активные цепи
# АИЦ (ФНЧ)
k_max_actic = np.max(r['K_actic'])
level_actic = k_max_actic / np.sqrt(2)
r['f_v_gr_graph_actic'] = np.interp(level_actic, r['K_actic'][::-1], f_arr[::-1])

# АДЦ (Полосовой фильтр)
k_max_actdc = np.max(r['K_actdc'])
level_actdc = k_max_actdc / np.sqrt(2)
idx_max = np.argmax(r['K_actdc'])

# Нижняя частота (на восходящем участке)
r['f_n_gr_graph_actdc'] = np.interp(level_actdc, r['K_actdc'][:idx_max+1], f_arr[:idx_max+1])
# Верхняя частота (на нисходящем участке)
r['f_v_gr_graph_actdc'] = np.interp(level_actdc, r['K_actdc'][idx_max:][::-1], f_arr[idx_max:][::-1])

# 3. Расчет ошибок
r['cletok'] = 3
r['razvertka'] = 0.1e-3
r['tau_i'] = r['razvertka'] * r['cletok']

r['UmaxKL'] = 3.4
r['UmaxVD'] = 0.5
r['Umax'] = r['UmaxKL'] * r['UmaxVD']
r['U5p'] = 0.05 * r['Umax']
r['U5pKL'] = r['U5p'] / r['UmaxVD']
r['tauKL'] = 2.2
r['tauTD'] = 0.1e-3
r['tau'] = r['tauKL'] * r['tauTD']

r['err_d_p_cond'] = 3 * r['tau'] / r['tau_i']
r['err_i_p_cond'] = r['tau_i'] / 3 / r['tau']
# # 3.1. Для экспериментальных данных
# r['R_p'] = 10e3
# r['C_p'] = 10e-9
# r['tau_p'] = r['R_p'] * r['C_p']
# r['err_d_p_exp'] = (3 * r['tau_p'] / r['tau_i']) * 100
# r['err_i_p_exp'] = (r['tau_i'] / (3 * r['tau_p'])) * 100

# # 3.2. Для гипотетических "идеальных" условий
# # Условие дифференцирования: 3*tau << tau_i. Возьмем tau = 1e-5 c.
# r['R_d_cond'] = 1e3
# r['C_d_cond'] = 10e-9
# r['tau_d_cond'] = r['R_d_cond'] * r['C_d_cond']
# r['err_d_p_cond'] = (3 * r['tau_d_cond'] / r['tau_i']) * 100

# # Условие интегрирования: 3*tau >> tau_i. Возьмем tau = 1e-3 c.
# r['R_i_cond'] = 100e3
# r['C_i_cond'] = 10e-9
# r['tau_i_cond'] = r['R_i_cond'] * r['C_i_cond']
# r['err_i_p_cond'] = (r['tau_i'] / (3 * r['tau_i_cond'])) * 100