I_phi_n = [ ...
    0.01 ...
    -0.14 ...
    0.14 ...
];

Phi = [ ...  
    0.3 ...
    0.7 ...
    1.1 ...
];

y_axis = {I_phi_n};
x_axis = Phi;

titles = {'I_{ф. н.} = f(\Phi)'};
files = {'ex3.png'};

for i = 1 : length(y_axis)
    fig = figure('Visible','off');

    plot(x_axis, y_axis{i}, 'o-');
    
    xlabel('\Phi'); ylabel('I_{ф. н.}, мкА'); title(titles{i});
    
    grid on; grid minor;
    
    xticks(x_axis);
    yticks(unique(round(y_axis{i}, 2)));
    
    saveas(fig, ['results/' files{i}]);
    close(fig);
end
