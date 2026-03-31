dofile('code/1.lua')

mat = {
    A11 = 0,
    A12 = 1 / n.C1,
    A13 = 0,
    
    A21 = -1 / n.L1,
    A22 = -n.R1 / n.L1,
    A23 = -n.R1 / n.L1,
    
    A31 = 0,
    A32 = -n.R1 / n.L2,
    A33 = -(n.R1 + n.R2) / n.L2,
    
    B11 = 0,
    B21 = n.R1 / n.L1,
    B31 = n.R1 / n.L2,
}