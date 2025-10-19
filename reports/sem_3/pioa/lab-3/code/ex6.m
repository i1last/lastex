if fixed_axis == 1  % fix X
    argument_array = y;
    projection_array = Z_up_slice(:, fixed_col);
else  % fix Y
    argument_array = x;
    projection_array = Z_up_slice(fixed_row, :)';
end


if showFigures
    figure('Name','Проекция верхнего огр. графика','NumberTitle','off');
    
    subplot(2, 2, 1), plot(argument_array, projection_array)
    title(['Проекция при ' fixed_axis_str ' == const'])
    xlabel(['Ось ' unfixed_axis_str])
    ylabel("Ось z")

    subplot(2, 2, 2), plot(argument_array, -projection_array + 2 * slice)
    title('Операция после отражения')
    xlabel(['Ось ' unfixed_axis_str])
    ylabel("Ось z")

    subplot(2, 2, 3), plot(argument_array, 2 * projection_array - slice)
    title('Операция растяжения в 2 раза')
    xlabel(['Ось ' unfixed_axis_str])
    ylabel("Ось z")

    subplot(2, 2, 4)
    hold on
    plot(argument_array, projection_array)              % Исходный
    plot(argument_array, x * 0 + slice)  % Линия уровня
    plot(argument_array, -projection_array + 2 * slice) % Отраженный
    plot(argument_array, 2 * projection_array - slice)  % Растянутый
    hold off
    legend('Исходный', 'Линия уровня', 'Отраженный', 'Растянутый')
    title('Все операции вместе')
    xlabel(['Ось ' unfixed_axis_str])
    ylabel("Ось z")
end