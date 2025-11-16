clear, clc

% Добавление директории с функциями в path для доступа к ним
addpath('./functions/');

%% Инициализация начальных условий

% Граф является неориентированным.
COND.vehicleSpeed        = 18;       % km/h
COND.batteryLifeHours    = 7;        % hours
COND.rechargeTimeMinutes = 24;       % minutes
COND.mapScale            = 40;       % km
COND.startPoint          = [-9, 7];  % [x, y]
COND.endPoint            = [8, -6];  % [x, y]

refuelingPointsFilePath = './data/refueling_points.txt';


%% Ввод данных
fprintf('--- Стандартные начальные условия ---\n');
fprintf('%-20s : %d\n', 'vehicleSpeed', COND.vehicleSpeed);
fprintf('%-20s : %d\n', 'batteryLifeHours', COND.batteryLifeHours);
fprintf('%-20s : %d\n', 'rechargeTimeMinutes', COND.rechargeTimeMinutes);
fprintf('%-20s : %d\n', 'mapScale', COND.mapScale);
fprintf('%-20s : [%d, %d]\n', 'startPoint', COND.startPoint(1), COND.startPoint(2));
fprintf('%-20s : [%d, %d]\n', 'endPoint', COND.endPoint(1), COND.endPoint(2));
fprintf('--------------------------\n');

disp('Желаете использовать стандартные начальные условия или использовать свои? [1 - свои; 0 - стандартные н.у.]');
isUserInput = input('>>> ');
if isUserInput ~= 1 && isUserInput ~= 0
    error('userInput: получено неизвестное значение');
end

if isUserInput
    % --- Ввод пользовательских начальных условий ---
    disp('vehicleSpeed: int, km/h');
    COND.vehicleSpeed = input('>>> ');

    disp('batteryLifeHours: int, hours');
    COND.batteryLifeHours = input('>>> ');

    disp('rechargeTimeMinutes: int, minutes');
    COND.rechargeTimeMinutes = input('>>> ');
    
    disp('mapScale: int, km');
    COND.mapScale = input('>>> ');
    
    disp('startPoint: [x, y]');
    COND.startPoint = input('>>> ');

    disp('endPoint: [x, y]');
    COND.endPoint = input('>>> ');

    % --- Валидация пользовательских начальных условий ---
    if length(COND.startPoint) ~= 2
        error('userInput: startPoint должно быть вектором из двух элементов [x, y]');
    elseif length(COND.endPoint) ~= 2
        error('userInput: endPoint должно быть вектором из двух элементов [x, y]');
    end

    % --- Вывод пользовательских начальных условий ---
    fprintf('--- Пользовательские начальные условия ---\n');
    fprintf('%-20s : %d\n', 'vehicleSpeed', COND.vehicleSpeed);
    fprintf('%-20s : %d\n', 'batteryLifeHours', COND.batteryLifeHours);
    fprintf('%-20s : %d\n', 'rechargeTimeMinutes', COND.rechargeTimeMinutes);
    fprintf('%-20s : %d\n', 'mapScale', COND.mapScale);
    fprintf('%-20s : [%d, %d]\n', 'startPoint', COND.startPoint(1), COND.startPoint(2));
    fprintf('%-20s : [%d, %d]\n', 'endPoint', COND.endPoint(1), COND.endPoint(2));
    fprintf('--------------------------\n');
end

disp('Желаете видеть подробный вывод в процессе выполнения программы? [1 - да; 0 - нет]');
isVerbose = input('>>> ');


%% Связывание точек в граф

nodes = readmatrix(refuelingPointsFilePath);
nodes = [COND.startPoint; nodes; COND.endPoint];
startNodeIndex = 1;             % Т.к. в массив nodes поместили вначале startPoint, затем промежуточные
endNodeIndex = size(nodes, 1);  % точки, затем конечную точку endPoint.

graph = buildGraph(nodes, COND.vehicleSpeed, COND.batteryLifeHours, COND.mapScale);
resultsFilePath = './results/graph_distances.csv';
writematrix(graph.distances, resultsFilePath);


if isVerbose
    disp('Узлы графа (координаты точек):');
    disp(graph.nodes);

    disp('Матрица смежности графа:');
    disp(graph.adjacency);

    disp('Матрица длин рёбер графа:');
    disp(graph.distances);

    fprintf('\n---\n');
end


%% Вычислене кратчайшего пути

[optimalPathIndices, optimalPathLength] = findOptimalPathByFordBellman(graph, startNodeIndex, endNodeIndex);

if isVerbose
    disp('Оптимальный путь (индексы узлов):');
    disp(optimalPathIndices');

    disp('Оптимальная длина пути:');
    disp(optimalPathLength);
    
    fprintf('\n---\n');
end


%% Генерация NMEA

nmeaMessages = generateNmeaMessages(optimalPathIndices, nodes, COND.vehicleSpeed, COND.mapScale, COND.rechargeTimeMinutes);

if isVerbose
    disp('Сгенерированные NMEA сообщения для оптимального пути:');
    for i = 1 : length(nmeaMessages)
        disp(nmeaMessages{i});
    end

    fprintf('\n---\n');
end


%% Визуализация и сохранение данных

plotFilePath = './results/optimal_route.png';
plotRoute(graph, optimalPathIndices);
print(gcf, plotFilePath, '-dpng', '-r300'); % Сохраняет текущую фигуру (gcf) в png с разрешением 300 dpi
% gcf: Get Current Figure - встроенная функция

resultsFilePath = './results/result.txt';
saveResults(optimalPathLength, nmeaMessages, resultsFilePath);

fileContent = fileread(resultsFilePath);
disp(fileContent)