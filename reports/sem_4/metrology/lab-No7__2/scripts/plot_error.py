import matplotlib.pyplot as plt
from scripts.calc import r
import numpy as np

plt.figure()
plt.plot(r['em']['Uavg'], r['em']['delta_avg'], label=r'$\delta$')
plt.plot(r['em']['Uavg'], r['em']['gamma_avg'], label=r'$\gamma$')
plt.xticks(np.round(r['em']['Uavg'], 2))
y_ticks = r['em']['delta_avg'] + r['em']['gamma_avg']
plt.yticks(np.arange(min(y_ticks), max(y_ticks) + 0.2, 0.5))
plt.xlabel(r'$U_{\text{ср}}$, В')
plt.ylabel('Погрешность, %')
plt.legend(ncol=2)
plt.savefig('plot_error.pgf')
# plt.show()