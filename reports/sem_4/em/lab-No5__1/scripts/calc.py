import numpy as np
from scripts.protocol import p

r = {}

# Задание 1: Расчет удельного и поверхностного сопротивления
R_film = np.array(p['pr13']['R'])
b_film = np.array(p['pr13']['b'])
l_film = np.array(p['pr13']['l'])
r['R_sq'] = R_film * b_film / l_film

R_wire = np.array(p['pr610']['R'])
l_wire = np.array(p['pr610']['l'])
d_wire = np.array(p['pr610']['d'])
S_wire = np.pi * d_wire**2 / 4
r['rho'] = R_wire * S_wire / l_wire

# Задание 3: Расчет ТКС
t = np.array(p['rt']['t'])
R_Ni = np.array(p['rt']['R_Ni'])
R_Cu = np.array(p['rt']['R_Cu'])
R_Const = np.array(p['rt']['R_Const'])

# Линейная аппроксимация для нахождения постоянного отношения dR/dt
r['dR_Ni_dt'] = np.polyfit(t, R_Ni, 1)[0]
r['dR_Cu_dt'] = np.polyfit(t, R_Cu, 1)[0]
r['dR_Const_dt'] = np.polyfit(t, R_Const, 1)[0]

alpha_l_Ni = 12.8e-6
alpha_l_Cu = 16.7e-6
alpha_l_Const = 17.0e-6

r['alpha_rho_Ni'] = r['dR_Ni_dt'] / R_Ni + alpha_l_Ni
r['alpha_rho_Cu'] = r['dR_Cu_dt'] / R_Cu + alpha_l_Cu
r['alpha_rho_Const'] = r['dR_Const_dt'] / R_Const + alpha_l_Const

# Задание 5: Расчет характеристик сплава Cu-Ni
# Индексы в протоколе: 1 - медь, 3 - константан, 4 - никель
rho_Cu = r['rho'][1]
rho_Const = r['rho'][3]
rho_Ni = r['rho'][4]

x_Ni_const = 0.4
x_Cu_const = 0.6
r['C'] = (rho_Const - rho_Ni * x_Ni_const - rho_Cu * x_Cu_const) / (x_Ni_const * x_Cu_const)

r['x_Ni'] = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
r['rho_alloy'] = rho_Ni * r['x_Ni'] + rho_Cu * (1 - r['x_Ni']) + r['C'] * r['x_Ni'] * (1 - r['x_Ni'])

alpha_rho_Cu_rt = r['alpha_rho_Cu'][0]
alpha_rho_Ni_rt = r['alpha_rho_Ni'][0]

r['alpha_rho_alloy'] = (1 / r['rho_alloy']) * ((1 - r['x_Ni']) * rho_Cu * alpha_rho_Cu_rt + r['x_Ni'] * rho_Ni * alpha_rho_Ni_rt)

# Задание 7: Подготовка данных термоЭДС
r['dt'] = np.array(p['eds']['t_hot']) - np.array(p['eds']['t_cold'])
r['U_Cu_Fe_mV'] = np.array(p['eds']['U_Cu_Fe']) * 1e3
r['U_Cu_Const_mV'] = np.array(p['eds']['U_Cu_Const']) * 1e3
r['U_Cu_Mang_mV'] = np.array(p['eds']['U_Cu_Mang']) * 1e3