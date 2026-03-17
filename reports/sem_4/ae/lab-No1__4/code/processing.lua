--[[
    Файл: processing.lua
    Описание: Расчетный модуль для лабораторной работы №4.
    Выполняет расчет коэффициентов усиления, граничных частот и
    параметров импульсных искажений.
--]]

-- Импорт исходных данных
dofile("code/protocol.lua")

r = { afc = {}, pulse = {} }

-- Вспомогательная функция для логарифмической интерполяции
-- Находит значение x, соответствующее y_target, интерполируя по
-- точкам (x1, y1) и (x2, y2) в логарифмическом масштабе.
local function log_interpolate(x1, y1, x2, y2, y_target)
    if y1 <= 0 or y2 <= 0 or y_target <= 0 then return nil end
    local log_x1, log_y1 = math.log(x1), math.log(y1)
    local log_x2, log_y2 = math.log(x2), math.log(y2)
    local log_y_target = math.log(y_target)
    if math.abs(log_y2 - log_y1) < 1e-6 then return x1 end
    local log_x_result = log_x1 + (log_x2 - log_x1) * (log_y_target - log_y1) / (log_y2 - log_y1)
    return math.exp(log_x_result)
end

local function process_afc(data)
    local res = { f = data.f, K = {}, K_max = 0, K_max_idx = 1 }
    for i = 1, #data.f do
        res.K[i] = data.outp[i] / data.inp[i]
        if res.K[i] > res.K_max then
            res.K_max = res.K[i]
            res.K_max_idx = i
        end
    end
    res.K_cutoff = res.K_max / math.sqrt(2)

    -- Поиск f_low
    for i = 2, res.K_max_idx do
        if res.K[i-1] <= res.K_cutoff and res.K[i] >= res.K_cutoff then
            res.f_low = log_interpolate(data.f[i-1], res.K[i-1], data.f[i], res.K[i], res.K_cutoff)
            break
        end
    end

    -- Поиск f_high
    for i = res.K_max_idx + 1, #data.f do
        if res.K[i-1] >= res.K_cutoff and res.K[i] <= res.K_cutoff then
            res.f_high = log_interpolate(data.f[i-1], res.K[i-1], data.f[i], res.K[i], res.K_cutoff)
            break
        end
    end
    return res
end

r.afc.woc  = process_afc(p.afc.woc)
r.afc.R3   = process_afc(p.afc.R3)
r.afc.evck = process_afc(p.afc.evck)
r.afc.ivck = process_afc(p.afc.ivck)
r.afc.nck  = process_afc(p.afc.nck)

-- Импульсные характеристики
local t_i = p.pulse.nf / 2 -- 2.5 ms

local function get_delta(f_low)
    if not f_low then return nil end
    local tau = 1 / (2 * math.pi * f_low)
    return (1 - math.exp(-t_i / tau)) * 100
end

local function get_tau(f_high)
    if not f_high then return nil end
    return 0.35 / f_high
end

r.pulse.woc = { delta = get_delta(r.afc.woc.f_low), tau = get_tau(r.afc.woc.f_high) }
r.pulse.R3  = { delta = get_delta(r.afc.R3.f_low),  tau = get_tau(r.afc.R3.f_high)  }
r.pulse.evck = { delta = get_delta(r.afc.evck.f_low), tau = get_tau(r.afc.evck.f_high) }
r.pulse.ivck = { delta = get_delta(r.afc.ivck.f_low), tau = get_tau(r.afc.ivck.f_high) }
r.pulse.nck = { delta = get_delta(r.afc.nck.f_low), tau = get_tau(r.afc.nck.f_high) }