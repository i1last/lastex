random_val = randi(10);

fixed_point = top_10_max__values(:, random_val);

fixed_ind_index = top_10_max__indexes(random_val);
[fixed_row, fixed_col] = ind2sub(size(Z_up_slice), fixed_ind_index);

fixed_axis = randi(2);  % Выбираем случайную ось. 1 == X; 2 == Y

if fixed_axis == 1  % fix X
    fixed_axis_str = 'x';
    unfixed_axis_str = 'y';

    argument_array = y;
    projection_array = Z(:, fixed_col);
else  % fix Y
    fixed_axis_str = 'y';
    unfixed_axis_str = 'x';

    argument_array = x;
    projection_array = Z(fixed_row, :)';
end

if showFigures
    figure('Name','Проекция графика','NumberTitle','off');
    plot(argument_array, projection_array)
    ylim([min_Z_val max_Z_val])
    title(['Проекция при ' fixed_axis_str ' == const'])
    xlabel(['Ось ' unfixed_axis_str])
    ylabel("Ось z")
end