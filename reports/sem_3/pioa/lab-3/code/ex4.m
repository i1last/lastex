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