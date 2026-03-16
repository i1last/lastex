---@diagnostic disable: undefined-global
LasTeX = LasTeX or {}

-- Вспомогательная функция для удаления лишних пробелов по краям строки
local function trim(s)
    return s:match("^%s*(.-)%s*$")
end

-- Универсальный вычислитель выражений
function LasTeX.eval(expr)
    if not expr or expr == "" then return nil end
    
    -- Пытаемся скомпилировать строку как "return <выражение>"
    local f, err = load("return " .. expr)
    if f then
        -- Выполняем функцию в глобальном окружении
        local status, result = pcall(f)
        if status then
            return result
        end
    end
    return nil
end

-- Форматирование отдельного значения
function LasTeX.format_value(val, opt, is_math)
    if val == nil then return "---" end
    
    local res = ""
    if type(val) ~= "number" then 
        res = tostring(val) 
    elseif opt == "exp" then
        if val == 0 then 
            res = "0" 
        else
            local s = string.format("%e", val)
            local mantissa, exponent = s:match("^([^e]+)e([+-]?%d+)$")
            res = string.format("%g \\cdot 10^{%d}", tonumber(mantissa), tonumber(exponent))
        end
    elseif tonumber(opt) then
        res = string.format("%." .. opt .. "f", val)
    else
        res = string.format("%f", val)
    end

    if is_math then
        return "$" .. res .. "$"
    else
        return res
    end
end

-- Вывод одиночного значения
function LasTeX.print_val(expr, opt, is_math)
    local val = LasTeX.eval(expr)
    tex.sprint(LasTeX.format_value(val, opt, is_math))
end

-- Базовая функция извлечения среза массива
function LasTeX.join_array(expr, fmt, sep, start_idx, end_idx, is_math)
    local arr = LasTeX.eval(expr)
    if type(arr) ~= "table" then
        tex.sprint("---")
        return
    end

    start_idx = tonumber(start_idx) or 1
    end_idx = tonumber(end_idx)
    if not end_idx or end_idx < 1 then end_idx = #arr end

    local result = {}
    for i = start_idx, end_idx do
        table.insert(result, LasTeX.format_value(arr[i], fmt, is_math))
    end
    tex.sprint(table.concat(result, sep))
end

-- Генерация строки (через &)
function LasTeX.print_row(path, fmt, start_idx, end_idx, is_math)
    LasTeX.join_array(path, fmt, " & ", start_idx, end_idx, is_math)
end

-- Генерация столбца (через \\)
function LasTeX.print_col(path, fmt, start_idx, end_idx, is_math)
    LasTeX.join_array(path, fmt, " \\\\ ", start_idx, end_idx, is_math)
end

-- Генерация блока (матрицы)
function LasTeX.print_block(exprs_str, fmts_str, start_idx, end_idx, is_math)
    local exprs = {}
    for e in exprs_str:gmatch("[^,]+") do table.insert(exprs, trim(e)) end

    local fmts = {}
    if fmts_str and fmts_str ~= "" then
        for f in fmts_str:gmatch("[^,]+") do table.insert(fmts, trim(f)) end
    end

    local arrays = {}
    local max_len = 0
    for i, e in ipairs(exprs) do
        local arr = LasTeX.eval(e)
        if type(arr) ~= "table" then arr = { arr } end
        arrays[i] = arr
        if #arr > max_len then max_len = #arr end
    end

    start_idx = tonumber(start_idx) or 1
    end_idx = tonumber(end_idx)
    if not end_idx or end_idx < 1 then end_idx = max_len end

    local block_rows = {}
    for row = start_idx, end_idx do
        local row_data = {}
        for col_idx = 1, #arrays do
            local val = arrays[col_idx][row]
            local fmt = fmts[col_idx] or fmts[1]
            table.insert(row_data, LasTeX.format_value(val, fmt, is_math))
        end
        table.insert(block_rows, table.concat(row_data, " & "))
    end
    tex.sprint(table.concat(block_rows, " \\\\ "))
end