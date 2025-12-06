% Настройка окружения
if ~exist('./results', 'dir')
    mkdir('./results');
end
set(0, 'DefaultFigureVisible', 'off');

% === ИСХОДНЫЕ ДАННЫЕ ===
% Углы (град)
angles = [90, 75, 60, 45, 30, 15, 0];

% --- МОНО панель ---
% Режим Pmax (I_mp, U_mp)
mono_Imp = [27.4, 27.1, 25.5, 22.4, 17.3, 12.3, 9.3];
mono_Ump = [12.14, 12.02, 11.31, 9.98, 7.74, 5.53, 4.12];
% Режим КЗ (I_sc)
mono_Isc = [42.8, 42.0, 35.9, 27.1, 19.1, 14.0, 9.6];
% Режим ХХ (U_oc)
mono_Uoc = [16.05, 15.75, 15.50, 15.26, 14.95, 14.60, 14.25];

% --- ПОЛИ панель ---
% Режим Pmax (I_mp, U_mp)
poly_Imp = [42.7, 38.7, 29.8, 21.7, 14.9, 10.2, 7.1];
poly_Ump = [14.93, 13.53, 10.41, 7.58, 5.22, 3.55, 2.66];
% Режим КЗ (I_sc)
poly_Isc = [45.4, 42.0, 39.3, 23.6, 15.6, 11.0, 7.5];
% Режим ХХ (U_oc)
poly_Uoc = [19.54, 19.18, 18.69, 18.19, 17.50, 16.72, 15.93];

% === РАСЧЕТЫ ===
% Мощность P = I * U (мВт)
mono_P = mono_Imp .* mono_Ump;
poly_P = poly_Imp .* poly_Ump;

% Коэффициент заполнения K = Pmax / (Uoc * Isc)
mono_K = mono_P ./ (mono_Uoc .* mono_Isc);
poly_K = poly_P ./ (poly_Uoc .* poly_Isc);

% === ПОСТРОЕНИЕ ГРАФИКОВ ===

% 1. Зависимость мощности от угла падения P(alpha)
f1 = figure('Position', [0, 0, 800, 600]);
plot(angles, mono_P, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(angles, poly_P, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
grid on;
xlabel('Угол наклона, град (\alpha)');
ylabel('Мощность, мВт (P)');
% title('Зависимость выходной мощности от угла наклона');
legend('Location', 'northeast');
xlim([0 95]);
exportgraphics(f1, './results/power_vs_angle.png', 'Resolution', 300);

% 2. Зависимость коэффициента заполнения от угла K(alpha)
f2 = figure('Position', [0, 0, 800, 600]);
plot(angles, mono_K, '-o', 'LineWidth', 2, 'DisplayName', 'Моно');
hold on;
plot(angles, poly_K, '-s', 'LineWidth', 2, 'DisplayName', 'Поли');
grid on;
xlabel('Угол наклона, град (\alpha)');
ylabel('Коэффициент заполнения (K)');
% title('Зависимость коэффициента заполнения от угла наклона');
legend('Location', 'best');
xlim([0 95]);
ylim([0 1]);
exportgraphics(f2, './results/fill_factor.png', 'Resolution', 300);

% 3. Семейство ВАХ (Аппроксимация по 3 точкам: SC, MP, OC)
f3 = figure('Position', [0, 0, 1000, 500]);

% Subplot Моно
subplot(1, 2, 1);
hold on;
colors = jet(length(angles));
for i = 1:length(angles)
    % Точки: (0, Isc), (Ump, Imp), (Uoc, 0) -> Сортировка по U
    v_pts = [0, mono_Ump(i), mono_Uoc(i)];
    i_pts = [mono_Isc(i), mono_Imp(i), 0];
    % Сплайн для плавности
    vv = linspace(0, mono_Uoc(i), 50);
    ii = pchip(v_pts, i_pts, vv);
    plot(vv, ii, 'Color', colors(i,:), 'LineWidth', 1.5, 'DisplayName', sprintf('%d^{\\circ}', angles(i)));
    plot(v_pts, i_pts, 'o', 'Color', colors(i,:), 'HandleVisibility', 'off');
end
grid on;
xlabel('Напряжение, В');
ylabel('Ток, мА');
title('ВАХ Монокристаллической панели');
legend('Location', 'northeast');
ylim([0 50]);

% Subplot Поли
subplot(1, 2, 2);
hold on;
for i = 1:length(angles)
    v_pts = [0, poly_Ump(i), poly_Uoc(i)];
    i_pts = [poly_Isc(i), poly_Imp(i), 0];
    vv = linspace(0, poly_Uoc(i), 50);
    ii = pchip(v_pts, i_pts, vv);
    plot(vv, ii, 'Color', colors(i,:), 'LineWidth', 1.5, 'DisplayName', sprintf('%d^{\\circ}', angles(i)));
    plot(v_pts, i_pts, 's', 'Color', colors(i,:), 'HandleVisibility', 'off');
end
grid on;
xlabel('Напряжение, В');
ylabel('Ток, мА');
title('ВАХ Поликристаллической панели');
legend('Location', 'northeast');
ylim([0 50]);

exportgraphics(f3, './results/iv_family.png', 'Resolution', 300);

close all;