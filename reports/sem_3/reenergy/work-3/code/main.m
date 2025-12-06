% Настройка окружения
if ~exist('./results', 'dir')
    mkdir('./results');
end
set(0, 'DefaultFigureVisible', 'off');

% === ИСХОДНЫЕ ДАННЫЕ (из протокола) ===
% N - количество закрытых элементов
N = 0:9;

% --- МОНО панель (20 Вт, Pmax) ---
mono_I = [13.2, 6.87, 1.65, 0.81, 0.66, 0.58, 0.42, 0.35, 0.33, 0.25]; % мА
mono_U = [10.5, 4.58, 1.36, 0.72, 0.46, 0.51, 0.33, 0.28, 0.24, 0.21]; % В

% --- ПОЛИ панель (20 Вт, Pmax) ---
poly_I = [14.8, 7.12, 4.11, 2.52, 1.96, 1.10, 0.89, 0.86, 0.82, 0.80]; % мА
poly_U = [10.85, 5.55, 3.14, 1.78, 1.53, 0.82, 0.64, 0.62, 0.59, 0.55]; % В

% === РАСЧЕТЫ ===
% Мощность P = I * U (мВт)
mono_P = mono_I .* mono_U;
poly_P = poly_I .* poly_U;

% Относительная мощность P_rel = (P / P_max_initial) * 100 %
mono_Prel = (mono_P ./ mono_P(1)) * 100;
poly_Prel = (poly_P ./ poly_P(1)) * 100;

% === ПОСТРОЕНИЕ ГРАФИКОВ ===

% 1. Зависимость Тока от кол-ва закрытых элементов I(N)
f1 = figure('Position', [0, 0, 800, 600]);
plot(N, mono_I, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(N, poly_I, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
grid on;
xlabel('Количество закрытых элементов (шт)');
ylabel('Ток нагрузки, мА');
title('Влияние частичного затенения на ток');
legend('Location', 'northeast');
exportgraphics(f1, './results/current_shading.png', 'Resolution', 300);

% 2. Зависимость Напряжения от кол-ва закрытых элементов U(N)
f2 = figure('Position', [0, 0, 800, 600]);
plot(N, mono_U, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(N, poly_U, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
grid on;
xlabel('Количество закрытых элементов (шт)');
ylabel('Напряжение на нагрузке, В');
title('Влияние частичного затенения на напряжение');
legend('Location', 'northeast');
exportgraphics(f2, './results/voltage_shading.png', 'Resolution', 300);

% 3. Зависимость Мощности от кол-ва закрытых элементов P(N)
f3 = figure('Position', [0, 0, 800, 600]);
plot(N, mono_P, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(N, poly_P, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
grid on;
xlabel('Количество закрытых элементов (шт)');
ylabel('Выходная мощность, мВт');
title('Деградация мощности при затенении');
legend('Location', 'northeast');
exportgraphics(f3, './results/power_shading.png', 'Resolution', 300);

% 4. Относительное падение мощности (%)
f4 = figure('Position', [0, 0, 800, 600]);
plot(N, mono_Prel, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(N, poly_Prel, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
yline(50, '--k', '50%'); % Уровень 50%
yline(10, ':k', '10%');  % Уровень 10%
grid on;
xlabel('Количество закрытых элементов (шт)');
ylabel('Относительная мощность (% от макс.)');
title('Относительное падение эффективности');
legend('Location', 'northeast');
exportgraphics(f4, './results/rel_power_shading.png', 'Resolution', 300);

close all;