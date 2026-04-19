import matplotlib.pyplot as plt
from scripts.protocol import p
from scripts.calc import r

def plot_bode(f, K, Kmax, fgr, feu, label, filename):
    plt.figure()
    plt.semilogx(f, K, marker='o', label=label)
    
    # Уровень 0.707 и перпендикуляр f_gr
    k_gr = 0.707 * Kmax
    plt.axhline(k_gr, color='C1', linestyle='--', label=r'$0.707 K_{max}$')
    if fgr is not None:
        plt.vlines(fgr, 0, k_gr, color='C1', linestyle='--')
    
    # Уровень K=1 и перпендикуляр f_eu
    plt.axhline(1.0, color='C2', linestyle=':', label=r'$K=1$')
    if feu is not None:
        plt.vlines(feu, 0, 1.0, color='C2', linestyle=':')
        
    plt.xlabel('Частота $f$, Гц')
    plt.ylabel('Коэффициент усиления $K$')
    plt.ylim(bottom=0)
    plt.legend(ncol=3)
    plt.savefig(filename)

plot_bode(p['fPoU'], r['K_parPoU'], r['Kmax_parPoU'], r['fgr_parPoU'], r['feu_parPoU'], 
          'Парал. по напряжению', 'afc_par_u.pgf')

plot_bode(p['fPoU'], r['K_serPoU'], r['Kmax_serPoU'], r['fgr_serPoU'], r['feu_serPoU'], 
          'Посл. по напряжению', 'afc_ser_u.pgf')

plot_bode(p['fPoI'], r['K_parPoI'], r['Kmax_parPoI'], r['fgr_parPoI'], r['feu_parPoI'], 
          'Парал. по току', 'afc_par_i.pgf')