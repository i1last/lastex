import matplotlib.pyplot as plt
from scripts.calc import r

fig, ax1 = plt.subplots()

line1 = ax1.plot(r['H_m'], r['B_m'], marker='o', label='$B_m$')
ax1.set_xlabel('$H_m$, А/м')
ax1.set_ylabel('$B_m$, Тл')

ax2 = ax1.twinx()
ax2.spines['right'].set_visible(True)
line2 = ax2.plot(r['H_m'], r['mu_st'], marker='s', color='C1', label='$\\mu_{ст}$')
ax2.set_ylabel('$\\mu_{ст}$')

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, ncol=2)

ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)
ax2.set_ylim(bottom=0)

plt.savefig('plot_mc.pgf')