x_positive = 0 : 0.01 : 10;
y_positive = (                 x_positive <= 2) .* (-x_positive) +...
             (2 < x_positive & x_positive <= 6) .* (-2) +...
             (6 < x_positive                  ) .* (+3);

% Создаем симметричную часть
x_negative = -fliplr(x_positive); % Отражаем x
y_negative = -fliplr(y_positive); % Функция нечетная, если f(-x) = -f(x)

% Объединяем
x = [x_negative, x_positive(2:end)]; % 2:end, поскольку 0 уже включен в x_negative
y = [y_negative, y_positive(2:end)]; % аналогично

% Построение графика
plot(x, y);
grid on;
xlabel('x'); ylabel('f(x)');
title('Нечетная функция на [-10, 10]');