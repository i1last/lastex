import matplotlib.pyplot as plt
from scripts.calc import r

plt.figure()
plt.plot(r['em']['Uavg'], r['em']['delta_avg'], label=r'$\delta$')
plt.plot(r['em']['Uavg'], r['em']['gamma_avg'], label=r'$\gamma$')
plt.xlabel(r'$U_{\text{ср}}$, В')
plt.ylabel('Погрешность, %')
plt.legend(ncol=2)
plt.savefig('plot_error.pgf')