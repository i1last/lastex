# scripts/plot_poles1.py
import matplotlib.pyplot as plt
from scripts.calc import r

plt.plot([r['part1']['p1']], [0], marker='x',markersize=12, linestyle='None', label='Полюс $p_1$')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

plt.xlabel('Re, с$^{-1}$')
plt.ylabel('Im, с$^{-1}$')
plt.legend(ncol=1)

plt.savefig('poles1.pgf')