function [ ] = table_2_func()
    % Функция для вычисления значений функции из таблицы 2 для варианта 3
    
    file = fopen('./src/table_2.csv', 'r');
    file_output = textscan(file, '%f;%f;%d;%s', 'HeaderLines', 1);
    fclose(file);

    range_start = file_output{1};
    range_end = file_output{2};
    count_of_dots = file_output{3};
    figure_type = file_output{4}{1};

    
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


