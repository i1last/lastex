import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def generate_data():
    # Базовая длина для всех образцов
    l0 = 50.0  # мм
    
    # 1. Кожа (соответствует кривой 1)
    # F0 = w * h = 10 * 1.5 = 15 мм^2
    F0_leather = 15.0
    dl_leather = np.linspace(0, 26, 250)
    P_leather = np.piecewise(dl_leather, 
        [dl_leather <= 21, dl_leather > 21],[lambda x: 530 * (1 - (x - 21)**2 / 21**2), 
         lambda x: 530 - (530 - 250) * (x - 21)]
    )
    eps_leather = (dl_leather / l0) * 100
    sigma_leather = P_leather / F0_leather

    # 2. Веревка (соответствует кривой 2)
    # F0 = pi * d^2 / 4 = pi * 1.5^2 / 4 ≈ 1.767 мм^2
    F0_rope = np.pi * (1.5**2) / 4
    dl_rope = np.linspace(0, 22, 200)
    P_rope = np.piecewise(dl_rope, 
        [dl_rope <= 17, dl_rope > 17],[lambda x: 220 * (1 - (x - 17)**2 / 17**2), 
         lambda x: 220 - (220 - 170) * ((x - 17) / 5)**2]
    )
    eps_rope = (dl_rope / l0) * 100
    sigma_rope = P_rope / F0_rope

    # 3. Проволока (соответствует кривой 4)
    # F0 = pi * d^2 / 4 = pi * 0.5^2 / 4 ≈ 0.196 мм^2
    F0_wire = np.pi * (0.5**2) / 4
    dl_wire = np.linspace(0, 23, 300)
    P_wire = np.zeros_like(dl_wire)
    for i, x in enumerate(dl_wire):
        if x < 0.5:
            P_wire[i] = 300 * x
        elif x < 1.5:
            P_wire[i] = 150 - 25 * (x - 0.5)
        elif x < 8:
            P_wire[i] = 125 + 10 * (x - 1.5) / 6.5
        elif x < 21:
            P_wire[i] = 135 + 25 * np.sin(np.pi / 2 * (x - 8) / 13)
        else:
            P_wire[i] = 160 - 30 * ((x - 21) / 2)**2
            
    eps_wire = (dl_wire / l0) * 100
    sigma_wire = P_wire / F0_wire

    return (eps_leather, sigma_leather), (eps_rope, sigma_rope), (eps_wire, sigma_wire)


(eps_l, sig_l), (eps_r, sig_r), (eps_w, sig_w) = generate_data()

fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(eps_l, sig_l, ls='-', label='Кожа', color='tab:red', linewidth=1.5)
ax.plot(eps_r, sig_r, ls='--', label='Веревка', color='tab:brown', linewidth=1.5)
ax.plot(eps_w, sig_w, ls='-.', label='Проволока', color='tab:cyan', linewidth=1.5)

# Отметки точек разрыва
ax.plot(eps_l[-1], sig_l[-1], marker='^', color='black', markersize=5)
ax.plot(eps_r[-1], sig_r[-1], marker='o', color='black', markersize=5)
ax.plot(eps_w[-1], sig_w[-1], marker='s', color='black', markersize=5)

ax.set_xlabel(r'Относительная деформация $\varepsilon$, \%')
ax.set_ylabel(r'Условное напряжение $\sigma$, МПа')
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.legend(loc='upper right', frameon=True, edgecolor='black')

plt.tight_layout()
plt.savefig('stress-strain-plot.pgf', bbox_inches='tight')
plt.close()