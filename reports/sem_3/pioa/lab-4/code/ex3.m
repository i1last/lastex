function result = ex3(matrix, search_mode, operation_mode)
    % MATRIX_OPERATIONS Выполняет операции над матрицей:
    %   matrix - входная произвольная матрица
    % 
    %   search_mode - режим поиска: 'min', 'max'.
    % 
    %   operation_mode - операция над найденными элементами: 'sum', 'mul'.
    %                    Производит накопительную сумму (произведение) столбцов (строк)
    % 
    %   result - структура с результатами

    % switch operation_mode
    %     case 'sum'
    %         result = min(matrix(:));
    %     case 'mul'
    %         result = max(matrix(:));
    %     otherwise
    %         error('Неизвестная операция над матрицей. Доступные: sum, mul');
    % end

    % switch search_place
    %     case 'row'
    %     case 'col'
    %     case 'cell'
    %     otherwise
    %         error('Неизвестная зона поиска. Доступные: row, col, cell');
    % end

    %  --- Проверка на корректность входных параметров ---
    if operation_mode ~= "sum" && operation_mode ~= "mul"
        error('Неизвестная операция над матрицей. Доступные: sum, mul');
    end

    if search_mode ~= "min" && search_mode ~= "max"
        error('Неизвестный режим поиска. Доступные: min, max');
    end

    %  --- Выполнение поиска ---
    result.value = 0;
    switch search_mode
        case 'min'
            result.value = +inf;
        case 'max'
            result.value = -inf;
    end

    result.subindex = 0;
    for row = 1 : size(matrix, 1)
        for col = 1 : size(matrix, 2)
            switch search_mode
                case 'min'
                    if matrix(row, col) < result.value
                        result.value = matrix(row, col);
                        result.subindex = [row, col];
                    end
                case 'max'
                    if matrix(row, col) > result.value
                        result.value = matrix(row, col);
                        result.subindex = [row, col];
                    end
            end
        end
    end

    % --- Выполнение операции над матрицей ---
    result.operation = matrix;
    switch operation_mode
        case 'sum'
            for col = 1 : size(matrix, 2)
                for row = 2 : size(matrix, 1)
                    result.operation(row, col) = result.operation(row, col) + result.operation(row - 1, col);
                end
            end
        case 'mul'
            for col = 1 : size(matrix, 2)
                for row = 2 : size(matrix, 1)
                     result.operation(row, col) = result.operation(row, col) * result.operation(row - 1, col);
                end
            end
    end
end
