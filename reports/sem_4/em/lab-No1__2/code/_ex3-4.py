from math import exp
c  = [2.74, 1.02, 3.7 / 1000, 1.44]
nu = [1.05, 0.61, 0.63, 1.93]
de = [1.12, 0.66, 0.18, 2.90]

mun = [0.13, 0.39, 7.8, 0.04]
mup = [0.05, 0.19, 0.075, 0.006]

ni = []
for i in range(4):
    x = (c[i] * 1e25 * nu[i] * 1e25) ** 0.5 * exp(-de[i] / 0.0517)
    ni.append(x)
    print(f"{x:e}")

print()

for i in range(4):
    x = 1.602 * 1e-19 * ni[i] * (mun[i] + mup[i])
    print(f"{x:e}")