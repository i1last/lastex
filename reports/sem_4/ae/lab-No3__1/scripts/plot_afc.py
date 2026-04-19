import matplotlib.pyplot as plt
import numpy as np
from scripts.calc import p, r

# --- График для пассивных цепей ---
plt.figure()
plt.plot(p['ad']['f'], r['K_dc'], label='Пассивная ДЦ')
plt.plot(p['ad']['f'], r['K_ic'], label='Пассивная ИЦ')

# Уровень -3 дБ
level = 1 / np.sqrt(2)
plt.axhline(y=level, color='gray', linestyle='--')
plt.text(1e5, level * 1.05, r'$K_{max}/\sqrt{2}$')
f_dc = r['f_n_gr_graph_dc']
f_ic = r['f_v_gr_graph_ic']
plt.plot([f_dc, f_dc], [0, level], color='C0', linestyle='--')
plt.plot([f_ic, f_ic], [0, level], color='C1', linestyle='--')
plt.ylim(bottom=0)
plt.xlim(left=10, right=1e6)

# Настройка осей и легенды
plt.xscale('log')
plt.xlabel(r'$f$, Гц')
plt.ylabel(r'$K$')
plt.legend(ncol=2)
plt.savefig('afc_passive.pgf')


# --- График для активных цепей ---
plt.figure()
plt.plot(p['ad']['f'], r['K_actdc'], label='Активная ДЦ')
plt.plot(p['ad']['f'], r['K_actic'], label='Активная ИЦ')

# Уровни -3 дБ
level_actdc = np.max(r['K_actdc']) / np.sqrt(2)
level_actic = np.max(r['K_actic']) / np.sqrt(2)
plt.axhline(y=level_actdc, color='gray', linestyle='--')
plt.axhline(y=level_actic, color='gray', linestyle='--')
plt.text(1e5, level_actdc * 1.05, r'$K_{max}^{АДЦ}/\sqrt{2}$')
plt.text(500, level_actic * 1.05, r'$K_{max}^{АИЦ}/\sqrt{2}$')
f_n_actdc = r['f_n_gr_graph_actdc']
f_v_actdc = r['f_v_gr_graph_actdc']
f_v_actic = r['f_v_gr_graph_actic']
plt.plot([f_n_actdc, f_n_actdc], [0, level_actdc], color='C0', linestyle='--')
plt.plot([f_v_actdc, f_v_actdc], [0, level_actdc], color='C0', linestyle='--')
plt.plot([f_v_actic, f_v_actic], [0, level_actic], color='C1', linestyle='--')
plt.xscale('log')
plt.xlabel(r'$f$, Гц')
plt.ylabel(r'$K$')
plt.legend(ncol=2)
plt.ylim(bottom=0)
plt.xlim(left=10, right=1e6)
plt.savefig('afc_active.pgf')