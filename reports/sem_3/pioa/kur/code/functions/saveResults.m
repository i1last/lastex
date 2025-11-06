function [ ] = saveResults(optimalPathLength, nmeaMessages, resultsFilePath)
    % Сохранение результатов в файл.
    % Входные аргументы:
    %   optimalPathLength: Длина оптимального пути.
    %   nmeaMessages: Массив ячеек (cell array) с NMEA-сообщениями.
    %   resultsFilePath: Путь к файлу для сохранения результатов.

    output_file = fopen(resultsFilePath, "w");

    if output_file == -1
        error("saveResults(): Ошибка в создании файла.")
    end

    fprintf(output_file, 'Optimal Path Length: %.2f km\n\n', optimalPathLength);

    fprintf(output_file, 'NMEA Messages:\n');
    for i = 1 : length(nmeaMessages)
        fprintf(output_file, '%s\n', nmeaMessages{i});
    end

    fclose(output_file);
end