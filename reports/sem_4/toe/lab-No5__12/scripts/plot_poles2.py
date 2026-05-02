# scripts/plot_poles2.py
import matplotlib.pyplot as plt
from scripts.calc import r

labels =['4 кОм (колеб.)', '0.67 кОм (крит.)', '0.1 кОм (апер.)']

for i in range(3):
    plt.plot([r['part2']['p1_real'][i], r['part2']['p2_real'][i]],
             [r['part2']['p1_imag'][i], r['part2']['p2_imag'][i]],
             marker='x', markersize=12, linestyle='None', label=labels[i])

plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

plt.xlabel('Re, с$^{-1}$')
plt.ylabel('Im, с$^{-1}$')
plt.legend(ncol=3)

plt.savefig('poles2.pgf')