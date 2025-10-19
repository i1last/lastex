%% Кусочно-линейная нечетная функция
disp('--- Кусочно-линейная нечетная функция ---');
disp('Выберите параметры функции:');
a = input('Введите точку a (первый интервал)    : ');
b = input('Введите точку b (второй интервал)    : ');
k = input('Введите коэффициент наклона k        : ');
m = input('Введите значение m (первая константа): ');
n = input('Введите значение n (вторая константа): ');

[x, y] = ex2(a, b, k, m, n);
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

matrix = randi([min_matrix_val_input, max_matrix_val_input], rows_input, cols_input);

search_mode_input    = input('Введите режим поиска (min/max)           : ', 's');
operation_mode_input = input('Введите операцию над элементами (sum/mul): ', 's');

result = ex3(matrix, search_mode_input, operation_mode_input);

disp('Исходная матрица:');
disp(matrix);
fprintf('Результат поиска %s: %f\n', search_mode_input, result.value);
disp('Позиция найденного элемента (строка, столбец):');
disp(result.subindex);
disp('Результат вычисления операции над найденным элементом:');
disp(result.operation);