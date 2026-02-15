import matplotlib.pyplot as plt
import numpy as np

def setup_plot(title):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.set_xlabel(r'$\text{Re}(p), \times 10^3 \text{ c}^{-1}$')
    ax.set_ylabel(r'$\text{Im}(p), \times 10^3 \text{ c}^{-1}$')
    ax.set_title(title)
    return fig, ax

# --- График 1: Цепь второго порядка (3 режима) ---
fig1, ax1 = setup_plot('')

# Данные (деленные на 1000)
# 1. Колебательный (R=0.5k): p = -10 +/- j43.6
re_osc = [-10, -10]
im_osc = [43.6, -43.6]
ax1.plot(re_osc, im_osc, 'rx', markeredgewidth=2, markersize=8, label=r'Колеб. ($R_1=0.5$ кОм)')

# 2. Апериодический (R=3k): p = -20, -100
re_aper = [-20, -100]
im_aper = [0, 0]
ax1.plot(re_aper, im_aper, 'bo', fillstyle='none', markeredgewidth=2, markersize=8, label=r'Апериод. ($R_1=3$ кОм)')

# 3. Критический (теория): p = -44.7
re_crit = [-44.7]
im_crit = [0]
ax1.plot(re_crit, im_crit, 'gs', fillstyle='none', markeredgewidth=2, markersize=8, label=r'Крит. ($R_{kp} \approx 2.2$ кОм)')

ax1.legend()
fig1.tight_layout()
fig1.savefig('b.pgf')

