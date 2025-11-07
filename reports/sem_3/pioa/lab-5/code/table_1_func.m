function [varargout] = table_1_func(x_range_from, x_range_to, x1_len, x2_len)
    % Функция для вычисления значений функции из таблицы 1 для варианта 3
    % Входные параметры:
    %   x_range_from - начало диапазона для x1 и x2
    %   x_range_to   - конец диапазона для x1 и x2
    %   x1_len       - количество точек по оси x1
    %   x2_len       - количество точек по оси x2

    ox1 = linspace(x_range_from, x_range_to, x1_len);
    ox2 = linspace(x_range_from, x_range_to, x2_len);
    [x1, x2] = meshgrid(ox1, ox2);
    y =  (x1 .^ 2 - 10 * cos(2 * pi .* x2)) .* (x2 .^ 2 - 10 * cos((2 * pi .* x1 .^ 2) ./ 5));
    

    if nargout <= 1
        result.x1 = x1;
        result.x2 = x2;
        result.y = y;
        
        varargout{1} = result;
    elseif nargout == 3
        varargout{1} = x1;
        varargout{2} = x2;
        varargout{3} = y;
    end
end
