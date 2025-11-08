%% Задаем функции и параметры
a = -0.6;
b = 4.6;

g = @(x) a*x + b;
f = @(x) sin(x/2) - cos(3 * x) + 1;
r = @(x) g(x) - f(x);

x = 2 : 0.001 : 11; 

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

%% Приближенное решение

dx = 0.5;
approx_roots = inf(2, length(X_approx));  % 2 x N, где N - число корней. Первая строка для x, вторая для dy
min_dy = inf(length(X_approx));
for i = 1 : length(X_approx)
    for x_0 = X_approx(i) - dx : 0.05 : X_approx(i) + dx
        dy = abs(r(x_0));

        if dy < min_dy(i)
            approx_roots(:, i) = [x_0; f(x_0)];
            min_dy(i) = dy;
        end
    end
end

fprintf('\n\n');
disp('--- Вычисленные приближенные корни: ---');
fprintf('\n');
fprintf("x = %.3f, y = %.3f\n", approx_roots);

% Добавление найденных точек на график
h_points_approx = plot(h_axes, approx_roots(1, :), approx_roots(2, :), 'o');


%% Точное решение
% fzero пытается найти x, при котором r(x) = 0 на основе начального приближения
% arrayfun применяется для обработки всех приближений сразу
X_sol = arrayfun(@(x) fzero(r, x), X_approx);
Y_sol = g(X_sol);

fprintf('\n\n');
disp('--- Вычисленные точные корни: ---');
fprintf('\n');
fprintf("x = %.3f, y = %.3f\n", [X_sol'; Y_sol']);

% Добавление найденных точек на график
h_points_accurat = plot(h_axes, X_sol, Y_sol, 'o');
legend;

%% Управление свойствами объектов
set(h_points_approx, ...
    'Marker',           'o', ...
    'MarkerEdgeColor',  'magenta', ...
    'MarkerFaceColor',  'magenta', ...
    'MarkerSize',       4, ...
    'DisplayName',      'Найденные приближенные решения');
set(h_points_accurat, ...
    'Marker',           'o', ...
    'MarkerEdgeColor',  'black', ...
    'MarkerSize',       12, ...
    'DisplayName',      'Найденные точные решения');
set(h_line1, ...
    'Color',       'blue', ...
    'LineStyle',   '-', ...
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
for i = 1 : length(approx_roots)
    x_sol_i = approx_roots(1, i);
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