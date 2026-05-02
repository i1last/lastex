# scripts/plot_afc.py
import numpy as np
import matplotlib.pyplot as plt
from scripts.protocol import p
from scripts.calc import r

f_afc = np.array(p['bd']['f'])
H_afc = np.array(p['bd']['Hu'])

plt.plot(f_afc / 1000, H_afc, marker='o', label='$|H_U(f)|$')
plt.axvline(r['part3']['f_cp'] / 1000, linestyle='--', color='black', label='$f_{\\text{ср}}$')

plt.xlabel('$f$, кГц')
plt.ylabel('$|H_U|$, отн. ед.')
plt.legend(ncol=2)

plt.savefig('afc.pgf')