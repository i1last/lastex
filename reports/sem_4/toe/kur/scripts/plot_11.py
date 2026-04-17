import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_10 import ex10, calc_spectra
from scripts.calc_11 import calc_out_spectra
from scripts.source import s

tu1 = ex10['tu1']
tu2 = ex10['tu2']
T1 = ex10['T1']
T2 = ex10['T2']
w1_1 = ex10['w1_1']
w1_2 = ex10['w1_2']
Im = s['Im']

w_k1, A_k1_out, Phi_k1_out, A_cont1_out, Phi_cont1_out = calc_out_spectra(tu1, T1, w1_1)
w_k2, A_k2_out, Phi_k2_out, A_cont2_out, Phi_cont2_out = calc_out_spectra(tu2, T2, w1_2)

_, A_k1_in, Phi_k1_in, _, _ = calc_spectra(tu1, T1, w1_1)
_, A_k2_in, Phi_k2_in, _, _ = calc_spectra(tu2, T2, w1_2)

def plot_spectra_out(w_k, A_k, Phi_k, A_cont, Phi_cont, w1, prefix):
    w_dense = np.linspace(0, max(w_k) * 1.1, 500)
    
    # Амплитудный спектр
    plt.figure()
    plt.plot(w_dense, A_cont(w_dense), 'r--', label=r'Огибающая $A_{\mathrm{вых}}(\omega)$')
    plt.stem(w_k, A_k, linefmt='b-', markerfmt='bo', basefmt='k-')
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$A_{\mathrm{вых}}(\omega)$')
    plt.xlim(left=-0.01)
    plt.ylim(bottom=0)
    plt.xticks(w_k, [r'$0$'] +[rf'${i}\omega_1$' for i in range(1, len(w_k))])
    plt.grid()
    plt.legend()
    plt.savefig(f'plot_disc_spec_A_out_{prefix}.pgf')
    
    # Фазовый спектр
    plt.figure()
    plt.plot(w_dense, Phi_cont(w_dense), 'r--', label=r'Огибающая $\Phi_{\mathrm{вых}}(\omega)$')
    plt.stem(w_k, Phi_k, linefmt='b-', markerfmt='bo', basefmt='k-')
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$\Phi_{\mathrm{вых}}(\omega), ^\circ$')
    plt.xlim(left=-0.01)
    plt.xticks(w_k,[r'$0$'] +[rf'${i}\omega_1$' for i in range(1, len(w_k))])
    plt.grid()
    plt.legend()
    plt.savefig(f'plot_disc_spec_Phi_out_{prefix}.pgf')

plot_spectra_out(w_k1, A_k1_out, Phi_k1_out, A_cont1_out, Phi_cont1_out, w1_1, '1')
plot_spectra_out(w_k2, A_k2_out, Phi_k2_out, A_cont2_out, Phi_cont2_out, w1_2, '2')

def plot_approx_out(tu, T, w1, A_k_in, Phi_k_in, A_k_out, Phi_k_out, prefix):
    t = np.linspace(-0.2 * T, 1.2 * T, 1000)

    # Формирование идеального меандра
    t_mod = t % T
    y_input = np.piecewise(t_mod,[
            (t_mod < tu / 2),
            (t_mod >= tu / 2)
        ],[Im, -Im]
    )
    
    # Входной РФ (аппроксимация)
    y_in_approx = np.zeros_like(t)
    for i in range(len(A_k_in)):
        if A_k_in[i] > 1e-4:
            y_in_approx += A_k_in[i] * np.cos(i * w1 * t + np.radians(Phi_k_in[i]))
            
    # Выходной РФ (реакция)
    y_out_approx = np.zeros_like(t)
    harmonics_out =[]
    for i in range(len(A_k_out)):
        if A_k_out[i] > 1e-4:
            harm = A_k_out[i] * np.cos(i * w1 * t + np.radians(Phi_k_out[i]))
            y_out_approx += harm
            harmonics_out.append(harm)
            
    plt.figure()
    plt.plot(t, y_input, marker='', linestyle='--', label='Исходный сигнал')
    plt.plot(t, y_in_approx, marker='', linestyle='-', label='Входной РФ')
    plt.plot(t, y_out_approx, marker='', linestyle='-.',label='Выходной РФ')
    
    colors = ['c', 'm', 'y', 'g', 'b']
    for i, harm in enumerate(harmonics_out):
        plt.plot(t, harm, color=colors[i % len(colors)], marker='', linestyle='-', linewidth=1)
    
    plt.xlim(left=(-0.05 * T))
    plt.xlabel(r'$t$')
    plt.ylabel(r'$i_{\mathrm{н}}(t)$')
    plt.legend(ncol=3)
    plt.grid()
    plt.savefig(f'plot_fourier_approx_out_{prefix}.pgf')

plot_approx_out(tu1, T1, w1_1, A_k1_in, Phi_k1_in, A_k1_out, Phi_k1_out, '1')
plot_approx_out(tu2, T2, w1_2, A_k2_in, Phi_k2_in, A_k2_out, Phi_k2_out, '2')