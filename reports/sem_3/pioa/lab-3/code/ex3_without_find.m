%% Формируем графики ниже и выше плоскости сечения
Z_up_slice = Z;
Z_down_slice = Z;

Z_up_slice(Z <= slice) = NaN;
Z_down_slice(Z >= slice) = slice;


%% Поиск 10 наибольших значений ограниченного верхнего графика (задание 3)
[~, top_10_max__indexes] = maxk(Z_up_slice(:), 10);

top_10_X = X(top_10_max__indexes)';
top_10_Y = Y(top_10_max__indexes)';
top_10_Z = Z(top_10_max__indexes)';

top_10_max__values = [
    top_10_X;
    top_10_Y;
    top_10_Z
];

fprintf('Поиск 10 наибольших значений ограниченного верхнего графика:')
for i = 1:10
    fprintf('\n\tf(%+f,\t%+f)=%f', top_10_X(i), top_10_Y(i), top_10_Z(i))
end
fprintf('\n\n')