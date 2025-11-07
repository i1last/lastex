function [ ] = table_2_func(range_start, range_end, count_of_dots, figure_type)
    % Функция для вычисления значений функции из таблицы 2 для варианта 3
    % Входные параметры:
    %   range_start - начальное значение диапазона
    %   range_end - конечное значение диапазона
    %   count_of_dots - количество точек
    %   figure_type - тип графика ('semilogx', 'semilogy', 'loglog', 'plot')

    
    w = logspace(log10(range_start), log10(range_end), count_of_dots);
    s = 1j.*w;
    numerator = [1 0 12 1];
    denominator = [1 -1 2 0 6];

    A = polyval(numerator, s) ./ polyval(denominator, s);

    figure()
    switch figure_type
        case 'semilogx'
            semilogx(w, A)
        case 'semilogy'
            semilogy(w, A)
        case 'loglog'
            loglog(w, A)
        otherwise
            plot(w, A)
    end
    
    xlabel("Ось \omega")
    ylabel("Ось A")
end


