import numpy as np
from scripts.calc_10 import ex10, calc_spectra
from scripts.calc_8 import get_H

ex11 = {}
K = 5

def calc_out_spectra(tu, T, w1):
    w_k, A_k_in, Phi_k_in, A_cont_in, Phi_cont_in = calc_spectra(tu, T, w1)
    
    def A_cont_out(w):
        H_val = get_H(w)
        return A_cont_in(w) * np.abs(H_val)
        
    def Phi_cont_out(w):
        H_val = get_H(w)
        phi_in_deg = Phi_cont_in(w)
        phi_H_deg = np.degrees(np.angle(H_val))
        phi_out_deg = phi_in_deg + phi_H_deg
        return (phi_out_deg + 180) % 360 - 180
    
    A_k_out = np.zeros_like(w_k, dtype=float)
    Phi_k_out = np.zeros_like(w_k, dtype=float)
    
    for i in range(len(w_k)):
        w = w_k[i]
        A_k_out[i] = A_cont_out(w)
        Phi_k_out[i] = Phi_cont_out(w)
        
    return w_k, A_k_out, Phi_k_out, A_cont_out, Phi_cont_out

w_k1, A_k1_out, Phi_k1_out, A_cont1_out, Phi_cont1_out = calc_out_spectra(ex10['tu1'], ex10['T1'], ex10['w1_1'])
w_k2, A_k2_out, Phi_k2_out, A_cont2_out, Phi_cont2_out = calc_out_spectra(ex10['tu2'], ex10['T2'], ex10['w1_2'])

ex11['tab_wk_1'] = w_k1.tolist()
ex11['tab_Ak_1'] = A_k1_out.tolist()
ex11['tab_Phik_1'] = Phi_k1_out.tolist()

ex11['tab_wk_2'] = w_k2.tolist()
ex11['tab_Ak_2'] = A_k2_out.tolist()
ex11['tab_Phik_2'] = Phi_k2_out.tolist()

def gen_fourier_str(A_k, Phi_k, w1):
    terms = []
    if A_k[0] > 1e-4:
        terms.append(f"{A_k[0]:.3f}")
        
    for i in range(1, K + 1):
        if A_k[i] > 1e-4:
            term = f"{A_k[i]:.3f} \\cos({i * w1:.3f}t "
            if Phi_k[i] < 0:
                term += f"- {abs(Phi_k[i]):.3f}^\\circ)"
            else:
                term += f"+ {Phi_k[i]:.3f}^\\circ)"
            terms.append(term)
            
    if not terms:
        return "0"
    return " + ".join(terms)

ex11['fs_1'] = gen_fourier_str(A_k1_out, Phi_k1_out, ex10['w1_1'])
ex11['fs_2'] = gen_fourier_str(A_k2_out, Phi_k2_out, ex10['w1_2'])