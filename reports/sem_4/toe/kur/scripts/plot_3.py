import numpy as np
import matplotlib.pyplot as plt
from scripts.calc_2 import tf
from scripts.calc_3 import w, a_w, phi_w

# График АЧХ
plt.figure()
plt.plot(w, a_w, marker="")
plt.xlim(left=min(w))
plt.ylim(bottom=min(a_w))
level = 0.707 * a_w[0]
plt.axhline(y=level, color='r', linestyle='--')
w_cut = np.interp(level, a_w[::-1], w[::-1])
plt.vlines(x=w_cut, ymin=0, ymax=level, color='r', linestyle='--')
plt.xlabel(r'$\omega$')
plt.ylabel(r'$A(\omega)$')
plt.savefig('plot_afc.pgf')

# График ФЧХ
plt.figure()
degphiw = np.degrees(phi_w)
plt.plot(w, degphiw, marker="")
plt.xlim(left=min(w))
plt.ylim(bottom=min(degphiw))
current_yticks = list(plt.yticks()[0])
plt.yticks(current_yticks + [round(min(degphiw), 1)])
plt.xlabel(r'$\omega$')
plt.ylabel(r'$\Phi(\omega), {}^{\circ}$')
plt.savefig('plot_pfc.pgf')

# Годограф (АФХ)
plt.figure()
awcos = a_w * np.cos(phi_w)
awsin = a_w * np.sin(phi_w)
plt.plot(awcos, awsin, marker="")
plt.xlabel('Re')
plt.ylabel('Im')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.grid(True, linestyle='--', alpha=0.6)
plt.gca().set_aspect('equal', adjustable='box')
plt.savefig('plot_afh.pgf')