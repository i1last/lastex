import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_6 import reaction
from scripts.calc_10 import ex10
from scripts.calc_11 import calc_out_spectra
from scripts.calc_12 import get_exact_response

tu1 = ex10['tu1']
tu2 = ex10['tu2']
T1 = ex10['T1']
T2 = ex10['T2']
w1_1 = ex10['w1_1']
w1_2 = ex10['w1_2']

def plot_comparison(tu, T, w1, prefix):
    # Получение спектра выходного сигнала из расчетов 11 пункта
    _, A_k_out, Phi_k_out, _, _ = calc_out_spectra(tu, T, w1)
    
    t = np.linspace(-0.2 * T, 1.2 * T, 1000)
    
    # Точное решение из п. 6
    y_exact = np.array([reaction(t_i, tu) for t_i in t])

    # Замкнутая форма
    y_zamk = get_exact_response(t, T)
    
    # Приближение отрезком ряда Фурье
    y_fourier = np.zeros_like(t)
    for i in range(len(A_k_out)):
        if A_k_out[i] > 1e-4:
            y_fourier += A_k_out[i] * np.cos(i * w1 * t + np.radians(Phi_k_out[i]))
            
    plt.figure()
    plt.plot(t, y_zamk, marker='', label='Замкнутая форма')
    plt.plot(t, y_fourier, marker='', label='Ряд Фурье (п. 11)')
    plt.plot(t, y_exact, marker='', label='Точный расчет (п. 6)')
    
    plt.xlim(left=min(t))
    plt.xlabel(r'$t$')
    plt.ylabel(r'$i_{\mathrm{н}}(t)$')
    plt.legend(ncol=3)
    plt.grid()
    plt.tight_layout()
    plt.savefig(f'plot_exact_vs_fourier_{prefix}.pgf')

plot_comparison(tu1, T1, w1_1, '1')
plot_comparison(tu2, T2, w1_2, '2')