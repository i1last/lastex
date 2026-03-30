from lupa import LuaRuntime
import matplotlib.pyplot as plt

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
p = lua.globals().p
r = lua.globals().r

# Извлечение данных для варианта 1
t_vals = list(p.fc.o1.t.values())
err_vals = list(r.fc.o1.relF.values())

plt.figure()
plt.plot(t_vals, err_vals, marker='o', linestyle='-')
plt.xscale('log')
plt.xlabel('Время счета $t_{\\text{сч}}$, с')
plt.ylabel('Относительная погрешность $\\delta_f$, \\%')
plt.tight_layout()
plt.savefig('error_vs_time.pgf')