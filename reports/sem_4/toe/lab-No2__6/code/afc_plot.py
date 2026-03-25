from lupa import LuaRuntime
import matplotlib.pyplot as plt

# --- Инициализация Lua ---
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute(f"dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

# --- Построение АЧХ для RLC-цепи ---
plt.figure(figsize=(8, 5))

# Извлечение данных из Lua-таблиц по индексам (1-based)
n_plot = len(r.RLC.plot.f)
f_plot_kHz = [r.RLC.plot.f[i] / 1000 for i in range(1, n_plot + 1)]
I_plot_mA = [r.RLC.plot.I[i] * 1000 for i in range(1, n_plot + 1)]

n_exp = len(p.RLC.f)
f_exp_kHz = [p.RLC.f[i] / 1000 for i in range(1, n_exp + 1)]
I_exp_mA = [p.RLC.I[i] * 1000 for i in range(1, n_exp + 1)]

# Теоретическая кривая
plt.plot(f_plot_kHz, I_plot_mA, label='Теоретическая АЧХ', color='black')

# Экспериментальные точки
plt.plot(f_exp_kHz, I_exp_mA, 's', label='Экспериментальные точки', markersize=6, color='black', markerfacecolor='white')

# Оформление
plt.xlabel(r'$f$, кГц')
plt.ylabel(r'$I$, мА')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig('afc_rlc.pgf')
plt.close()