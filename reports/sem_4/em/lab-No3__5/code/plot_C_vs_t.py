from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua и выполнение скрипта обработки
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")

# Получение доступа к глобальным таблицам
p = lua.globals().p
r = lua.globals().r

# Извлечение данных
t = np.array(list(p.t.values()))

C1_net_pF = np.array(list(r.C1_net.values())) * 1e12
C2_net_pF = np.array(list(r.C2_net.values())) * 1e12
C3_net_pF = np.array(list(r.C3_net.values())) * 1e12
C4_net_pF = np.array(list(r.C4_net.values())) * 1e12
C5_net_pF = np.array(list(r.C5_net.values())) * 1e12

# Построение графика
plt.figure()
plt.plot(t, C1_net_pF, label='1. Неорг. стекло')
plt.plot(t, C2_net_pF, label='2. Слюда')
plt.plot(t, C3_net_pF, label='3. Тиконд')
plt.plot(t, C4_net_pF, label='4. Полипропилен')
plt.plot(t, C5_net_pF, label='5. Сегнетокерамика')

# Настройка осей и легенды
plt.xlabel('Температура, $^\circ$C')
plt.ylabel('Емкость, пФ')
plt.legend(ncol=3, borderaxespad=-4)
plt.grid()

# Сохранение в PGF
plt.savefig('plot_C_vs_t.pgf')
plt.close()



# Построение графика
plt.figure()
plt.plot(t, C1_net_pF, label='1. Неорг. стекло')
plt.plot(t, C2_net_pF, label='2. Слюда')
plt.plot(t, C3_net_pF, label='3. Тиконд')
plt.plot(t, C4_net_pF, label='4. Полипропилен')

# Настройка осей и легенды
plt.xlabel('Температура, $^\circ$C')
plt.ylabel('Емкость, пФ')
plt.legend(ncol=3, borderaxespad=-4)
plt.grid()

plt.savefig('plot_C_vs_t_withoutSegnetoKeram.pgf')
