function graph = buildGraph(nodes, vehicleSpeed, batteryLifeHours, mapScale)
    % Данная функция определяет возможность перемещения между узлами и возвращает
    % следующие матрицы:
    % 1. nodes - матрица координат узлов графа. Она должна иметь следующий вид:
    %     - Каждая строка соответствует одному узлу:
    %         - 1 столбец := x-координата,
    %         - 2 столбец := y-координата.
    % 2. adjacencyMatrix - матрица смежности, определяет перемещаемость между узлами графа:
    %     - Индексы строк и столбцов соответствуют номерам узлов,
    %     - Пересечение i-й строки и j-го столбца:
    %         - 1, если узлы i и j связаны ребром (т.е. можно переместиться между ними),
    %         - 0, если узлы i и j не связаны ребром.
    % 3. distanceMatrix - матрица длин рёбер:
    %     - Индексы строк и столбцов соответствуют номерам узлов,
    %     - Пересечение i-й строки и j-го столбца:
    %         - длина ребра между узлами i и j, если узлы i и j связаны,
    %         - бесконечность                 , если узлы i и j не связаны.

    if size(nodes, 2) ~= 2
        error('nodes - матрица координат узлов графа. Каждая строка соответствует одному узлу, где 1-й столбец := x-координата, 2-ой столбец := y-координата.')
    end


    maxVehicleDistance = vehicleSpeed * batteryLifeHours;

    numberOfNodes = size(nodes, 1);
    
    adjacencyMatrix = false(numberOfNodes);
    distanceMatrix = inf(numberOfNodes);
    distanceMatrix(1 : numberOfNodes + 1 : end) = 0;  % Устанавливаем главную диагональ нулевой

    for i = 1 : numberOfNodes
        for j = i + 1 : numberOfNodes  % Поскольку матрицы симметричны
            distanceBetweenNodes = sqrt((nodes(i, 1) - nodes(j, 1)) ^ 2 + (nodes(i, 2) - nodes(j, 2)) ^ 2) * mapScale;

            if distanceBetweenNodes <= maxVehicleDistance
                adjacencyMatrix(i, j) = 1;
                adjacencyMatrix(j, i) = 1;

                distanceMatrix(i, j) = distanceBetweenNodes;
                distanceMatrix(j, i) = distanceBetweenNodes;
            end
        end
    end


    graph.nodes = nodes;
    graph.adjacency = adjacencyMatrix;
    graph.distances = distanceMatrix;
end
