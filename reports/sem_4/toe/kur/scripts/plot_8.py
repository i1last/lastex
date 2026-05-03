import numpy as np
import matplotlib.pyplot as plt
from scripts.source import s
from scripts.calc_1 import n
from scripts.calc_8 import get_H, get_I1

Im = s['Im']
tu1 = n['ti1']
tu2 = n['ti2']

def plot_reaction_spectra(tu, suffix):
    # Определение диапазона частот для построения (до 4-го нуля спектра)
    w_max = 4 * (4 * np.pi / (2*tu))
    w = np.linspace(0, w_max, 2000)

    # Вычисление спектра реакции I2(jw) = I1(jw) * H(jw)
    H = get_H(w)
    I1 = get_I1(w, tu)
    I2 = I1 * H

    A2 = np.abs(I2)
    phi_raw = np.degrees(
        np.unwrap(
            np.angle(I2)
        )
    )
    Phi2_deg = np.where(phi_raw > 0, phi_raw % 360, phi_raw % -360)

    # График амплитудного спектра реакции
    plt.figure()
    plt.plot(w, A2, marker='')
    plt.xlim(left=min(w))
    plt.ylim(bottom=min(A2))
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$A_2(\omega)$')
    plt.savefig(f'plot_spec_A2_{suffix}.pgf')

    # График фазового спектра реакции
    plt.figure()
    plt.plot(w, Phi2_deg, marker='')
    plt.xlim(left=min(w))
    plt.yticks(np.arange(90, -361, -45))
    plt.xlabel(r'$\omega$')
    plt.ylabel(r'$\Phi_2(\omega), ^\circ$')
    plt.savefig(f'plot_spec_Phi2_{suffix}.pgf')

# Генерация графиков для двух длительностей
plot_reaction_spectra(tu1, '1')
plot_reaction_spectra(tu2, '2')

# plt.show()