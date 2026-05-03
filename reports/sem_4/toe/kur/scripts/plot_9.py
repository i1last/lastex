import numpy as np
import matplotlib.pyplot as plt
from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_6 import reaction
from scripts.calc_8 import get_H, get_I1

Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']

def get_approx_reaction(tu, t_arr):
    # Расчет спектра реакции на меандр
    w_max = 100.0 / tu
    N_w = 5000
    w_arr = np.linspace(0, w_max, N_w)
    
    H_w = get_H(w_arr)
    w_safe = np.where(w_arr == 0, 1e-10, w_arr)
    I1_w = get_I1(w_safe, tu)
    
    I2_w = I1_w * H_w
    A2 = np.abs(I2_w)
    Phi2 = np.angle(I2_w)
    
    # Численное интегрирование
    i2_approx = np.zeros_like(t_arr)
    for i, t in enumerate(t_arr):
        integrand = A2 * np.cos(w_arr * t + Phi2)
        i2_approx[i] = np.trapz(integrand, w_arr) / np.pi
        
    return i2_approx

def plot_comparison(tu, suffix):
    t_max = 2 * tu
    t_arr = np.linspace(-0.05, t_max, 500)
    
    i2_approx = get_approx_reaction(tu, t_arr)
    i2_exact = np.array([reaction(t, tu) for t in t_arr])
    
    plt.figure()
    plt.plot(t_arr, i2_approx, marker='', label='Приближенный расчет по спектру')
    plt.plot(t_arr, i2_exact, marker='', label=fr'Точный расчет (разд. 6). $t_\mathrm{{и}}={tu}$')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$i_2(t)$')
    plt.legend(ncol=2)
    plt.xlim(left=0)
    plt.savefig(f'plot_approx_reaction_{suffix}.pgf')

# Генерация двух графиков
plot_comparison(tu1, '1')
plot_comparison(tu2, '2')

# plt.show()