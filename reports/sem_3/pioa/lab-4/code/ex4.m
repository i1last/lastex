%% Кусочно-линейная нечетная функция
disp('--- Кусочно-линейная нечетная функция ---');
disp('Выберите параметры функции:');
a = input('Введите точку a (первый интервал)    : ');
b = input('Введите точку b (второй интервал)    : ');
m = input('Введите значение m (первая константа): ');
n = input('Введите значение n (вторая константа): ');

x = -10 : 0.01 : 10;
f = ex2(a, b, m, n);
y = f(x);
plot(x, y);
grid on;
xlabel('x'); ylabel('f(x)');
title('Нечетная кусочно-линейная функция на [-10, 10]');

%% Работа с произвольной матрицей
disp('');
disp('--- Работа с произвольной матрицей ---');

disp('Матрица будет заполнена случайными целыми числами в указанном диапазоне...');
max_matrix_val_input = input('Введите максимальное значение элемента матрицы: ');
min_matrix_val_input = input('Введите минимальное значение элемента матрицы : ');
rows_input           = input('Введите количество строк матрицы              : ');
cols_input           = input('Введите количество столбцов матрицы           : ');
operation_mode_input = input('Введите операцию над элементами (sum/mul)     : ', 's');

matrix = randi([min_matrix_val_input, max_matrix_val_input], rows_input, cols_input);

search_results.struct = ex3_1(matrix);
[search_results.value, search_results.subindex] = ex3_1(matrix);

operation_result = ex3_2(matrix, operation_mode_input);

disp('Исходная матрица:');
disp(matrix);
disp('Результат поиска:');
disp(search_results);
disp(search_results.struct);
disp('Результат вычислений:');
disp(operation_result);