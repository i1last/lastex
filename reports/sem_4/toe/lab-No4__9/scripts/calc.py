# scripts/calc.py
import numpy as np
from scripts.protocol import p

r = {}
omega = 2 * np.pi * p['prms']['f']

# Задания 1, 2: Определение параметров катушек
x1 = p['prms']['c1']['Uin'] / p['prms']['c1']['Iin']
x2 = p['prms']['c2']['Uin'] / p['prms']['c2']['Iin']
L1 = x1 / omega
L2 = x2 / omega

xM1 = p['prms']['c1']['Uout'] / p['prms']['c1']['Iin']
xM2 = p['prms']['c2']['Uout'] / p['prms']['c2']['Iin']
M1 = xM1 / omega
M2 = xM2 / omega
M_avg = (M1 + M2) / 2

k = M_avg / np.sqrt(L1 * L2)

r['prms'] = {
    'x1': x1, 'x2': x2,
    'L1': L1, 'L2': L2,
    'xM1': xM1, 'xM2': xM2,
    'M1': M1, 'M2': M2,
    'M_avg': M_avg,
    'k': k
}

# Задание 3: Последовательное соединение
omega_sc = 2 * np.pi * p['sc']['f']
L_sc_exp_sogl = p['sc']['Ugen'] / (omega_sc * p['sc']['sogl']['Igen'])
L_sc_exp_vstr = p['sc']['Ugen'] / (omega_sc * p['sc']['vstr']['Igen'])

L_sc_th_sogl = L1 + L2 + 2 * M_avg
L_sc_th_vstr = L1 + L2 - 2 * M_avg

r['sc'] = {
    'exp_sogl': L_sc_exp_sogl,
    'exp_vstr': L_sc_exp_vstr,
    'th_sogl': L_sc_th_sogl,
    'th_vstr': L_sc_th_vstr
}

# Задание 4: Параллельное соединение
omega_pc = 2 * np.pi * p['pc']['f']
L_pc_exp_sogl = p['pc']['U'] / (omega_pc * p['pc']['sogl']['Igen'])
L_pc_exp_vstr = p['pc']['U'] / (omega_pc * p['pc']['vstr']['Igen'])

L_pc_th_sogl = (L1 * L2 - M_avg**2) / (L1 + L2 - 2 * M_avg)
L_pc_th_vstr = (L1 * L2 - M_avg**2) / (L1 + L2 + 2 * M_avg)

r['pc'] = {
    'exp_sogl': L_pc_exp_sogl,
    'exp_vstr': L_pc_exp_vstr,
    'th_sogl': L_pc_th_sogl,
    'th_vstr': L_pc_th_vstr
}

# Задания 5-7: АЧХ трансформатора
f_afc = np.array(p['afc']['f'])
omega_afc = 2 * np.pi * f_afc
U1 = p['afc']['U1']

def H_th(w, R_H):
    return (M_avg * R_H) / np.sqrt(w**2 * (L1 * L2 - M_avg**2)**2 + (L1 * R_H)**2)

H_exp_R1 = np.array(p['afc']['R1']['U2']) / U1
H_th_R1 = H_th(omega_afc, p['afc']['R1']['R'])

H_exp_R2 = np.array(p['afc']['R2']['U2']) / U1
H_th_R2 = H_th(omega_afc, p['afc']['R2']['R'])

f_plot = np.linspace(f_afc[0], f_afc[-1], 200)
omega_plot = 2 * np.pi * f_plot

r['afc'] = {
    'f': f_afc,
    'H_exp_R1': H_exp_R1,
    'H_th_R1': H_th_R1,
    'H_exp_R2': H_exp_R2,
    'H_th_R2': H_th_R2,
    'f_plot': f_plot,
    'H_th_R1_plot': H_th(omega_plot, p['afc']['R1']['R']),
    'H_th_R2_plot': H_th(omega_plot, p['afc']['R2']['R'])
}