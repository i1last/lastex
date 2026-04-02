import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_2 import tf
from scripts.calc_3 import w, a_w, phi_w

# График АЧХ
plt.figure()
plt.plot(w, a_w, marker="")
plt.axhline(y=0.707*a_w[0], color='r', linestyle='--')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A(\omega)$')
plt.savefig('plot_afc.pgf')

# График ФЧХ
plt.figure()
plt.plot(w, np.degrees(phi_w), marker="")
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi(\omega), {}^{\circ}$')
plt.savefig('plot_pfc.pgf')

# Годограф (АФХ)
plt.figure()
plt.plot(a_w * np.cos(phi_w), a_w * np.sin(phi_w), marker="")
plt.xlabel('Re')
plt.ylabel('Im')
plt.savefig('plot_afh.pgf')