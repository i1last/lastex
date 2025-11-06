function nmeaMessages = generateNmeaMessages(pathIndices, nodes, vehicleSpeed, mapScale, rechargeTimeMinutes)
    % Генерация NMEA сообщений для заданного пути.
    % Входные аргументы:
    %   pathIndices: Вектор с индексами узлов оптимального пути
    %   nodes: Матрица с координатами всех узлов.
    %   vehicleSpeed: Скорость объекта (км/ч).
    %   mapScale: Масштаб карты (км).
    % Выходной аргумент:
    %   nmeaMessages: Массив ячеек (cell array), где каждая ячейка содержит одну строку NMEA-сообщения.

    nmeaMessages = {};
    totalTimeHours = 0;
    prev_ZZ = 0;

    for i = 1 : length(pathIndices) - 1
        idx1 = pathIndices(i);
        idx2 = pathIndices(i + 1);

        point1 = nodes(idx1, :);
        point2 = nodes(idx2, :);


        distance_km = sqrt(...
            (point2(1) - point1(1)) ^ 2 +...
            (point2(2) - point1(2)) ^ 2) * mapScale;
        DD = round(distance_km, 2);


        segment_time_hours = distance_km / vehicleSpeed;
        totalTimeHours = totalTimeHours + segment_time_hours + (rechargeTimeMinutes / 60);
        XX = floor(totalTimeHours);
        YY = (totalTimeHours - XX) * 60;


        dx = point2(1) - point1(1);
        dy = point2(2) - point1(2);
        azimuth_rad = atan2(dy, dx);
        azimuth_deg = rad2deg(azimuth_rad);
        if azimuth_deg < 0
            azimuth_deg = azimuth_deg + 360;
        end
        ZZ = round(azimuth_deg, 1);

        if prev_ZZ == ZZ
            S1 = 'N';
        else
            S1 = 'T';
        end
        prev_ZZ = ZZ;


        if i == length(pathIndices) - 1
            S2 = 'E';
        else
            S2 = 'N';
        end

        %               $UTHDG,XX,Y.Y,DD.DD,S1,Z.Z,S2
        message = sprintf('$UTHDG,%02d,%04.1f,%06.2f,%c,%05.1f,%c', XX, YY, DD, S1, ZZ, S2);

        nmeaMessages{i} = message;
    end

end