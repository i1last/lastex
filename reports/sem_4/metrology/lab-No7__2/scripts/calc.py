import numpy as np
from scripts.protocol import p

r = {}

# Задание 2: Основная погрешность
Ui = np.array(p['em']['Ui'])
Uoup = np.array(p['em']['Uoup'])
Uodown = np.array(p['em']['Uodown'])
UN = p['em']['UN']

dU_up = (Ui - Uoup)
dU_down = (Ui - Uodown)

delta_up = dU_up / Uoup * 100
delta_down = dU_down / Uodown * 100

gamma_up = dU_up / UN * 100
gamma_down = dU_down / UN * 100

H = np.abs(Uoup - Uodown)

Uavg = (Uoup + Uodown) / 2
dU_avg = (Ui - Uavg)
delta_avg = dU_avg / Uavg * 100
gamma_avg = dU_avg / UN * 100

r['em'] = {
    'dU_up': dU_up.tolist(),
    'dU_down': dU_down.tolist(),
    'delta_up': delta_up.tolist(),
    'delta_down': delta_down.tolist(),
    'gamma_up': gamma_up.tolist(),
    'gamma_down': gamma_down.tolist(),
    'H': H.tolist(),
    'Uavg': Uavg.tolist(),
    'delta_avg': delta_avg.tolist(),
    'gamma_avg': gamma_avg.tolist()
}

# Задание 3: АЧХ
fhf = np.array(p['ahf']['f'])
Uhf = np.array(p['ahf']['U'])
flf = np.array(p['alf']['f'])
Ulf = np.array(p['alf']['U'])

Uf0 = 2.44
Khf = Uhf / Uf0
Klf = Ulf / Uf0

# Интерполяция для верхней граничной частоты (K = 0.9)
# Поскольку Khf убывает, для np.interp переворачиваем массивы
fb = np.interp(0.9, Khf[::-1], fhf[::-1])

r['afc'] = {
    'Khf': Khf.tolist(),
    'Klf': Klf.tolist(),
    'fb': float(fb),
    'Uf0': Uf0
}

# Задание 4: Влияние формы сигнала
U_sin = p['wi']['sin']
U_rect = p['wi']['rect']
U_tria = p['wi']['tria']

k_sin = 1.11
k_rect = 1.0
k_tria = 1.15
k_cal = 1.11

Ucp_sin = U_sin / k_cal
Ucp_rect = U_rect / k_cal
Ucp_tria = U_tria / k_cal

Utrue_sin = k_sin * Ucp_sin
Utrue_rect = k_rect * Ucp_rect
Utrue_tria = k_tria * Ucp_tria

d_sin = (U_sin - Utrue_sin) / Utrue_sin * 100
d_rect = (U_rect - Utrue_rect) / Utrue_rect * 100
d_tria = (U_tria - Utrue_tria) / Utrue_tria * 100

r['wi'] = {
    'Ucp': [Ucp_sin, Ucp_rect, Ucp_tria],
    'Utrue': [Utrue_sin, Utrue_rect, Utrue_tria],
    'delta': [d_sin, d_rect, d_tria]
}