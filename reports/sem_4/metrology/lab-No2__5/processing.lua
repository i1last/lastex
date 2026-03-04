---@diagnostic disable: need-check-nil, param-type-mismatch
-- Вспомогательные функции
function read_csv_single(filename)
    local f = io.open(filename, "r")
    if not f then return nil end
    local content = f:read("*a")
    f:close()
    content = content:gsub("\n", "")
    local t = {}
    for str in string.gmatch(content, "([^;]*)") do
        table.insert(t, str)
    end
    return t
end

function read_csv_multi(filename)
    local data = {}
    local f = io.open(filename, "r")
    if not f then return {} end
    for line in f:lines() do
        local row = {}
        for str in string.gmatch(line, "([^;]+)") do
            table.insert(row, tonumber(str))
        end
        table.insert(data, row)
    end
    f:close()
    return data
end

function mean(t)
    local sum = 0
    for _, v in ipairs(t) do sum = sum + v end
    return sum / #t
end

function std_dev(t, avg)
    local sum_sq = 0
    for _, v in ipairs(t) do sum_sq = sum_sq + (v - avg)^2 end
    return math.sqrt(sum_sq / (#t - 1))
end

function round(num, decimals)
    local mult = 10^(decimals or 0)
    return math.floor(num * mult + 0.5) / mult
end

-- ЗАГРУЗКА ДАННЫХ
-- p1.csv: R0; dR0; Delta_instr; n; P
local p1 = read_csv_single('p1.csv')
R0 = tonumber(p1[1])
delta_R0 = tonumber(p1[2]) -- Относительная погрешность резистора (%)
Delta_instr = tonumber(p1[3]) -- Абсолютная приборная погрешность (В)
n = tonumber(p1[4])
prob_P = tonumber(p1[5]) or 0.95

-- p2.csv: U_single; U0_single
local p2 = read_csv_single('p2.csv')
U_s = tonumber(p2[1])
U0_s = tonumber(p2[2])

-- p3.csv: Multi rows
local p3_data = read_csv_multi('p3.csv')
U1_arr = {}
U2_arr = {}
for i, row in ipairs(p3_data) do
    table.insert(U1_arr, row[1])
    table.insert(U2_arr, row[2])
end

-- РАСЧЕТЫ: Однократные (Задание 2 и 3)

-- 1. Напряжение U (Задание 2)
abs_delta_U = Delta_instr
rel_delta_U = (abs_delta_U / math.abs(U_s)) * 100

-- 2. Ток I (Задание 3)
I_s = U0_s / R0
-- Погрешность измерения U0 (на резисторе R0)
abs_delta_U0 = Delta_instr
rel_delta_U0 = (abs_delta_U0 / math.abs(U0_s)) * 100
-- Относительная погрешность тока
delta_I_rel = rel_delta_U0 + delta_R0
-- Абсолютная погрешность тока
abs_delta_I = I_s * delta_I_rel / 100

-- 3. Мощность P (Задание 3)
P_s = U_s * I_s
-- Относительная погрешность мощности
delta_P_rel = rel_delta_U + delta_I_rel
-- Абсолютная погрешность мощности
abs_delta_P = math.abs(P_s) * delta_P_rel / 100


-- РАСЧЕТЫ: Многократные (Задание 4 и 5)
-- Статистическая обработка

-- Напряжение
U_mean = mean(U1_arr)
S_U = std_dev(U1_arr, U_mean)
S_U_mean = S_U / math.sqrt(n)

t_8 = 2.23
t_10 = 2.13
t_val = (t_8 + t_10) / 2
delta_U_multi = t_val * S_U_mean

-- Ток
I_arr = {}
for _, u2 in ipairs(U2_arr) do
    table.insert(I_arr, u2 / R0)
end
I_mean = mean(I_arr)
S_I = std_dev(I_arr, I_mean)
S_I_mean = S_I / math.sqrt(n)
delta_I_multi = t_val * S_I_mean

-- Мощность
P_multi_mean = U_mean * I_mean
term1 = (U_mean^2) * (S_I_mean^2)
term2 = (I_mean^2) * (S_U_mean^2)
S_Pm = math.sqrt(term1 + term2)

-- Степени свободы
num_feff = (term1 + term2)^2
den_feff = (U_mean^4 * S_I_mean^4) + (I_mean^4 * S_U_mean^4)
f_eff = (n + 1) * (num_feff / den_feff) - 2
t_val_eff = t_val -- поскольку f_eff=9
delta_P_multi = t_val_eff * S_Pm