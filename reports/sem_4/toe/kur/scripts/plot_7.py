import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_6 import ex6
from scripts.calc_7 import ex7

Im = ex6['Im']
tu = ex6['tu']

# Формирование массива частот до 4-го нуля спектра
w_max = 4 * ex7['w_y1']
w = np.linspace(1e-5, w_max, 1000)
w = np.insert(w, 0, 0)

A1 = np.zeros_like(w)
Phi1 = np.zeros_like(w) # Здесь будем хранить в градусах

A1[0] = ex7['A1_0']
Phi1[0] = 0

for i in range(1, len(w)):
    val = (2 * Im / w[i]) * np.sin(w[i] * tu / 2)
    A1[i] = np.abs(val)
    
    # Расчет фазы в радианах с последующим переводом в градусы
    if val >= 0:
        p_rad  = -w[i] * tu / 2
    else:
        p_rad  = np.pi - w[i] * tu / 2
    
    p_deg = np.degrees(p_rad)
    Phi1[i] = np.remainder(p_deg, -360)

# График амплитудного спектра
plt.figure()
plt.plot(w, A1, marker='')
plt.axhline(0.1 * ex7['A1_0'], linestyle='--', label='10% уровень')
plt.axvline(ex7['w_sp'], linestyle=':', label=r'$\Delta\omega_{\text{сп}}$')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A_1(\omega)$')
plt.legend(ncol=2)
plt.grid(True)
plt.savefig('plot_spec_A.pgf')

# График фазового спектра
plt.figure()
plt.plot(w, Phi1, marker='')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi_1(\omega)$, {}^\circ')
plt.grid(True)
plt.yticks(np.arange(-180, 90, 90)) 
plt.savefig('plot_spec_Phi.pgf')