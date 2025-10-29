clear, clc

%% Исходное изображени
img = imread('./imgs/bre.png');

figure;
imshow(img);
title('Исходное изображение');

[rows, cols, channels] = size(img)

%% Деление на 4 части

half_rows = floor(rows / 2);
half_cols = floor(cols / 2);

%  NW  North  NE
% West       East
%  SW  South  SW
nw = img(1 : half_rows, 1 : half_cols, :);
ne = img(1 : half_rows, half_cols + 1 : end, :);
sw = img(half_rows + 1 : end, 1 : half_cols, :);
se = img(half_rows + 1 : end, half_cols + 1 : end, :);

figure;
subplot(2, 2, 1), imshow(nw);
subplot(2, 2, 2), imshow(ne);
subplot(2, 2, 3), imshow(sw);
subplot(2, 2, 4), imshow(se);

%% Обработка разделенных частей

% --- Зеркальное отражение
% flip() меняет порядок элементов в каждом столбце на обратный,
% а flip(..., 2) - в каждой строке. В нашем случае отражение
% относительно вертикали
nw_mirror = flip(nw, 2);

% --- Полный разворот
% rot90(..., k) - повернуть на 90 градусов k раз
ne_180 = rot90(ne, 2);

% --- Инверсия цвета
sw_inversion = imcomplement(sw);

% --- Замена одного цвета на другой (заменим цвет пиджаков на красный)
se_replaced = se;

color = [15 15 15];  % примерный цвет пиджаков
color_error = color(1);  % устанавливаем погрешность
color_mask = ...
    (color(1) - color_error <= se(:, :, 1) & se(:, :, 1) <= color(1) + color_error) &...
    (color(2) - color_error <= se(:, :, 2) & se(:, :, 2) <= color(2) + color_error) &...
    (color(3) - color_error <= se(:, :, 3) & se(:, :, 3) <= color(3) + color_error);

% uint8, поскольку цвета 0..255 (8 бит):
se_replaced(:, :, 1) = se(:, :, 1) .* uint8(~color_mask) + uint8(color_mask .* 255);
se_replaced(:, :, 2) = se(:, :, 2) .* uint8(~color_mask);  % оставляем все пиксели, которые
se_replaced(:, :, 3) = se(:, :, 3) .* uint8(~color_mask);  % не подходят под условие маски

figure;
subplot(2, 2, 1), imshow(nw_mirror);
subplot(2, 2, 2), imshow(ne_180);
subplot(2, 2, 3), imshow(sw_inversion);
subplot(2, 2, 4), imshow(se_replaced);