import numpy as np
from scripts.source import s
from scripts.calc_1 import n

ex10 = {}
Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']

# Принимаем период равным длительности полного импульса
ex10['tu1'] = tu1
ex10['tu2'] = tu2
ex10['T1'] = 2*tu1
ex10['T2'] = 2*tu2
ex10['w1_1'] = 2 * np.pi / ex10['T1']
ex10['w1_2'] = 2 * np.pi / ex10['T2']

K = 5
k_arr = np.arange(K + 1)
ex10['k'] = k_arr.tolist()

def calc_spectra(tu, T, w1):
    w_k = k_arr * w1
    A_k = np.zeros_like(w_k, dtype=float)
    Phi_k = np.zeros_like(w_k, dtype=float)
    
    def A_cont(w):
        w_safe = np.where(w == 0, 1e-10, w)
        val = (2 / T) * np.abs(4 * Im / w_safe * np.sin(w_safe * T / 8)**2)
        return np.where(w == 0, 0.0, val)
        
    def Phi_cont(w):
        phi_deg = np.degrees(np.pi / 2 - w * T / 4)
        return np.where(phi_deg > 0, phi_deg % 360, phi_deg % -360)
    
    for i in range(len(k_arr)):
        w = w_k[i]
        A_k[i] = A_cont(w)
        Phi_k[i] = Phi_cont(w)
        
    return w_k, A_k, Phi_k, A_cont, Phi_cont

w_k1, A_k1, Phi_k1, A_cont1, Phi_cont1 = calc_spectra(tu1, ex10['T1'], ex10['w1_1'])
w_k2, A_k2, Phi_k2, A_cont2, Phi_cont2 = calc_spectra(tu2, ex10['T2'], ex10['w1_2'])

ex10['tab_wk_1'] = w_k1.tolist()
ex10['tab_Ak_1'] = A_k1.tolist()
ex10['tab_Phik_1'] = Phi_k1.tolist()

ex10['tab_wk_2'] = w_k2.tolist()
ex10['tab_Ak_2'] = A_k2.tolist()
ex10['tab_Phik_2'] = Phi_k2.tolist()

def gen_fourier_str(A_k, Phi_k, w1):
    terms =[]
    for i in range(1, K + 1):
        if A_k[i] > 1e-4:
            term = f"{A_k[i]:.3f} \\cos({i * w1:.3f}t "
            if Phi_k[i] < 0:
                term += f"- {abs(Phi_k[i]):.3f}^\\circ)"
            else:
                term += f"+ {Phi_k[i]:.1f}^\\circ)"
            terms.append(term)
    if not terms:
        return "0"
    return " + ".join(terms)

ex10['fs_1'] = gen_fourier_str(A_k1, Phi_k1, ex10['w1_1'])
ex10['fs_2'] = gen_fourier_str(A_k2, Phi_k2, ex10['w1_2'])