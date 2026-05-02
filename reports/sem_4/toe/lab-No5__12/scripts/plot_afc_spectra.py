# scripts/plot_afc_spectra.py
import numpy as np
import matplotlib.pyplot as plt
from scripts.protocol import p
from scripts.calc import r

f_afc = np.array(p['bd']['f'])
H_afc = np.array(p['bd']['Hu'])

f_sp = np.linspace(0, 500e3, 1000)
w_sp = 2 * np.pi * f_sp
w_sp[0] = 1e-10  # Избегание деления на ноль

Uin_2 = 2 * np.abs(np.sin(0.5 * w_sp * r['part3']['t_u'][0])) / w_sp
Uin_10 = 2 * np.abs(np.sin(0.5 * w_sp * r['part3']['t_u'][1])) / w_sp

Uin_2[0] = r['part3']['t_u'][0]
Uin_10[0] = r['part3']['t_u'][1]

fig, ax1 = plt.subplots()

ax1.plot(f_afc / 1000, H_afc, label='$|H_U(f)|$')
ax1.axvline(r['part3']['f_cp'] / 1000, linestyle='--', label='$f_{\\text{ср}}$')
ax1.set_xlabel('$f$, кГц')
ax1.set_ylabel('$|H_U|$, отн. ед.')

ax2 = ax1.twinx()
ax2.plot(f_sp / 1000, Uin_2 * 1e6, marker='', label='$|U_{\\text{вх}}|$, $t_{\\text{и}} = 2$ мкс')
ax2.plot(f_sp / 1000, Uin_10 * 1e6,marker='', label='$|U_{\\text{вх}}|$, $t_{\\text{и}} = 10$ мкс')
ax2.set_ylabel('$|U_{\\text{вх}}|$, мкВ$\\cdot$с')

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, ncol=2)

plt.savefig('afc_spectra.pgf')