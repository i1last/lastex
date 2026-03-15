--[[
    Файл: processing.lua
    Описание: Расчет погрешностей измерений для лабораторной работы №8.
--]]

-- Подключение файла с исходными данными
dofile('protocol.lua')

-- Инициализация таблицы для хранения результатов
results = {
    resistors = {},
    capacitor = {},
    inductor = {}
}

-- Функция для форматирования чисел с заданной точностью
function format_num(val, precision)
    if val == nil then return "---" end
    return string.format('%.' .. (precision or 2) .. 'f', val)
end

--------------------------------------------------------------------------------
-- ЗАДАНИЕ 1: ОБРАБОТКА ИЗМЕРЕНИЙ АКТИВНЫХ СОПРОТИВЛЕНИЙ
--------------------------------------------------------------------------------

-- 1.1. Расчеты для измерителя иммитанса Е7-21
-- Измеренные значения R2=905.7 Ом и RN2=999 Ом попадают в диапазон 4 (100.0 - 1000 Ом).
-- Конечное значение диапазона R_k = 1000 Ом.
-- Формула относительной погрешности: delta_R = [0.15 + 0.01 * (R_k / R - 1)] %

local R_k_imm = 1000 -- Ом

-- Резистор R2
local R2_imm_val = protocol.resistors_data.R2.immitanse
local R2_imm_delta_rel = 0.15 + 0.01 * (R_k_imm / R2_imm_val - 1)
local R2_imm_delta_abs = (R2_imm_delta_rel / 100) * R2_imm_val
results.resistors.R2_imm = {
    val = R2_imm_val,
    delta_rel = R2_imm_delta_rel,
    delta_abs = R2_imm_delta_abs
}

-- Резистор RN2
local RN2_imm_val = protocol.resistors_data.RN2.immitanse
local RN2_imm_delta_rel = 0.15 + 0.01 * (R_k_imm / RN2_imm_val - 1)
local RN2_imm_delta_abs = (RN2_imm_delta_rel / 100) * RN2_imm_val
results.resistors.RN2_imm = {
    val = RN2_imm_val,
    delta_rel = RN2_imm_delta_rel,
    delta_abs = RN2_imm_delta_abs
}


-- 1.2. Расчеты для цифрового вольтметра (мультиметра)
-- Принимаем типовую погрешность для лабораторного мультиметра в режиме омметра:
-- delta_R = +-(0.5% + 2 ед. мл. разряда)
-- Абсолютная погрешность: Delta_R = 0.005 * R_изм + 2

-- Резистор R2
local R2_volt_val = protocol.resistors_data.R2.voltmetr
local R2_volt_delta_abs = 0.005 * R2_volt_val + 2
local R2_volt_delta_rel = (R2_volt_delta_abs / R2_volt_val) * 100
results.resistors.R2_volt = {
    val = R2_volt_val,
    delta_rel = R2_volt_delta_rel,
    delta_abs = R2_volt_delta_abs
}

-- Резистор RN2
local RN2_volt_val = protocol.resistors_data.RN2.voltmetr
local RN2_volt_delta_abs = 0.005 * RN2_volt_val + 2
local RN2_volt_delta_rel = (RN2_volt_delta_abs / RN2_volt_val) * 100
results.resistors.RN2_volt = {
    val = RN2_volt_val,
    delta_rel = RN2_volt_delta_rel,
    delta_abs = RN2_volt_delta_abs
}

--------------------------------------------------------------------------------
-- ЗАДАНИЕ 2: ОБРАБОТКА ИЗМЕРЕНИЙ РЕАКТИВНЫХ ЭЛЕМЕНТОВ
--------------------------------------------------------------------------------

-- 2.1. Расчеты для конденсатора
-- C = 2.094e-9 Ф = 2.094 нФ. Это диапазон 3 (1.600 - 16.00 нФ).
-- Конечное значение диапазона C_k = 16.00 нФ = 16e-9 Ф.
-- delta_C = [0.15 + 0.01(C_k/C - 1)] * sqrt(1 + tg^2(delta)) %
-- Delta_tg_delta = [2.5(1+tg^2(delta)) + C_k/C * (1+tg^2(delta))] * 10^-3

local C_s = protocol.reactive_elements.capacitor.C
local tan_delta = protocol.reactive_elements.capacitor.tandelta
local C_k = 16e-9

local C_delta_rel = (0.15 + 0.01 * (C_k / C_s - 1)) * math.sqrt(1 + tan_delta^2)
local C_delta_abs = (C_delta_rel / 100) * C_s

local tan_delta_abs = (2.5 + C_k / C_s) * (1 + tan_delta^2) * 1e-3
local tan_delta_rel = (tan_delta_abs / tan_delta) * 100

results.capacitor = {
    C_s = C_s,
    C_delta_abs = C_delta_abs,
    C_delta_rel = C_delta_rel,
    tan_delta = tan_delta,
    tan_delta_abs = tan_delta_abs,
    tan_delta_rel = tan_delta_rel
}


-- 2.2. Расчеты для катушки индуктивности
-- L = 1.028e-3 Гн = 1.028 мГн. Это диапазон 7 (160.0 - 1600 мкГн), т.е. (0.16 - 1.6) мГн.
-- Конечное значение диапазона L_k = 1.6 мГн = 1.6e-3 Гн.
-- tg(delta) = 1 / Q
-- delta_L = [0.3 + 0.06(L_k/L - 1)] * sqrt(1 + tg^2(delta)) %
-- delta_Q = [(0.25 + 0.1*L_k/L) * (Q + 1/Q)] %

local L_s = protocol.reactive_elements.induction.L
local Q_s = protocol.reactive_elements.induction.Q
local L_k = 1.6e-3
local tan_delta_L = 1 / Q_s

local L_delta_rel = (0.3 + 0.06 * (L_k / L_s - 1)) * math.sqrt(1 + tan_delta_L^2)
local L_delta_abs = (L_delta_rel / 100) * L_s

local Q_delta_rel = (0.25 + 0.1 * (L_k / L_s)) * (Q_s + 1 / Q_s)
local Q_delta_abs = (Q_delta_rel / 100) * Q_s

results.inductor = {
    L_s = L_s,
    L_delta_abs = L_delta_abs,
    L_delta_rel = L_delta_rel,
    Q_s = Q_s,
    Q_delta_abs = Q_delta_abs,
    Q_delta_rel = Q_delta_rel
}