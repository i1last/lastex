prompt = 'Введите строку по прототипу "#array#:name: val1 val2 ... #endarray#":\n>>> ';
input_str = input(prompt, 's'); 

pattern = '#array#:(?<name>\w+):(?<values>[^#]+)#endarray#';

tokens = regexp(input_str, pattern, 'names');

if ~isempty(tokens)
    array_name = tokens.name;
    
    string_values = strsplit(tokens.values, ' ');
    numeric_values = str2double(string_values);

    numeric_values(isnan(numeric_values)) = []; 

    disp('--- Результаты разбора строки (Пункт 7) ---');
    disp(['Имя массива: ' array_name]);
    disp('Числовой массив:');
    disp(numeric_values);

else
    disp('Ошибка: Введенная строка не соответствует прототипу');
end