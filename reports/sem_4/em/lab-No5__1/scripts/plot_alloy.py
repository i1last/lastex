import matplotlib.pyplot as plt
from scripts.calc import r

fig, ax1 = plt.subplots()

ax1.set_xlabel(r'Массовая доля никеля $x_{\text{Ni}}$')
ax1.set_ylabel(r'$\rho$, Ом$\cdot$м')
l1 = ax1.plot(r['x_Ni'], r['rho_alloy'], marker='o', label=r'$\rho$')

ax2 = ax1.twinx()
ax2.set_ylabel(r'$\alpha_\rho$, К$^{-1}$')
ax2.spines['right'].set_visible(True)
l2 = ax2.plot(r['x_Ni'], r['alpha_rho_alloy'], marker='s', color='C2', linestyle='--', label=r'$\alpha_\rho$')
l3 = ax2.plot([0.4], [r['alpha_rho_Const'][0]], marker='*', markersize=10, linestyle='None', label=r'$\alpha_\rho$ (эксп. константан)')

lines = l1 + l2 + l3
labels =[l.get_label() for l in lines]
ax1.legend(lines, labels, ncol=3, numpoints=1)

plt.savefig('plot_alloy.pgf')