import matplotlib.pyplot as plt
from scripts.calc import p, r

plt.plot(p['rt']['t'], r['alpha_rho_Ni'], label='Никель', marker='o')
plt.xlabel(r'$t$, $^\circ$C')
plt.ylabel(r'$\alpha_\rho$, К$^{-1}$')
plt.legend(ncol=1)
plt.savefig('plot_alpha_Ni.pgf')
plt.close()


plt.plot(p['rt']['t'], r['alpha_rho_Cu'], label='Медь', marker='s')
plt.xlabel(r'$t$, $^\circ$C')
plt.ylabel(r'$\alpha_\rho$, К$^{-1}$')
plt.legend(ncol=1)
plt.savefig('plot_alpha_Cu.pgf')
plt.close()


plt.plot(p['rt']['t'], r['alpha_rho_Const'], label='Константан', marker='^')
plt.xlabel(r'$t$, $^\circ$C')
plt.ylabel(r'$\alpha_\rho$, К$^{-1}$')
plt.legend(ncol=1)
plt.savefig('plot_alpha_Const.pgf')
plt.close()