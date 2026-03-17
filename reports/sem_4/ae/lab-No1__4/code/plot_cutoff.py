from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
r = lua.globals().r

fig, ax = plt.subplots()

# Для примера строим только "Без коррекции" для ясности среза
f = np.array(list(r.afc.woc.f.values()))
k = np.array(list(r.afc.woc.K.values()))
k_max = r.afc.woc.K_max
k_gr = r.afc.woc.K_cutoff

ax.semilogx(f, k, 'k-', label='Без коррекции')
ax.axhline(y=k_max, color='r', linestyle='--', alpha=0.5, label='$K_{max}$')
ax.axhline(y=k_gr, color='b', linestyle='--', alpha=0.5, label='$K_{гр} = 0.707 K_{max}$')

# Отметки частот
if r.afc.woc.f_low:
    ax.axvline(x=r.afc.woc.f_low,)
if r.afc.woc.f_high:
    ax.axvline(x=r.afc.woc.f_high,)

ax.set_xlabel('Частота $f$, Гц')
ax.set_ylabel('Усиление $K$')
ax.legend()
ax.grid()

plt.savefig('afc_cutoff.pgf')