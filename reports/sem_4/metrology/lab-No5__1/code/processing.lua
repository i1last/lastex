-- code/processing.lua
-- dofile("protocol.lua")
dofile("code/protocol.lua")

r = {
    vdc = {},
    vac = {},
    idc = {},
    afc = {}
}

-- Функция для расчета погрешностей
local function process_errors(mode, x_N)
    local data = p[mode]
    local res = {
        dx_up = {},
        dx_down = {},
        dx_max = {},
        delta = {},
        gamma = {},
        H = {}
    }
    
    local max_gamma_abs = 0

    for i = 1, #data.x do
        local x = data.x[i]
        local x_up = data.x_up[i]
        local x_down = data.x_down[i]

        -- Абсолютные погрешности
        local dx_up = math.abs(x - x_up)
        local dx_down = math.abs(x - x_down)

        -- Выбор максимальной по модулю с сохранением знака
        local dx_max = dx_up
        if math.abs(dx_down) > math.abs(dx_up) then
            dx_max = dx_down
        end

        -- Относительная, приведенная погрешности и вариация
        local delta = (dx_max / x) * 100
        local gamma = (dx_max / x_N) * 100
        local H = (math.abs(x_up - x_down) / x_N) * 100

        table.insert(res.dx_up, dx_up)
        table.insert(res.dx_down, dx_down)
        table.insert(res.dx_max, dx_max)
        table.insert(res.delta, delta)
        table.insert(res.gamma, gamma)
        table.insert(res.H, H)

        if math.abs(gamma) > max_gamma_abs then
            max_gamma_abs = math.abs(gamma)
        end
    end
    
    res.max_gamma = max_gamma_abs
    r[mode] = res
end

-- Нормирующие значения (верхние пределы)
local vdc_N = p.vdc.x[#p.vdc.x]
local vac_N = p.vac.x[#p.vac.x]
local idc_N = p.idc.x[#p.idc.x]

process_errors("vdc", vdc_N)
process_errors("vac", vac_N)
process_errors("idc", idc_N)

-- Поиск глобальной максимальной приведенной погрешности
r.global_max_gamma = math.max(r.vdc.max_gamma, r.vac.max_gamma, r.idc.max_gamma)

-- Обработка АЧХ
r.afc.K = {}
for i = 1, #p.afc.f do
    local k_val = p.afc.U[i] / p.afc.U_50Hz
    table.insert(r.afc.K, k_val)
end

-- Интерполяция верхней частоты среза (спад 10%, K = 0.9)
r.afc.f_high = 0
for i = 1, #p.afc.f - 1 do
    if r.afc.K[i] >= 0.9 and r.afc.K[i+1] < 0.9 then
        local f1, f2 = p.afc.f[i], p.afc.f[i+1]
        local k1, k2 = r.afc.K[i], r.afc.K[i+1]
        r.afc.f_high = f1 + (0.9 - k1) * (f2 - f1) / (k2 - k1)
        break
    end
end