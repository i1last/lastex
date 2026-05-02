# scripts/plot_afc_rh1.py
import matplotlib.pyplot as plt
from scripts.calc import r

plt.figure()
plt.plot(r['afc']['f'] / 1e3, r['afc']['H_exp_R1'], marker='o', label=r'Эксперимент')
plt.plot(r['afc']['f_plot'] / 1e3, r['afc']['H_th_R1_plot'], marker='', linestyle='--', label=r'Теория')
plt.xlabel(r'$f$, кГц')
plt.ylabel(r'$|H_U(j\omega)|$')
plt.legend(ncol=2)
plt.savefig('afc_rh1.pgf')