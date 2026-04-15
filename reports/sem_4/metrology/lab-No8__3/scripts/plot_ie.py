import matplotlib.pyplot as plt
import numpy as np
from scripts.calc import r

plt.figure()
plt.scatter(r['ie_R'], r['ie_dR'], color='black', marker='o', label='Эксперимент')

# Линия аппроксимации
R_line = np.linspace(min(r['ie_R']), max(r['ie_R']), 100)
dR_line = r['a'] + r['b'] * R_line
plt.plot(R_line, dR_line, marker='', color='black', label='Аппроксимация')

plt.xlabel('$R$, Ом')
plt.ylabel('$\\Delta R_\\text{и}$, Ом')
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig('plot_ie.pgf')