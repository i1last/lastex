function result_matrix = ex3_2(matrix, operation_mode)
    % ex3_2 выполняет операцию над матрицей
    %   matrix - входная матрица
    %   operation_mode - 'sum' или 'mul' для накопительной суммы/произведения
    %   result_matrix - матрица с результатами

    if operation_mode ~= "sum" && operation_mode ~= "mul"
        error('Неизвестная операция. Доступные: sum, mul');
    end

    result_matrix = matrix;
    switch operation_mode
        case 'sum'
            for col = 1:size(matrix, 2)
                for row = 2:size(matrix, 1)
                    result_matrix(row, col) = result_matrix(row, col) + result_matrix(row-1, col);
                end
            end
        case 'mul'
            for col = 1:size(matrix, 2)
                for row = 2:size(matrix, 1)
                    result_matrix(row, col) = result_matrix(row, col) * result_matrix(row-1, col);
                end
            end
    end
end