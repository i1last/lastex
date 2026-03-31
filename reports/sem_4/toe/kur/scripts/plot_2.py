import matplotlib.pyplot as plt
from scripts.calc_2 import tf

poles_re = [tf['p1_re'], tf['p2_re'], tf['p3_re']]
poles_im =[tf['p1_im'], tf['p2_im'], tf['p3_im']]

zeros_re = [0.0, 0.0]
zeros_im = [tf['z1_im'], tf['z2_im']]

fig, ax = plt.subplots()

ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

ax.plot(poles_re, poles_im, 'rx', ms=10, label='Полюсы')
ax.plot(zeros_re, zeros_im, 'bo', ms=10, label='Нули')

ax.set_xlabel('Re')
ax.set_ylabel('Im')
ax.legend(ncol=2, numpoints=1)

plt.savefig('pz_map.pgf')