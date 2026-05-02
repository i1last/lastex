import matplotlib.pyplot as plt
from scripts.protocol import p
from scripts.calc import r

plt.semilogx(p['afcd']['f'], r['K_afc'], marker='o', label='АЧХ')

plt.axvline(x=p['cf']['feu'], color='k', linestyle='--', label='$f_{\\text{ЕУ}}$')
plt.axvline(x=p['cf']['fumm'], color='gray', linestyle='-.', label='$f_{\\text{УММ}}$')

plt.xlabel('$f$, Гц')
plt.ylabel('$K$')
plt.legend(ncol=3)

plt.savefig('plot_afc.pgf')