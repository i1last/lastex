import matplotlib.pyplot as plt
from scripts.calc import p

t = p['t']
labels = [
    '1. Неорг. стекло', 
    '2. Слюда', 
    '3. Тиконд', 
    '4. Полипропилен', 
    '5. Сегнетокерамика'
]

plt.figure()
for i in range(1, 6):
    plt.plot(t, [p[f'tan{i}']] * len(t), label=labels[i-1])
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'Тангенс угла потерь, $\tan \delta$')
plt.legend(ncol=2)
plt.savefig('plot_tan_vs_t.pgf')