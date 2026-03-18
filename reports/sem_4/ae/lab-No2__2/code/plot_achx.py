from lupa import LuaRuntime
import matplotlib.pyplot as plt

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

# Извлечение данных из Lua-таблиц
f = [p.achx.f[i] for i in range(1, len(p.achx.f) + 1)]
K_oe = [r.K.oe[i] for i in range(1, len(r.K.oe) + 1)]
K_ob =[r.K.ob[i] for i in range(1, len(r.K.ob) + 1)]
K_ok = [r.K.ok[i] for i in range(1, len(r.K.ok) + 1)]

plt.plot(f, K_oe, label='ОЭ')
plt.plot(f, K_ob, label='ОБ')
plt.plot(f, K_ok, label='ОК')

plt.xscale('log')
plt.xlabel('$f$, Гц')
plt.ylabel('$K$')
plt.legend(ncol=3)

plt.savefig('plot_achx.pgf')