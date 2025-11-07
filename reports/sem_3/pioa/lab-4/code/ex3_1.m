function result = ex3_1(matrix)
    % ex3_1 находит минимальный элемент и столбец с ним
    %   matrix - входная матрица
    %   Выходы:
    %   - Один выход: структура с полями min_value, col_index
    %   - Два выхода: min_value, col_index

    if isempty(matrix)
        error('Матрица пуста');
    end

    % Поиск минимального элемента и его столбца
    [min_value, min_index] = min(matrix(:));
    [~, col_index] = ind2sub(size(matrix), min_index);

    % Формирование результата
    result.min_value = min_value;
    result.col_index = col_index;
    result.col = matrix(:, col_index);
end
