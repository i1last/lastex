dofile('./protocol.lua')

processed = {
    CdS = {},
    CdSe = {},
    Intensity = {}
}

-- Функция для обработки спектральных характеристик
local function process_spectral(raw_data, R_dark)
    local res = {
        gamma_c = {},
        gamma_f = {},
        gamma_f_prime = {},
        rel = {}
    }
    
    -- Темновая проводимость в мкСм
    local gamma_t = (1 / R_dark) * 1e6
    local max_prime = 0
    local max_idx = 1

    for i = 1, #raw_data.R_c do
        -- Световая проводимость в мкСм
        local g_c = (1 / raw_data.R_c[i]) * 1e6
        -- Фотопроводимость
        local g_f = g_c - gamma_t
        if g_f < 0 then g_f = 0 end 
        
        -- Приведенная фотопроводимость
        local g_f_prime = g_f / raw_data.E_lambda[i]

        table.insert(res.gamma_c, g_c)
        table.insert(res.gamma_f, g_f)
        table.insert(res.gamma_f_prime, g_f_prime)

        if g_f_prime > max_prime then
            max_prime = g_f_prime
            max_idx = i
        end
    end

    -- Относительная фотопроводимость и поиск красной границы (интерполяция)
    local lambda_half = 0
    local lambda_half_x1 = 0
    local lambda_half_x2 = 0
    local lambda_half_y1 = 0
    local lambda_half_y2 = 0
    for i = 1, #res.gamma_f_prime do
        local rel_val = res.gamma_f_prime[i] / max_prime
        table.insert(res.rel, rel_val)

        -- Поиск пересечения уровня 0.5 на длинноволновом (правом) спаде
        if i > max_idx and res.rel[i-1] >= 0.5 and rel_val <= 0.5 then
            local x1 = raw_data.lambda[i-1] * 1e6
            local x2 = raw_data.lambda[i] * 1e6
            local y1 = res.rel[i-1]
            local y2 = rel_val
            
            -- Линейная интерполяция
            lambda_half = x1 + (x2 - x1) * (0.5 - y1) / (y2 - y1)
            lambda_half_x1 = x1
            lambda_half_x2 = x2
            lambda_half_y1 = y1
            lambda_half_y2 = y2
        end
    end

    res.max_prime = max_prime
    res.lambda_half = lambda_half
    res.lambda_half_x1 = lambda_half_x1
    res.lambda_half_x2 = lambda_half_x2
    res.lambda_half_y1 = lambda_half_y1
    res.lambda_half_y2 = lambda_half_y2
    res.Eg = 1.24 / lambda_half

    return res
end

processed.CdS = process_spectral(protocol.SpectralCdS, protocol.DarkResistanceOfCdS)
processed.CdSe = process_spectral(protocol.SpectralCdSe, protocol.DarkResistanceOfCdSe)

-- Функция для обработки световой характеристики
local function process_intensity(raw_data, R_dark)
    local res = {
        gamma_c = {},
        gamma_f = {},
        d_rel = {}
    }
    local gamma_t = (1 / R_dark) * 1e6
    local d_max = 4.0 -- максимальная ширина щели в мм

    for i = 1, #raw_data.R_c do
        local g_c = (1 / raw_data.R_c[i]) * 1e6
        local g_f = g_c - gamma_t
        if g_f < 0 then g_f = 0 end
        
        -- d в протоколе хранится в метрах, переводим в мм для расчета отношения
        local d_mm = raw_data.d[i] * 1000 
        
        table.insert(res.gamma_c, g_c)
        table.insert(res.gamma_f, g_f)
        table.insert(res.d_rel, d_mm / d_max)
    end
    
    return res
end

processed.Intensity = process_intensity(protocol.Intensity, protocol.DarkResistanceOfCdSe)