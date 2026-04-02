import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_6 import ex6, reaction

# Определение временного интервала (должен охватывать импульс и затухание)
t_max = ex6['tu'] * 3
t = np.linspace(-1, t_max, 1000)

y_reaction = np.array([reaction(tau) for tau in t])
y_input = np.where((t >= 0) & (t <= ex6['tu']), ex6['Im'], 0)

plt.figure()
plt.plot(t, y_input, marker='', label=r'Входной импульс $i_1(t)$')
plt.plot(t, y_reaction, marker='', label=r'Реакция цепи $i_2(t)$')
plt.xlabel(r'$t$, с')
plt.ylabel(r'Ток, А')
plt.legend(ncol=2)
plt.savefig('plot_reaction.pgf')