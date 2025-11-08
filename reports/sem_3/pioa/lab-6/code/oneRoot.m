%% Определение исходной функции
f = @(x) sin(x/2) - cos(3 * x) + 1;
x_range = 0 : 0.001 : 12; 
y2_values = f(x_range);

%% Выбор новых коэффициентов
a_new = -8;
b_new = 32;

fprintf('--- Выбранные коэффициенты для единственного решения ---\n');
fprintf('Новый коэффициент a = %.1f\n', a_new);
fprintf('Новый коэффициент b = %.1f\n', b_new);

%% Построение графика
% Новая прямая с выбранными коэффициентами
y1_new = a_new * x_range + b_new;

% Создание и настройка графика
figure('Name', 'Единственное решение с крутым наклоном');
hold on;
grid on;

ylim([-3, 5])
plot(x_range, y1_new, 'b--', 'DisplayName', sprintf('y_1(x) = %.1fx + %.1f', a_new, b_new));
plot(x_range, y2_values, 'r', 'DisplayName', 'f(x) = sin(x/2) - cos(x) + 1;');

title('Подбор коэффициентов для единственного решения');
xlabel('x');
ylabel('y');
legend;