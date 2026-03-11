# plot_settling_plots.py
import matplotlib
matplotlib.use('pgf')
import matplotlib.pyplot as plt
from lupa import LuaRuntime
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
os.chdir(project_root)
lua = LuaRuntime()
lua.execute("dofile('protocol.lua')")
os.chdir(script_dir)

# Зависимость от f_0
d_f = lua.globals().protocol.settling_freq
f_0 = [d_f.f_0_i[i] for i in range(1, len(d_f.f_0_i) + 1)]
t_y_f = [d_f.t_y[i] for i in range(1, len(d_f.t_y) + 1)]

fig1, ax1 = plt.subplots(figsize=(5, 4))
ax1.plot(f_0, t_y_f, 'o-')
ax1.set_xlabel(r'Частота $f_0$, Гц')
ax1.set_ylabel(r'Время установления $t_y$, с')
ax1.set_title(r'$t_y = F(f_0)$')
ax1.grid(True, linestyle=':')
plt.tight_layout()
plt.savefig('settling_freq.pgf')

# Зависимость от beta
d_b = lua.globals().protocol.settling_beta
beta = [d_b.betta_i[i] for i in range(1, len(d_b.betta_i) + 1)]
t_y_b = [d_b.t_y[i] for i in range(1, len(d_b.t_y) + 1)]

fig2, ax2 = plt.subplots(figsize=(5, 4))
ax2.plot(beta, t_y_b, 's-', color='orange')
ax2.set_xlabel(r'Коэффициент демпфирования $\beta$')
ax2.set_ylabel(r'Время установления $t_y$, с')
ax2.set_title(r'$t_y = F(\beta)$')
ax2.grid(True, linestyle=':')
plt.tight_layout()
plt.savefig('settling_beta.pgf')