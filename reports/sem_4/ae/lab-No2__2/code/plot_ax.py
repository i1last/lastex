from lupa import LuaRuntime
import matplotlib.pyplot as plt

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
p = lua.globals().p

# Извлечение данных из Lua-таблиц
Uin = [p.ax.Uin[i] for i in range(1, len(p.ax.Uin) + 1)]
Uoe = [p.ax.Uoe[i] for i in range(1, len(p.ax.Uoe) + 1)]
Uob =[p.ax.Uob[i] for i in range(1, len(p.ax.Uob) + 1)]
Uok = [p.ax.Uok[i] for i in range(1, len(p.ax.Uok) + 1)]

plt.plot(Uin, Uoe, label='ОЭ')
plt.plot(Uin, Uob, label='ОБ')
plt.plot(Uin, Uok, label='ОК')

plt.xlabel('$U_{вх}$, В')
plt.ylabel('$U_{вых}$, В')
plt.legend(ncol=3)

plt.savefig('plot_ax.pgf')