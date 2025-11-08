%% Задаем функции и параметры
a = -0.6;
b = 4.6;

g = @(x) a*x + b;
f = @(x) sin(x/2) - cos(3 * x) + 1;
r = @(x) g(x) - f(x);

x = 0 : 0.001 : 12; 

y_1 = g(x);
y_2 = f(x);

%% Графическое представление с использованием указателей (handles)
h_fig = figure("Name", "Графическое решение уравнения g(x) = f(x)");
h_axes = axes('Parent', h_fig);
hold on;
grid on;

h_line1 = plot(h_axes, x, y_1);
h_line2 = plot(h_axes, x, y_2);

xlabel('x');
ylabel('y');
title('Графическое решение уравнения g(x) = f(x)');


%% Численное решение уравнения
disp('Сколько корней наблюдается на графике? Введите число:');
number_of_roots = input('>>> ');

disp('Пожалуйста, кликните на графике на все точки корней...');
[X_approx, ~] = ginput(number_of_roots);  % Пользователь находит корни на графике

% fzero пытается найти x, при котором r(x) = 0 на основе начального приближения
% arrayfun применяется для обработки всех приближений сразу
X_sol = arrayfun(@(x) fzero(r, x), X_approx);
Y_sol = g(X_sol);

fprintf('\n\n');
disp('--- Вычисленные корни: ---');
fprintf('\n');
fprintf("x = %.3f, y = %.3f\n", [X_sol'; Y_sol']);

% Добавление найденных точек на график
h_points = plot(h_axes, X_sol, Y_sol);
legend;

%% Управление свойствами объектов
set(h_points, ...
    'Marker',           'o', ...
    'MarkerEdgeColor',  'k', ...  % black
    'MarkerSize',       8, ...
    'DisplayName',      'Найденные решения');
set(h_line1, ...
    'Color',       'blue', ...
    'LineStyle',   '--', ...
    'LineWidth',   1, ...
    'DisplayName', 'g(x) = -0.6x + 4.6');

set(h_line2, ...
    'Color',       'red', ...
    'LineWidth',   1.5, ...
    'DisplayName', 'f(x) = sin(x/2) - cos(x) + 1');


set(h_axes, 'GridLineStyle', ':');


%% Проверка точности решений
fprintf('\n\n');
disp('--- Проверка точности найденных решений: ---');
fprintf('\n');
for i = 1:length(X_sol)
    x_sol_i = X_sol(i);
    g_sol_i = g(x_sol_i);
    f_sol_i = f(x_sol_i);
    
    error = abs(g_sol_i - f_sol_i);
    
    fprintf('Корень %d: x = %.4f\n', i, x_sol_i);
    fprintf('    g(x) = %.4f, f(x) = %.4f\n', g_sol_i, f_sol_i);
    fprintf('    Абсолютная ошибка |g-f| = %.4f\n', error);
    
    if error < 0.01
        fprintf('    OK: Точность удовлетворяет требованию (< 0.01).\n\n');
    else
        fprintf('    WARNING: Точность НЕ удовлетворяет требованию (>= 0.01).\n\n');
    end
end