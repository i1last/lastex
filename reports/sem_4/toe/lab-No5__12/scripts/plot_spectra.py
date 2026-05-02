# scripts/plot_spectra.py
import numpy as np
import matplotlib.pyplot as plt
from scripts.calc import r

f_sp = np.linspace(0, 500e3, 1000)
w_sp = 2 * np.pi * f_sp
w_sp[0] = 1e-10  # Избегание деления на ноль

Uin_2 = 2 * np.abs(np.sin(0.5 * w_sp * r['part3']['t_u'][0])) / w_sp
Uin_10 = 2 * np.abs(np.sin(0.5 * w_sp * r['part3']['t_u'][1])) / w_sp

Uin_2[0] = r['part3']['t_u'][0]
Uin_10[0] = r['part3']['t_u'][1]

plt.plot(f_sp / 1000, Uin_2 * 1e6, marker='', label='$|U_{\\text{вх}}|$, $t_{\\text{и}} = 2$ мкс')
plt.plot(f_sp / 1000, Uin_10 * 1e6, marker='', label='$|U_{\\text{вх}}|$, $t_{\\text{и}} = 10$ мкс')

plt.xlabel('$f$, кГц')
plt.ylabel('$|U_{\\text{вх}}|$, мкВ$\\cdot$с')
plt.legend(ncol=2)

plt.savefig('spectra.pgf')