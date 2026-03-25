from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

def get_data(dataset_name):
    data = p[dataset_name]
    # Преобразование Lua-таблиц в списки Python
    f = [data.f[i] for i in range(1, len(data.f) + 1)]
    i_vals = [data.I[i] * 1000 for i in range(1, len(data.I) + 1)] # в мА
    return f, i_vals

# Подготовка данных для графиков
f_mp, i_mp = get_data('mp')
f_r1, i_r1 = get_data('R1')
f_c3, i_c3 = get_data('C3')

# Построение
plt.plot(f_mp, i_mp, label='Малые потери')
plt.plot(f_r1, i_r1, label='С резистором $R_1$')
plt.plot(f_c3, i_c3, label='С емкостью $3C$')

plt.xlabel('$f$, Гц')
plt.ylabel('$I$, мА')
plt.legend(ncol=3)

# Сохранение в формате PGF для LaTeX
plt.savefig('ach_plot.pgf')