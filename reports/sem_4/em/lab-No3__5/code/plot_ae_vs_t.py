from lupa import LuaRuntime
import matplotlib.pyplot as plt
import numpy as np

# Инициализация Lua и выполнение скрипта обработки
lua = LuaRuntime(unpack_returned_tuples=True)
lua.execute("dofile('code/processing.lua')")

# Получение доступа к глобальной таблице результатов
r = lua.globals().r

# Извлечение данных
t_calc = np.array(list(r.t_calc.values()))
ae1 = np.array(list(r.ae1.values()))
ae2 = np.array(list(r.ae2.values()))
ae3 = np.array(list(r.ae3.values()))
ae4 = np.array(list(r.ae4.values()))
ae5 = np.array(list(r.ae5.values()))
print(ae1)
print(ae2)
print(ae3)
print(ae4)
print(ae5)

# Построение графика
plt.figure()
plt.plot(t_calc, ae1, label='1. Неорг. стекло')
plt.plot(t_calc, ae2, label='2. Слюда')
plt.plot(t_calc, ae3, label='3. Тиконд')
plt.plot(t_calc, ae4, label='4. Полипропилен')
plt.plot(t_calc, ae5, label='5. Сегнетокерамика')

# Настройка осей и легенды
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'ТКДП $\alpha_\epsilon$, К$^{-1}$')
plt.legend(ncol=3)
plt.grid()

# Сохранение в PGF
plt.savefig('plot_ae_vs_t.pgf')
# plt.close()





plt.figure()
plt.plot(t_calc, ae1, label='1. Неорг. стекло')
plt.plot(t_calc, ae2, label='2. Слюда')
plt.plot(t_calc, ae3, label='3. Тиконд')
plt.plot(t_calc, ae4, label='4. Полипропилен')
# plt.plot(t_calc, ae5, label='5. Сегнетокерамика')

# Настройка осей и легенды
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'ТКДП $\alpha_\epsilon$, К$^{-1}$')
plt.legend(ncol=3)
plt.grid()

# Сохранение в PGF
plt.savefig('plot_ae_vs_t_withoutSK.pgf')
# plt.show()