function [ ] = plotRoute(graph, optimalPathIndices)
    % PLOUTEROUTE Функция для визуализации маршрута на графе.
    % Входные параметры:
    %   graph - структура графа:
    %       .nodes     - матрица координат узлов графа
    %       .adjacency - матрица смежности графа
    %       .distances - матрица длин рёбер графа
    %   optimalPathIndices - индексы узлов, составляющих оптимальный путь

    if isempty(optimalPathIndices)
        error('plotRoute(): Оптимальный путь не найден')
    end

    figure;
    hold on;

    % Отрисовка всех узлов графа
    h_nodes = plot(graph.nodes(:, 1), graph.nodes(:, 2), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 5);
    %                                     black-^^-circle  ^- заливка    ^-черным

    % Отрисовка всевозможных путей
    h_possible = [];
    for i = 1 : length(graph.adjacency)
        for j = 1 : length(graph.adjacency)
            if graph.adjacency(i, j) == 1
                h_possible = plot(...
                    [graph.nodes(i, 1), graph.nodes(j, 1)],...  % x_i x_j
                    [graph.nodes(i, 2), graph.nodes(j, 2)],...  % y_i y_j
                    'k:');                         % 'k--' = black dashed
                
                % Координаты середины ребра
                mid_x = (graph.nodes(i, 1) + graph.nodes(j, 1)) / 2;
                mid_y = (graph.nodes(i, 2) + graph.nodes(j, 2)) / 2;
                
                % Расстояние между точками
                distance = graph.distances(i, j);
                label_str = sprintf('%.2f', distance);
                
                % Выводим текст на график
                text(mid_x, mid_y, label_str, 'FontSize', 10, 'Color', [0.5 0.5 0.5]);
            end
        end
    end

    % Отрисовка оптимального пути
    h_optimal = [];
    for i = 1 : length(optimalPathIndices) - 1
        idx1 = optimalPathIndices(i);
        idx2 = optimalPathIndices(i + 1);
        x_coords = [graph.nodes(idx1, 1), graph.nodes(idx2, 1)];
        y_coords = [graph.nodes(idx1, 2), graph.nodes(idx2, 2)];

        h_optimal = plot(x_coords, y_coords, '-r', 'LineWidth', 2);
    end

    % Выделение начальной и конечной точек
    startNodeCoords = graph.nodes(optimalPathIndices(1), :);
    endNodeCoords = graph.nodes(optimalPathIndices(end), :);
    h_start = plot(startNodeCoords(1), startNodeCoords(2), 'go', 'MarkerFaceColor', 'g', 'MarkerSize', 8); % Зеленый старт
    h_finish = plot(endNodeCoords(1), endNodeCoords(2), 'mo', 'MarkerFaceColor', 'm', 'MarkerSize', 8);     % Пурпурный финиш


    handles = [h_nodes, h_possible, h_optimal, h_start, h_finish];
    labels = {'Узлы', 'Возможные пути', 'Оптимальный путь', 'Старт', 'Финиш'};

    grid on;
    title('Визуализация маршрута на графе');
    xlabel('x')
    ylabel('y');
    legend(handles, labels, 'Location', 'best');
    axis equal;
    hold off;
end