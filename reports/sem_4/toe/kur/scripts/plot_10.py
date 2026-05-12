import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_10 import ex10, calc_spectra
from scripts.source import s
from scripts.calc_1 import n

Im = s['Im']
tu1 = ex10['tu1']
tu2 = ex10['tu2']
T1 = ex10['T1']
T2 = ex10['T2']
w1_1 = ex10['w1_1']
w1_2 = ex10['w1_2']

w_k1, A_k1, Phi_k1, A_cont1, Phi_cont1 = calc_spectra(tu1, T1, w1_1)
w_k2, A_k2, Phi_k2, A_cont2, Phi_cont2 = calc_spectra(tu2, T2, w1_2)

def plot_spectra(w_k, A_k, Phi_k, A_cont, Phi_cont, w1, prefix):
    w_dense = np.linspace(0, max(w_k) * 1.1, 500)
    
    # Амплитудный спектр
    plt.figure()
    plt.plot(w_dense, A_cont(w_dense), 'r--', label=r'Огибающая $\frac{2}{T}A(\omega)$')
    plt.stem(w_k, A_k, linefmt='b-', markerfmt='bo', basefmt='k-')
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$A_{\mathrm{вх}}(\omega)$')
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.xticks(w_k, [r'$0$'] +[rf'${i}\omega_1$' for i in range(1, len(w_k))])
    plt.grid()
    plt.legend()
    plt.savefig(f'plot_disc_spec_A_{prefix}.pgf')
    
    # Фазовый спектр
    plt.figure()
    plt.plot(w_dense, Phi_cont(w_dense), 'r--', label=r'Огибающая $\Phi(\omega)$')
    plt.stem(w_k, Phi_k, linefmt='b-', markerfmt='bo', basefmt='k-')
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$\Phi_{\mathrm{вх}}(\omega), ^\circ$')
    plt.xlim(left=-0.01)
    plt.xticks(w_k, [r'$0$'] +[rf'${i}\omega_1$' for i in range(1, len(w_k))])
    plt.yticks(np.arange(90, -361, -90))
    plt.grid()
    plt.legend()
    plt.savefig(f'plot_disc_spec_Phi_{prefix}.pgf')

plot_spectra(w_k1, A_k1, Phi_k1, A_cont1, Phi_cont1, w1_1, '1')
plot_spectra(w_k2, A_k2, Phi_k2, A_cont2, Phi_cont2, w1_2, '2')

def plot_approx(tu, T, w1, A_k, Phi_k, prefix):
    t = np.linspace(-0.2 * T, 1.2 * T, 1000)
    
    # Формирование идеального меандра
    t_mod = t % T
    y_input = np.piecewise(t_mod,
        [
            (t_mod < T / 4),
            (t_mod >= T / 4) & (t_mod < T / 2),
            (t_mod >= T / 2)
        ],
        [Im, -Im, 0]
    )
    
    y_approx = np.zeros_like(t)
    harmonics = []
    for i in range(1, len(A_k)):
        if A_k[i] > 1e-4:
            harm = A_k[i] * np.cos(i * w1 * t + np.radians(Phi_k[i]))
            y_approx += harm
            harmonics.append(harm)
            
    plt.figure()
    plt.plot(t, y_input, marker='', label='Исходный сигнал')
    plt.plot(t, y_approx, marker='', label='Аппроксимация')
    
    colors =['c', 'm', 'y', 'g', 'b']
    for i, harm in enumerate(harmonics):
        plt.plot(t, harm, color=colors[i % len(colors)], marker='', linestyle='-', linewidth=1)
        
    plt.xlim(left=(-0.05 * T))
    plt.xlabel(r'$t$')
    plt.ylabel(r'$i_0(t)$')
    plt.legend(ncol=2)
    plt.grid()
    plt.savefig(f'plot_fourier_approx_{prefix}.pgf')

plot_approx(tu1, T1, w1_1, A_k1, Phi_k1, '1')
plot_approx(tu2, T2, w1_2, A_k2, Phi_k2, '2')

# plt.show()