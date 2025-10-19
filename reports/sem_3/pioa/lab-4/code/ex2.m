function [x, y] = ex2(a, b, k, m, n)
    % piecewise_odd_function генерирует нечетную кусочно-линейную функцию
    %     a, b - интервальные точки кусочно-линейной функции
    %     k    - коэффициент наклона линейного участка
    %     m, n - произвольные константы для горизонтальных участков

    x_positive = 0 : 0.01 : 10;
    y_positive = (                 x_positive <= a) .* (k * x_positive) + ...
                 (a < x_positive & x_positive <= b) .* (m) + ...
                 (b < x_positive                  ) .* (n);

    x_negative = -fliplr(x_positive);
    y_negative = -fliplr(y_positive);

    x = [x_negative, x_positive(2:end)];
    y = [y_negative, y_positive(2:end)];
end