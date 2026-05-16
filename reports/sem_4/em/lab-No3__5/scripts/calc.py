from scripts.protocol import p

r = {}

# Температурные коэффициенты линейного расширения диэлектриков (1/K)
r['ald'] = [3e-6, 13.5e-6, 8e-6, 1.1e-4, 12e-6]

# Расчет истинной емкости образцов (C_net = C_meas - C0)
for i in range(1, 6):
    r[f'C{i}_net'] = [c - p['C0'] for c in p[f'C{i}']]

# Массив температур для рассчитанных коэффициентов (на 1 элемент короче)
r['t_calc'] = p['t'][:-1]

# Расчет коэффициентов alpha_C и alpha_epsilon
for i in range(1, 6):
    ac_list = []
    ae_list = []
    C_net = r[f'C{i}_net']
    ald_val = r['ald'][i-1]
    
    # Для линейных диэлектриков (1-4) производная постоянна
    if i < 5:
        dt_full = p['t'][-1] - p['t'][0]
        dC_full = C_net[-1] - C_net[0]
        dCdt_linear = dC_full / dt_full if dt_full != 0 else 0

    for j in range(len(r['t_calc'])):
        if i < 5:
            dCdt = dCdt_linear
        else:
            # Для сегнетокерамики (5) производная вычисляется по интервалам
            dt = p['t'][j+1] - p['t'][j]
            dC = C_net[j+1] - C_net[j]
            dCdt = dC / dt if dt != 0 else 0
            
        ac = (1 / C_net[j]) * dCdt
        ae = ac - ald_val
        
        ac_list.append(ac)
        ae_list.append(ae)
        
    r[f'ac{i}'] = ac_list
    r[f'ae{i}'] = ae_list