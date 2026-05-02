import numpy as np
import matplotlib.pyplot as plt
from scripts.calc import r
from scripts.protocol import p

t = np.linspace(0, 15e-6, 1000)
tau = r['part1']['tau']
U_in = 1.0

# Теоретический выходной сигнал
U_out_2 = np.where(t <= 2e-6, U_in * (1 - np.exp(-t/tau)),
                   U_in * (1 - np.exp(-2e-6/tau)) * np.exp(-(t-2e-6)/tau))

U_out_10 = np.where(t <= 10e-6, U_in * (1 - np.exp(-t/tau)),
                    U_in * (1 - np.exp(-10e-6/tau)) * np.exp(-(t-10e-6)/tau))

plt.plot(t * 1e6, U_out_2, marker='',label='$t_{\\text{и}} = 2$ мкс')
plt.plot(t * 1e6, U_out_10,marker='', label='$t_{\\text{и}} = 10$ мкс')

# Уровни экспериментальных максимумов
plt.axhline(p['fod']['Uoutmax'][0], color='C0', marker='', linestyle='--', label='Эксп. max (2 мкс)')
plt.axhline(p['fod']['Uoutmax'][1], color='C1', marker='', linestyle='--', label='Эксп. max (10 мкс)')

plt.xlabel('$t$, мкс')
plt.ylabel('$U_{\\text{вых}}$, В')
plt.legend(ncol=2)

plt.savefig('transient1.pgf')