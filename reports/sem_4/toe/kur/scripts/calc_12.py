import numpy as np
import scipy.signal as sig
from scripts.source import s
from scripts.calc_8 import tf

ex12 = {}
Im = s['Im']
ex12['Im'] = Im

# Извлечение коэффициентов передаточной функции и удаление ведущих нулей
num_arr = np.array([tf.get('N3', 0), tf.get('N2', 0), tf.get('N1', 0), tf.get('N0', 0)], dtype=float)
den_arr = np.array([tf.get('D3', 0), tf.get('D2', 0), tf.get('D1', 0), tf.get('D0', 0)], dtype=float)

num_arr = np.trim_zeros(num_arr, 'f')
den_arr = np.trim_zeros(den_arr, 'f')
if len(num_arr) == 0:
    num_arr = np.array([0.0])

# Вычисление вычетов (R_k), полюсов (p_k) и прямой передачи H(inf)
residues, poles, direct = sig.residue(num_arr, den_arr)

ex12['H_inf'] = direct[0] if len(direct) > 0 else 0.0
ex12['poles_real'] = np.real(poles).tolist()
ex12['poles_imag'] = np.imag(poles).tolist()
ex12['res_real'] = np.real(residues).tolist()
ex12['res_imag'] = np.imag(residues).tolist()
ex12['k_indices'] = list(range(1, len(poles) + 1))

def get_exact_response(t_array, T):
    """
    Вычисление точного аналитического решения в замкнутой форме 
    для установившейся реакции на двуполярный меандр.
    """
    y = np.zeros_like(t_array, dtype=float)
    D_val = direct[0] if len(direct) > 0 else 0.0
    
    for idx, t in enumerate(t_array):
        t_mod = t % T
        is_negative_half = t_mod >= T / 2
        tau = t_mod if not is_negative_half else t_mod - T / 2
        
        val = D_val
        for A, p in zip(residues, poles):
            # Обработка возможного нулевого полюса (идеальный интегратор)
            if abs(p) < 1e-9:
                term = A * (tau - T / 4)
            else:
                term = (A / p) * ( (2 * np.exp(p * tau)) / (1 + np.exp(p * T / 2)) - 1 )
            
            # Сумма сопряженных комплексных полюсов дает строго вещественный результат
            val += np.real(term)
        
        val *= Im
        if is_negative_half:
            val = -val
            
        y[idx] = val
        
    return y