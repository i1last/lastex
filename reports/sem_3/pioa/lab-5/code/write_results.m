clear, clc

[x, y, z] = table_1_func();

output_file = fopen('./results.txt','w');
data = [x(:)'; y(:)'; z(:)'];

fprintf(output_file, '#array#:MySurf:\n');
fprintf(output_file, '%f %f %f\n', data);
fprintf(output_file, '#endarray#');

fclose(output_file);