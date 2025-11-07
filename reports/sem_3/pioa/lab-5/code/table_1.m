clear, clc

filename = './src/table_1.csv'; 

M = readmatrix(filename, 'Delimiter', ';');

x_range_from = M(1, 1);
x_range_to   = M(1, 2);
x1_len       = M(2, 1);
x2_len       = M(2, 2);

result = table_1_func(x_range_from, x_range_to, x1_len, x2_len);