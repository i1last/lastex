import numpy as np
from scripts.source import s
from scripts.calc_1 import n

ex10 = {}
Im = s['Im']
tu = n['ti1'] # Используем первую длительность, как основную
T = 2 * tu # Период для меандра
ex10['T'] = T
ex10['w1'] = 2 * np.pi / T

# Количество гармоник для аппроксимации (0, 1, 3, 5)
ex10['N'] = 5
harmonics = [k for k in range(ex10['N'] + 1) if k % 2 != 0 or k == 0]
ex10['harmonics'] = harmonics

# Массивы для дискретного спектра
ex10['k'] = []
ex10['A1k'] = []
ex10['Phi1k_deg'] = []

# Вычисление коэффициентов ряда Фурье для двуполярного меандра
# A1k = 2/T * A1(k*w1), Phi1k = Phi1(k*w1)
# Аналитическое решение для меандра:
# A0 = 0
# Ak = 4*Im / (k*pi) for odd k
# Phi_k = 0 for odd k
ex10['A1_0'] = 0.0 # Постоянная составляющая для симметричного меандра

for k in harmonics:
    ex10['k'].append(k)
    if k == 0:
        A1k_val = ex10['A1_0']
        Phi1k_val_deg = 0.0
    else:
        A1k_val = (4 * Im) / (k * np.pi)
        Phi1k_val_deg = 0.0
    
    ex10['A1k'].append(A1k_val)
    ex10['Phi1k_deg'].append(Phi1k_val_deg)

# Генерация выражения для ряда Фурье
fourier_terms = []
for k_val, A_val, Phi_val in zip(ex10['k'], ex10['A1k'], ex10['Phi1k_deg']):
    if k_val != 0:
        term = f"{A_val:.3f} \\cos({k_val * ex10['w1']:.3f}t + {Phi_val:.1f}^\\circ)"
        fourier_terms.append(term)

ex10['fourier_series_str'] = f"i_1(t) \\approx {ex10['A1_0']:.3f} + " + " + ".join(fourier_terms)