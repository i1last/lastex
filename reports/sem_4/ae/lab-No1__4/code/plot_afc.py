from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua и загрузка данных
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
r = lua.globals().r

# Извлечение данных для построения
woc_f = np.array(list(r.afc.woc.f.values()))
woc_K = np.array(list(r.afc.woc.K.values()))

r3_f = np.array(list(r.afc.R3.f.values()))
r3_K = np.array(list(r.afc.R3.K.values()))

evck_f = np.array(list(r.afc.evck.f.values()))
evck_K = np.array(list(r.afc.evck.K.values()))

ivck_f = np.array(list(r.afc.ivck.f.values()))
ivck_K = np.array(list(r.afc.ivck.K.values()))

nck_f = np.array(list(r.afc.nck.f.values()))
nck_K = np.array(list(r.afc.nck.K.values()))

# Построение графика
fig, ax = plt.subplots()

ax.semilogx(woc_f, woc_K,  label='Без коррекции')
ax.semilogx(r3_f, r3_K,     label='С $R_3$')
ax.semilogx(evck_f, evck_K, label='ЭВЧК')
ax.semilogx(ivck_f, ivck_K,label='ИВЧК')
ax.semilogx(nck_f, nck_K,  label='НЧК')

# Настройка осей и легенды
ax.set_xlabel('Частота $f$, Гц')
ax.set_ylabel('Коэффициент усиления $K$')
ax.grid()
ax.legend(ncol=3)

# Сохранение в файл
plt.savefig('afc.pgf')