import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from scripts.protocol import p

plt.plot(p['tc']['Uin'], p['tc']['UforR14'], marker='o', label='$R_H = R_{14}$')
plt.plot(p['tc']['Uin'], p['tc']['UforR15'], marker='s', label='$R_H = R_{15}$')

ax = plt.gca()
ax.yaxis.set_major_locator(MultipleLocator(2))

plt.xlabel('$U_{\\text{вх}}$, В')
plt.ylabel('$U_{\\text{вых}}$, В')
plt.legend(ncol=2)

plt.savefig('plot_tc.pgf')