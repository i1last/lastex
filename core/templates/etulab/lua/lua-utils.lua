---@diagnostic disable: undefined-global
LasTeX = LasTeX or {}

-- Вспомогательная функция для удаления лишних пробелов по краям строки
local function trim(s)
    return s:match("^%s*(.-)%s*$")
end

-- Безопасное разрешение пути (например, "results.table_data.U")
function LasTeX.resolve_path(path)
    if not path or path == "" then return nil end
    local current = _G
    
    -- Регулярное выражение ищет сегменты между точками
    for part in path:gmatch("[^%.]+") do
        -- Проверяем, есть ли в сегменте квадратные скобки: имя[индекс]
        local name, index = part:match("([^%[%]]+)%[(%d+)%]")
        
        if name and index then
            -- Если есть скобки, сначала берем таблицу по имени, затем элемент по индексу
            current = current[name]
            if type(current) == "table" then
                current = current[tonumber(index)]
            else
                return nil
            end
        else
            -- Если скобок нет, идем по обычному ключу
            if type(current) == "table" then
                current = current[part]
            else
                return nil
            end
        end
        
        if current == nil then return nil end
    end
    
    return current
end

-- Форматирование отдельного значения
function LasTeX.format_value(val, opt)
    if val == nil then return "---" end
    if type(val) ~= "number" then return tostring(val) end

    if opt == "exp" then
        if val == 0 then return "$0$" end
        local s = string.format("%e", val)
        local mantissa, exponent = s:match("^([^e]+)e([+-]?%d+)$")
        -- %g убирает лишние нули в мантиссе
        return string.format("$%g \\cdot 10^{%d}$", tonumber(mantissa), tonumber(exponent))
    elseif tonumber(opt) then
        -- Точность до заданного количества знаков
        return string.format("$%." .. opt .. "f$", val)
    else
        -- Стандартное поведение %f (обычно 6 знаков)
        return string.format("$%f$", val)
    end
end

-- Вывод одиночного значения
function LasTeX.print_val(path, opt)
    tex.sprint(LasTeX.format_value(LasTeX.resolve_path(path), opt))
end

-- Базовая функция извлечения среза массива
function LasTeX.join_array(path, fmt, sep, start_idx, end_idx)
    local arr = LasTeX.resolve_path(path)
    if type(arr) ~= "table" then
        tex.sprint("---")
        return
    end

    start_idx = tonumber(start_idx) or 1
    end_idx = tonumber(end_idx)
    if not end_idx or end_idx < 1 then
        end_idx = #arr
    end

    local result = {}
    for i = start_idx, end_idx do
        table.insert(result, LasTeX.format_value(arr[i], fmt))
    end

    tex.sprint(table.concat(result, sep))
end

-- Генерация строки (через &)
function LasTeX.print_row(path, fmt, start_idx, end_idx)
    LasTeX.join_array(path, fmt, " & ", start_idx, end_idx)
end

-- Генерация столбца (через \\)
function LasTeX.print_col(path, fmt, start_idx, end_idx)
    LasTeX.join_array(path, fmt, " \\\\ ", start_idx, end_idx)
end

-- Генерация блока (матрицы)
function LasTeX.print_block(paths_str, fmts_str, start_idx, end_idx)
    local paths = {}
    for p in paths_str:gmatch("[^,]+") do table.insert(paths, trim(p)) end

    local fmts = {}
    if fmts_str and fmts_str ~= "" then
        for f in fmts_str:gmatch("[^,]+") do table.insert(fmts, trim(f)) end
    end

    local arrays = {}
    local max_len = 0
    
    for i, p in ipairs(paths) do
        local arr = LasTeX.resolve_path(p)
        if type(arr) ~= "table" then arr = { arr } end
        arrays[i] = arr
        if #arr > max_len then max_len = #arr end
    end

    start_idx = tonumber(start_idx) or 1
    end_idx = tonumber(end_idx)
    if not end_idx or end_idx < 1 then end_idx = max_len end

    -- 1. Собрать все строки в массив
    local block_rows = {}
    for row = start_idx, end_idx do
        local row_data = {}
        for col_idx = 1, #arrays do
            local val = arrays[col_idx][row]
            local fmt = fmts[col_idx] or fmts[1]
            table.insert(row_data, LasTeX.format_value(val, fmt))
        end
        table.insert(block_rows, table.concat(row_data, " & "))
    end

    -- 2. Соединить строки через разделитель и вернуть единым блоком
    tex.sprint(table.concat(block_rows, " \\\\ "))
end