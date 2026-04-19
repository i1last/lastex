from scripts.protocol import p

r = {}

# Расчет коэффициентов усиления K = U_вых / U_вх
r['K_parPoU'] = [u / p['Uin'] for u in p['UparPoU']]
r['K_serPoU'] = [u / p['Uin'] for u in p['UserPoU']]
r['K_parPoI'] = [u / p['Uin'] for u in p['UparPoI']]

def calc_params(f, K):
    """Вычисление максимального усиления и граничных частот (линейная интерполяция)."""
    K_max = max(K)
    K_gr = 0.707 * K_max
    
    f_gr = None
    for i in range(len(K) - 1):
        if (K[i] >= K_gr and K[i+1] <= K_gr) or (K[i] <= K_gr and K[i+1] >= K_gr):
            f_gr = f[i] + (K_gr - K[i]) * (f[i+1] - f[i]) / (K[i+1] - K[i])
            break
            
    f_eu = None
    for i in range(len(K) - 1):
        if (K[i] >= 1.0 and K[i+1] <= 1.0) or (K[i] <= 1.0 and K[i+1] >= 1.0):
            f_eu = f[i] + (1.0 - K[i]) * (f[i+1] - f[i]) / (K[i+1] - K[i])
            break
            
    return K_max, f_gr, f_eu

r['Kmax_parPoU'], r['fgr_parPoU'], r['feu_parPoU'] = calc_params(p['fPoU'], r['K_parPoU'])
r['Kmax_serPoU'], r['fgr_serPoU'], r['feu_serPoU'] = calc_params(p['fPoU'], r['K_serPoU'])
r['Kmax_parPoI'], r['fgr_parPoI'], r['feu_parPoI'] = calc_params(p['fPoI'], r['K_parPoI'])