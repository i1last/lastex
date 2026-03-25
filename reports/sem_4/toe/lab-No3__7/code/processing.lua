-- Инициализация глобальных таблиц
r = {} -- Результаты расчетов

-- Загрузка данных протокола
dofile("code/protocol.lua")

-- Вспомогательная функция для линейной интерполяции частоты на уровне 0.707
local function get_bandwidth(f_arr, i_arr, i_0)
    local i_target = i_0 * 0.707
    local f_low, f_high
    
    -- 1. Поиск индекса фактического максимума тока
    local max_val = -1
    local max_idx = 1
    for k, v in ipairs(i_arr) do
        if v > max_val then
            max_val = v
            max_idx = k
        end
    end

    -- 2. Поиск f_low (слева от найденного максимума)
    for i = 1, max_idx - 1 do
        if i_arr[i] <= i_target and i_arr[i+1] > i_target then
            f_low = f_arr[i] + (i_target - i_arr[i]) * (f_arr[i+1] - f_arr[i]) / (i_arr[i+1] - i_arr[i])
            break
        end
    end

    -- 3. Поиск f_high (справа от найденного максимума)
    for i = max_idx, #f_arr - 1 do
        if i_arr[i] >= i_target and i_arr[i+1] < i_target then
            f_high = f_arr[i] + (i_target - i_arr[i]) * (f_arr[i+1] - f_arr[i]) / (i_arr[i+1] - i_arr[i])
            break
        end
    end

    if f_low and f_high then
        return math.abs(f_high - f_low)
    end
    return 0
end

-- В функции process_dataset вызов должен быть изменен на:


-- Основная функция обработки набора данных
local function process_dataset(id)
    local src = p[id]
    local res = {}

    -- 1. Параметры элементов
    res.R = src.U / src.I_0
    res.rho = src.U_C0 / src.I_0
    res.L = res.rho / (2 * math.pi * src.f_0)
    res.C = 1 / (2 * math.pi * src.f_0 * res.rho)

    -- 2. Добротность
    res.Q1 = src.U_C0 / src.U
    res.df = get_bandwidth(src.f, src.I, src.I_0)
    if res.df > 0 then
        res.Q2 = src.f_0 / res.df
    else
        res.Q2 = 0
    end

    -- 3. Модуль проводимости (АЧХ) для всех точек
    res.Y = {}
    for i = 1, #src.I do
        res.Y[i] = src.I[i] / src.U
    end

    r[id] = res
end

-- Обработка всех состояний контура
process_dataset("mp")
process_dataset("R1")
process_dataset("C3")