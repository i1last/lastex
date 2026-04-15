import matplotlib.pyplot as plt
from scripts.calc import r

plt.figure()
# Идеальная характеристика
plt.plot([0, 10], [0, 10], linestyle='-', color='red', label='Идеальная ХП')
# Реальная характеристика (ступенчатая)
plt.step(r['sc_R'], r['sc_Rp'], where='post', color='black', label='Реальная ХП')

plt.xlabel('$R$, Ом')
plt.ylabel('$R_\\text{п}$, Ом')
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig('plot_sc.pgf')