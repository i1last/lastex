x = linspace(-5, 5, 750);
y = linspace(-5, 5, 750);
[X, Y] = meshgrid(x, y);
Z = (X .^ 2 - 10 * cos(2 * pi .* Y)) .* (Y .^ 2 - 10 * cos((2 * pi .* X .^ 2) ./ 5));