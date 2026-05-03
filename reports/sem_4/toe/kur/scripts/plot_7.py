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
    # Чтобы избежать деления на 0, используем малую добавку для расчетов
    w_safe = np.where(w == 0, 1e-20, w)
    
    # Амплитудный спектр по формуле (7.2)
    A1 = np.abs(4 * Im / w_safe * np.sin(w_safe * 2*ti / 4)**2)
    A1[w == 0] = 0  # В нуле амплитуда 0, так как площадь меандра = 0
    
    # Фазовый спектр по формуле (7.3)
    phi_raw = 90 - np.degrees(w * 2*ti / 2)
    Phi1 = np.where(phi_raw > 0, phi_raw % 360, phi_raw % -360)
            
    return A1, Phi1

A1_1, Phi1_1 = compute_spectra(ti1, w1)
A1_2, Phi1_2 = compute_spectra(ti2, w2)

# --- График амплитудного спектра ti1 ---
plt.figure()
plt.plot(w1, A1_1, label=rf'$A_1(\omega)$ при $t_\mathrm{{и}}={ti1}$', marker='')
plt.xlim(left=0)
plt.ylim(bottom=0)
target1 = 0.1 * np.max(A1_1)
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
target2 = 0.1 * np.max(A1_2)
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
plt.yticks(np.arange(90, -361, -45))
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
plt.yticks(np.arange(90, -361, -45))
plt.tight_layout()
plt.savefig('plot_spec_Phi_ti2.pgf')

# plt.show()