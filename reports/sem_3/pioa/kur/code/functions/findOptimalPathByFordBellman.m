function [optimalPathIndices, optimalPathLength] = findOptimalPathByFordBellman(graph, startNodeIndex, endNodeIndex)
    % Данная функция находит оптимальный путь в графе с помощью алгоритма Форда-Беллмана.
    % Входные параметры:
    %   graph - структура графа, содержащая поля:
    %       .nodes - матрица координат узлов графа
    %       .distances - матрица расстояний между узлами графа
    %   startNodeIndex - индекс начального узла
    %   endNodeIndex - индекс конечного узла
    % Возвращаемые параметры:
    %   optimalPathIndices - массив индексов узлов, составляющих оптимальный путь
    %   optimalPathLength - длина оптимального пути

    numberOfNodes = size(graph.nodes, 1);
    
    distances = inf(1, numberOfNodes);
    distances(startNodeIndex) = 0;

    predecessors = NaN(1, numberOfNodes);

    % Алгоритм будет выполнен после N - 1 итераций, где N - количество узлов
    for reflections = 1 : numberOfNodes - 1
        for i = 1 : numberOfNodes
            for j = 1 : numberOfNodes
                
                % Проверяем, что ребро между узлами i и j существует
                if distances(i) == inf || graph.distances(i, j) == inf
                    continue
                end

                if distances(i) + graph.distances(i, j) < distances(j)
                    distances(j) = distances(i) + graph.distances(i, j);
                    predecessors(j) = i;
                end
            end
        end
    end


    optimalPathLength = distances(endNodeIndex);
    
    if optimalPathLength == inf
        optimalPathIndices = [];
        return;
    end

    path = [];
    currentNode = endNodeIndex;
    while ~isnan(currentNode)
        path = [currentNode, path];  % Развертываение происходит в обратном порядке
        
        if currentNode == startNodeIndex
            break; % Путь успешно построен
        end
        currentNode = predecessors(currentNode);
    end
    
    % Если цикл завершился, а до начальной точки не дошли, значит путь оборван
    if path(1) ~= startNodeIndex
        optimalPathIndices = [];
    else
        optimalPathIndices = path;
    end
end
