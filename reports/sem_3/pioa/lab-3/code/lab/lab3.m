clear, clc

showFigures = 1;


%% Исходный график (задание 1)
x = linspace(-5, 5, 750);
y = linspace(-5, 5, 750);
[X, Y] = meshgrid(x, y);
Z = (X .^ 2 - 10 * cos(2 * pi .* Y)) .* (Y .^ 2 - 10 * cos((2 * pi .* X .^ 2) ./ 5));




%% Получаем значение плоскости сечения (задание 2)
prompt = sprintf('Установите уровень плоскости по оси Z (от %.2f до %.2f): ', min(min(Z)), max(max(Z)));
slice = input(prompt);
% slice = 400;




%% Формируем графики ниже и выше плоскости сечения
Z_up_slice = Z;
Z_down_slice = Z;

Z_up_slice(Z <= slice) = NaN;
Z_down_slice(Z >= slice) = slice;


%% Поиск 10 наибольших значений ограниченного верхнего графика (задание 3)
non_nan_indexes = find(~isnan(Z_up_slice(:)));

non_nan_values = Z_up_slice(non_nan_indexes);
[~, sorted_idx] = sort(non_nan_values, 'descend');

top_10_max__indexes = non_nan_indexes(sorted_idx(1:min(10, end)));


top_10_X = X(top_10_max__indexes)';
top_10_Y = Y(top_10_max__indexes)';
top_10_Z = Z(top_10_max__indexes)';
top_10_max__values = [top_10_X; top_10_Y; top_10_Z];

fprintf('Поиск 10 наибольших значений ограниченного верхнего графика:')
for i = 1:10
    fprintf('\n\tf(%+f,\t%+f)=%f', top_10_X(i), top_10_Y(i), top_10_Z(i))
end
fprintf('\n\n')





%% Отображаем графики (задание 4)
max_Z_val = 1000; % max(max(Z));
min_Z_val = -400; % min(min(Z));

if showFigures
    figure('Name','Исходный график','NumberTitle','off');
    surf(X, Y, Z)
    title("Исходный график")
    xlabel("Ось x")
    ylabel("Ось y")
    zlabel("Ось z")

    figure('Name','Нижний ограниченный график','NumberTitle','off');
    surf(X, Y, Z_down_slice)
    zlim([min_Z_val max_Z_val])
    title("Ограниченный плоскостью график (нижний)")
    xlabel("Ось x")
    ylabel("Ось y")
    zlabel("Ось z")

    figure('Name','Верхний ограниченный график','NumberTitle','off');
    surf(X, Y, Z_up_slice)
    zlim([min_Z_val max_Z_val])
    title("Ограниченный плоскостью график (верхний)")
    xlabel("Ось x")
    ylabel("Ось y")
    zlabel("Ось z")
end


%% Выбираем случайную точку из задания 3 и извлекаем проекцию поверхности (задание 5)

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



%% Работа с диапазонами над плоскостью сечения (задание 6)

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



%% Вывод данных (задание 7)

prompt = 'Введите строку по прототипу "#array#:name: val1 val2 ... #endarray#":\n>>> ';
input_str = input(prompt, 's'); 

pattern = '#array#:(?<name>\w+):(?<values>[^#]+)#endarray#';

tokens = regexp(input_str, pattern, 'names');

if ~isempty(tokens)
    array_name = tokens.name;
    
    string_values = strsplit(tokens.values, ' ');
    numeric_values = str2double(string_values);

    numeric_values(isnan(numeric_values)) = []; 

    disp('--- Результаты разбора строки (Пункт 7) ---');
    disp(['Имя массива: ' array_name]);
    disp('Числовой массив:');
    disp(numeric_values);

else
    disp('Ошибка: Введенная строка не соответствует прототипу');
end