from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua и выполнение скрипта обработки
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")

# Получение доступа к глобальной таблице протокола
p = lua.globals().p

# Извлечение данных
t = np.array(list(p.t.values()))
tan1 = p.tan1
tan2 = p.tan2
tan3 = p.tan3
tan4 = p.tan4
tan5 = p.tan5

# Построение графика
plt.figure()
plt.plot(t, np.full_like(t, tan1), label='1. Неорг. стекло')
plt.plot(t, np.full_like(t, tan2), label='2. Слюда')
plt.plot(t, np.full_like(t, tan3), label='3. Тиконд')
plt.plot(t, np.full_like(t, tan4), label='4. Полипропилен')
plt.plot(t, np.full_like(t, tan5), label='5. Сегнетокерамика')

# Настройка осей и легенды
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'Тангенс угла потерь, $\tan \delta$')
plt.legend(ncol=3)
plt.grid()

# Сохранение в PGF
plt.savefig('plot_tan_vs_t.pgf')