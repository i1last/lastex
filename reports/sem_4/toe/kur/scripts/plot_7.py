import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scripts.calc_6 import ex6
from scripts.calc_7 import ex7
from scripts.calc_1 import n

Im = ex6['Im']
ti1 = n['ti1']
ti2 = n['ti2']

# Формирование массива частот. 
# Максимальная частота определяется по самому короткому импульсу (ti2), 
# так как его спектр самый широкий. Берем до 4-го нуля спектра ti2.
w_max1 = 5 * ex7['ti1']['w_y1']
w_max2 = 5 * ex7['ti2']['w_y1']
w1 = np.linspace(1e-5, w_max1, 2000)
w1 = np.insert(w1, 0, 0)
w2 = np.linspace(1e-5, w_max2, 2000)
w2 = np.insert(w2, 0, 0)

def compute_spectra(ti, w):
    A1 = np.zeros_like(w)
    Phi1 = np.zeros_like(w)
    
    A1[0] = Im * ti
    Phi1[0] = 0
    
    for i in range(1, len(w)):
        val = (2 * Im / w[i]) * np.sin(w[i] * ti / 2)
        A1[i] = np.abs(val)
        
        # Расчет фазы в радианах
        if val >= 0:
            p_rad = -w[i] * ti / 2
        else:
            p_rad = np.pi - w[i] * ti / 2
        
        # Перевод в градусы и приведение к диапазону (-360, 0]
        p_deg = np.degrees(p_rad)
        Phi1[i] = np.remainder(p_deg, -360)
        
        # Устранение вертикальных линий сшивки на графике фазы (замена скачков на NaN)
        if i > 1 and np.abs(Phi1[i] - Phi1[i-1]) > 180:
            Phi1[i-1] = np.nan
            
    return A1, Phi1

A1_1, Phi1_1 = compute_spectra(ti1, w1)
A1_2, Phi1_2 = compute_spectra(ti2, w2)

# --- График амплитудного спектра ti1 ---
plt.figure()
plt.plot(w1, A1_1, label=rf'$A_1(\omega)$ при $t_\mathrm{{и}}={ti1}$', marker='')
plt.xlim(left=0)
plt.ylim(bottom=0)
target1 = 0.1 * ex7['ti1']['A1_0']
plt.axhline(target1, linestyle='--', alpha=0.5)
peaks1, _ = find_peaks(A1_1)
idx_peak1 = peaks1[np.argmin(np.abs(A1_1[peaks1] - target1))]
w_sp1_visual = w1[idx_peak1]
plt.axvline(w_sp1_visual, linestyle=':', label=r'$\Delta\omega_{\mathrm{сп1}}$')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A_1(\omega)$')
plt.legend(ncol=2)
plt.grid(True)
plt.tight_layout()
plt.savefig('plot_spec_A_ti1.pgf')

# --- График амплитудного спектра ti2 ---
plt.figure()
plt.plot(w2, A1_2, label=rf'$A_1(\omega)$ при $t_\mathrm{{и}}={ti2}$', marker='')
plt.xlim(left=0)
plt.ylim(bottom=0)
target2 = 0.1 * ex7['ti2']['A1_0']
plt.axhline(target2, linestyle='--', alpha=0.5)
peaks2, _ = find_peaks(A1_2)
idx_peak2 = peaks2[np.argmin(np.abs(A1_2[peaks2] - target2))]
w_sp2_visual = w2[idx_peak2]
plt.axvline(w_sp2_visual, linestyle=':', label=r'$\Delta\omega_{\mathrm{сп2}}$')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A_1(\omega)$')
plt.legend(ncol=2)
plt.grid(True)
plt.tight_layout()
plt.savefig('plot_spec_A_ti2.pgf')

# --- График фазового спектра ti1 ---
plt.figure()
plt.plot(w1, Phi1_1, label=rf'$\Phi_1(\omega)$ при $t_\mathrm{{и}}={ti1}$', marker='')
plt.xlim(left=0)
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi_1(\omega), ^\circ$')
plt.legend()
plt.grid(True)
plt.yticks(np.arange(0, -181, -45))
plt.tight_layout()
plt.savefig('plot_spec_Phi_ti1.pgf')

# --- График фазового спектра ti2 ---
plt.figure()
plt.plot(w2, Phi1_2, label=rf'$\Phi_1(\omega)$ при $t_\mathrm{{и}}={ti2}$', marker='')
plt.xlim(left=0)
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi_1(\omega), ^\circ$')
plt.legend()
plt.grid(True)
plt.yticks(np.arange(0, -181, -45))
plt.tight_layout()
plt.savefig('plot_spec_Phi_ti2.pgf')

# plt.show()