# plot_step_response.py
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
lua.execute("dofile('processing.lua')")
os.chdir(script_dir)

p_data = lua.globals().protocol.step_response
r_data = lua.globals().results.step_response

# Корректное извлечение данных из Lua таблиц (1-based indexing)
t = [p_data.t_i[i] for i in range(1, len(p_data.t_i) + 1)]
u_in = [p_data.u_in_i[i] for i in range(1, len(p_data.u_in_i) + 1)]
u_out = [p_data.u_out_i[i] for i in range(1, len(p_data.u_out_i) + 1)]
delta_y = [r_data.delta_y_i[i] for i in range(1, len(r_data.delta_y_i) + 1)]

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6))

# График сигналов
ax1.plot(t, u_in, 'o--', label=r'$u_{\text{вх}}(t)$', alpha=0.7)
ax1.plot(t, u_out, 's-', label=r'$u_{\text{вых}}(t)$')
ax1.set_ylabel('Напряжение, В')
ax1.legend()
ax1.grid(True, linestyle=':')

# График погрешности
ax2.plot(t, delta_y, 'd-', color='red', label=r'$\Delta u(t)$')
ax2.set_xlabel('Время $t$, с')
ax2.set_ylabel('Погрешность, В')
ax2.legend()
ax2.grid(True, linestyle=':')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('step_response.pgf')