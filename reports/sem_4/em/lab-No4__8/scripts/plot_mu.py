import matplotlib.pyplot as plt
from scripts.calc import r

plt.plot(r['tab2'][0], r['mu_ef'], label='$\\mu_{эф}$')
plt.xlabel('$f$, Гц')
plt.ylabel('$\\mu_{эф}$')
plt.legend(ncol=1)

plt.savefig('plot_mu.pgf')