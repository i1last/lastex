import matplotlib.pyplot as plt
from scripts.calc import r

plt.plot(r['f_loss'], r['E'], marker='o', linestyle='', label='$Э$ (эксперимент)')

f_line =[0, max(r['f_loss'])]
E_line = [r['E_G'] + r['k_loss'] * f for f in f_line]
plt.plot(f_line, E_line, linestyle='-', label='Линейная аппроксимация')

plt.plot(0, r['E_G'], marker='s', linestyle='', color='C3', label='$Э_Г$ ($f=0$)')

plt.xlabel('$f$, Гц')
plt.ylabel('$Э$, Дж/кг')
plt.legend(ncol=2)

plt.savefig('plot_losses.pgf')