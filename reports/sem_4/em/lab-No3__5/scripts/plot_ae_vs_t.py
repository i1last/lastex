import matplotlib.pyplot as plt
from scripts.calc import r

t_calc = r['t_calc']
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
    plt.plot(t_calc, r[f'ae{i}'], label=labels[i-1])
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'ТКДП $\alpha_\varepsilon$, К$^{-1}$')
plt.legend(ncol=2)
plt.savefig('plot_ae_vs_t.pgf')

# График без сегнетокерамики
plt.figure()
for i in range(1, 5):
    plt.plot(t_calc, r[f'ae{i}'], label=labels[i-1])
plt.xlabel('Температура, $^\circ$C')
plt.ylabel(r'ТКДП $\alpha_\varepsilon$, К$^{-1}$')
plt.legend(ncol=2)
plt.savefig('plot_ae_vs_t_withoutSK.pgf')