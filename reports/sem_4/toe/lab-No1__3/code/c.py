import matplotlib.pyplot as plt


def setup_plot(title):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.set_xlabel(r'$\text{Re}(p), \times 10^3 \text{ c}^{-1}$')
    ax.set_ylabel(r'$\text{Im}(p), \times 10^3 \text{ c}^{-1}$')
    ax.set_title(title)
    return fig, ax
# --- График 2: Цепь третьего порядка ---
fig2, ax2 = setup_plot('')

# Данные (деленные на 1000)
# Вещественный корень: p1 = -10
# Комплексные корни: p2,3 = -25 +/- j61.4
re_3rd = [-10, -25, -25]
im_3rd = [0, 61.4, -61.4]

ax2.plot([-10], [0], 'bo', markeredgewidth=2, markersize=8, label=r'$p_1$ (RC-цепь)')
ax2.plot([-25, -25], [61.4, -61.4], 'rx', markeredgewidth=2, markersize=8, label=r'$p_{2,3}$ (RLC-контур)')

# Дополнительные линии для наглядности сопряженных корней
ax2.plot([-25, -25], [-61.4, 61.4], 'r--', alpha=0.3)

ax2.legend()
fig2.tight_layout()
fig2.savefig('c.pgf')