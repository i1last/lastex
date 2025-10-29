function [varargout] = table_1_func()
    % Функция для вычисления значений функции из таблицы 1 для варианта 3
    
    file = fopen('./src/table_1.csv', 'r');
    x_lens = textscan(file, '%f;%f', 'HeaderLines', 1);
    fclose(file);

    ox1 = linspace(-5, 5, x_lens{1});
    ox2 = linspace(-5, 5, x_lens{2});
    [x1, x2] = meshgrid(ox1, ox2);
    y =  (x1 .^ 2 - 10 * cos(2 * pi .* x2)) .* (x2 .^ 2 - 10 * cos((2 * pi .* x1 .^ 2) ./ 5));
    

    if nargout <= 1
        result.x1 = x1;
        result.x2 = x2;
        result.y = y;
        
        varargout{1} = result;
    else if nargout == 3
        varargout{1} = x1;
        varargout{2} = x2;
        varargout{3} = y;
    end
end
