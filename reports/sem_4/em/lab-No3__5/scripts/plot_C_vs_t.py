import matplotlib.pyplot as plt
from scripts.calc import p, r

t = p['t']
labels = [
    '1. Неорг. стекло', 
    '2. Слюда', 
    '3. Тиконд', 
    '4. Полипропилен', 
    '5. Сегнетокерамика'
]

# График для всех 5 образцов
plt.figure()
for i in range(5, 6):
    plt.plot(t, [c * 1e12 for c in r[f'C{i}_net']], label=labels[i-1])
plt.xlabel('Температура, $^\circ$C')
plt.ylabel('Емкость, пФ')
plt.legend(ncol=2)
plt.savefig('plot_C_vs_t.pgf')

# График без сегнетокерамики
plt.figure()
for i in range(1, 5):
    plt.plot(t, [c * 1e12 for c in r[f'C{i}_net']], label=labels[i-1])
plt.xlabel('Температура, $^\circ$C')
plt.ylabel('Емкость, пФ')
plt.legend(ncol=2)
plt.savefig('plot_C_vs_t_withoutSegnetoKeram.pgf')