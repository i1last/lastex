import matplotlib.pyplot as plt
from scripts.calc import r
from scripts.protocol import p

f = p['alf']['f'] + p['ahf']['f']
K = r['afc']['Klf'] + r['afc']['Khf']

# Сортировка по частоте для корректного отображения линии
f, K = zip(*sorted(zip(f, K)))

plt.figure()
plt.semilogx(f, K, label=r'$K(f)$')
plt.axhline(0.9, linestyle='--', color='gray', label='Уровень 0.9')
plt.axvline(r['afc']['fb'], linestyle=':', color='red', label=r'$f_{\text{в}}$')
plt.xlabel(r'$f$, Гц')
plt.ylabel(r'$K(f)$')
plt.legend(ncol=3)
plt.savefig('plot_afc.pgf')