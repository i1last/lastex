from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua и загрузка данных
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")
r = lua.globals().r

# Построение графика
fig, ax = plt.subplots()

# Список режимов для итерации
modes = [
    ('woc', 'Без коррекции'),
    ('R3', 'С $R_3$'),
    ('evck', 'ЭВЧК'),
    ('ivck', 'ИВЧК'),
    ('nck', 'НЧК')
]

for key, label in modes:
    mode_data = r.afc[key]
    if mode_data is None:
        continue
        
    # Преобразование Lua-таблиц в numpy массивы
    f = np.array(list(mode_data.f.values()))
    k = np.array(list(mode_data.K.values()))
    
    # Построение основного графика
    line, = ax.semilogx(f, k, marker='', label=label)
    
    # Добавление линии уровня среза K_гр
    if mode_data.K_cutoff:
        ax.axhline(y=mode_data.K_cutoff, 
                   linestyle='-', 
                   color=line.get_color(), 
                   alpha=0.5, 
                   linewidth=1)

# Настройка осей и легенды
ax.set_xlabel('Частота $f$, Гц')
ax.set_ylabel('Коэффициент усиления $K$')
ax.grid()
ax.legend(ncol=3)

# Сохранение в файл
plt.savefig('afc_cutoff.pgf')