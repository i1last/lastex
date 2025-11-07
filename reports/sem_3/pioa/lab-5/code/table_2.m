file = fopen('./src/table_2.csv', 'r');
file_output = textscan(file, '%f;%f;%d;%s', 'HeaderLines', 1);
fclose(file);

range_start = file_output{1};
range_end = file_output{2};
count_of_dots = file_output{3};
figure_type = file_output{4}{1};

table_2_func(range_start, range_end, count_of_dots, figure_type);