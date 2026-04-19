import matplotlib.pyplot as plt
from scripts.calc import r

plt.plot(r['dt'], r['U_Cu_Fe_mV'], label='Медь-железо', marker='o')
plt.xlabel(r'$\Delta t$, $^\circ$C')
plt.ylabel(r'$\Delta U$, мВ')
plt.legend(ncol=1)
plt.savefig('plot_eds_CuFe.pgf')
plt.close()

plt.plot(r['dt'], r['U_Cu_Const_mV'], label='Медь-константан', marker='s')
plt.xlabel(r'$\Delta t$, $^\circ$C')
plt.ylabel(r'$\Delta U$, мВ')
plt.legend(ncol=1)
plt.savefig('plot_eds_CuConst.pgf')
plt.close()

plt.plot(r['dt'], r['U_Cu_Mang_mV'], label='Медь-манганин', marker='^')
plt.xlabel(r'$\Delta t$, $^\circ$C')
plt.ylabel(r'$\Delta U$, мВ')
plt.legend(ncol=1)
plt.savefig('plot_eds_CuMang.pgf')
plt.close()