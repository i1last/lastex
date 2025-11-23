clc; clear; close all;

% --- 1. Подготовка директории для сохранения ---
output_dir = './results';
if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

% --- 2. Ввод экспериментальных данных ---

% Монокристаллическая панель (50 Вт)
% U (Вольты), I (миллиАмперы)
U_mono = [15.8, 13.64, 13.48, 13.16, 13.3, 10.4, 8.15, 5.4, 3.94, 3.47, 3.02, 0];
I_mono = [0, 6.14, 8.1, 12.3, 20.2, 29.01, 31.11, 33.24, 33.6, 33.82, 33.91, 35.7];

% Поликристаллическая панель (50 Вт)
U_poly = [19.36, 18.92, 18.86, 18.74, 18.62, 17.46, 14.1, 12.15, 8.11, 4.2, 2.95, 0];
I_poly = [0, 9.21, 11.26, 15.02, 17.48, 32.5, 40.1, 41.3, 43.3, 44.4, 44.5, 49];

% --- 3. Расчет мощности (P = U * I) ---
P_mono = U_mono .* I_mono; % мВт
P_poly = U_poly .* I_poly; % мВт

% --- 4. Построение графика 1: ВАХ (I от U) ---
fig1 = figure('Name', 'I-V Curves', 'Color', 'w', 'Visible', 'off');
hold on;
% Сортировка для корректного отображения линий (по убыванию напряжения)
[U_mono_s, idx_m] = sort(U_mono, 'descend'); I_mono_s = I_mono(idx_m);
[U_poly_s, idx_p] = sort(U_poly, 'descend'); I_poly_s = I_poly(idx_p);

plot(U_mono_s, I_mono_s, '-ob', 'LineWidth', 1.5, 'MarkerFaceColor', 'b', 'DisplayName', 'Моно (50 Вт)');
plot(U_poly_s, I_poly_s, '-sr', 'LineWidth', 1.5, 'MarkerFaceColor', 'r', 'DisplayName', 'Поли (50 Вт)');

xlabel('Напряжение U, В');
ylabel('Ток I, мА');
legend('Location', 'SouthWest');
grid on; grid minor;
xlim([0 max([U_mono, U_poly])*1.05]);
ylim([0 max([I_mono, I_poly])*1.05]);

% Сохранение графика 1
output_path1 = fullfile(output_dir, 'iv_curves.png');
saveas(fig1, output_path1);
fprintf('График ВАХ сохранен: %s\n', output_path1);
close(fig1);

% --- 5. Построение графика 2: Мощностные характеристики (P от I) ---
fig2 = figure('Name', 'P-I Curves', 'Color', 'w', 'Visible', 'off');
hold on;

% Сортировка по возрастанию тока для графика P(I)
[I_mono_s, idx_m] = sort(I_mono, 'ascend'); P_mono_s = P_mono(idx_m);
[I_poly_s, idx_p] = sort(I_poly, 'ascend'); P_poly_s = P_poly(idx_p);

plot(I_mono_s, P_mono_s, '-ob', 'LineWidth', 1.5, 'MarkerFaceColor', 'b', 'DisplayName', 'Моно (50 Вт)');
plot(I_poly_s, P_poly_s, '-sr', 'LineWidth', 1.5, 'MarkerFaceColor', 'r', 'DisplayName', 'Поли (50 Вт)');

xlabel('Ток I, мА');
ylabel('Мощность P, мВт');
legend('Location', 'NorthWest');
grid on; grid minor;
xlim([0 max([I_mono, I_poly])*1.05]);
ylim([0 max([P_mono, P_poly])*1.05]);

% Сохранение графика 2
output_path2 = fullfile(output_dir, 'pi_curves.png');
saveas(fig2, output_path2);
fprintf('График мощности сохранен: %s\n', output_path2);
close(fig2);

fprintf('Все графики успешно сохранены в папку: %s\n', output_dir);