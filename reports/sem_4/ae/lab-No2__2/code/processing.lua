-- Инициализация и импорт протокола
dofile("code/protocol.lua")

-- Глобальная таблица результатов
r = {}

--------------------------------------------------------------------------------
-- 1. Обработка амплитудных характеристик (АХ)
--------------------------------------------------------------------------------
r.U_lin_max = { oe = 0, ob = 0, ok = 0 }

-- Функция поиска границы линейного участка
-- Критерий: падение дифференциального коэффициента усиления ниже 80% от начального
local function find_ulin_max(Uin, Uout)
    local K0 = Uout[1] / Uin[1]
    local last_good_Uin = Uin[1]
    
    for i = 2, #Uin do
        local dU_out = Uout[i] - Uout[i-1]
        local dU_in = Uin[i] - Uin[i-1]
        local K_diff = dU_out / dU_in
        
        if K_diff < K0 * 0.8 then
            break
        end
        last_good_Uin = Uin[i]
    end
    return last_good_Uin
end

r.U_lin_max.oe = find_ulin_max(p.ax.Uin, p.ax.Uoe)
r.U_lin_max.ob = find_ulin_max(p.ax.Uin, p.ax.Uob)
r.U_lin_max.ok = find_ulin_max(p.ax.Uin, p.ax.Uok)

--------------------------------------------------------------------------------
-- 2. Обработка амплитудно-частотных характеристик (АЧХ)
--------------------------------------------------------------------------------
r.K = { oe = {}, ob = {}, ok = {} }
r.max_K = { oe = 0, ob = 0, ok = 0 }

-- Расчет коэффициентов усиления и поиск максимумов
local Uin_achx = p.achx.Uin
for i = 1, #p.achx.f do
    r.K.oe[i] = p.achx.Uoe[i] / Uin_achx
    r.K.ob[i] = p.achx.Uob[i] / Uin_achx
    r.K.ok[i] = p.achx.Uok[i] / Uin_achx
    
    if r.K.oe[i] > r.max_K.oe then r.max_K.oe = r.K.oe[i] end
    if r.K.ob[i] > r.max_K.ob then r.max_K.ob = r.K.ob[i] end
    if r.K.ok[i] > r.max_K.ok then r.max_K.ok = r.K.ok[i] end
end

--------------------------------------------------------------------------------
-- 3. Расчет граничных частот
--------------------------------------------------------------------------------
r.thresh = {
    oe = r.max_K.oe * 0.7,
    ob = r.max_K.ob * 0.7,
    ok = r.max_K.ok * 0.7
}

-- Функция логарифмической интерполяции для поиска частоты среза
local function find_cutoff(f, K, thresh, search_lower)
    local max_idx = 1
    for i = 1, #K do
        if K[i] > K[max_idx] then max_idx = i end
    end

    if search_lower then
        -- Поиск нижней частоты (от начала до максимума)
        for i = 1, max_idx - 1 do
            if K[i] <= thresh and K[i+1] > thresh then
                local log_f1 = math.log(f[i])
                local log_f2 = math.log(f[i+1])
                local fraction = (thresh - K[i]) / (K[i+1] - K[i])
                return math.exp(log_f1 + (log_f2 - log_f1) * fraction)
            end
        end
        return f[1] -- Если срез не достигнут, возвращаем минимальную частоту
    else
        -- Поиск верхней частоты (от максимума до конца)
        for i = max_idx, #K - 1 do
            if K[i] >= thresh and K[i+1] < thresh then
                local log_f1 = math.log(f[i])
                local log_f2 = math.log(f[i+1])
                local fraction = (thresh - K[i]) / (K[i+1] - K[i])
                return math.exp(log_f1 + (log_f2 - log_f1) * fraction)
            end
        end
        return f[#f] -- Если срез не достигнут, возвращаем максимальную частоту
    end
end

r.f_low = {
    oe = find_cutoff(p.achx.f, r.K.oe, r.thresh.oe, true),
    ob = find_cutoff(p.achx.f, r.K.ob, r.thresh.ob, true),
    ok = find_cutoff(p.achx.f, r.K.ok, r.thresh.ok, true)
}

r.f_high = {
    oe = find_cutoff(p.achx.f, r.K.oe, r.thresh.oe, false),
    ob = find_cutoff(p.achx.f, r.K.ob, r.thresh.ob, false),
    ok = find_cutoff(p.achx.f, r.K.ok, r.thresh.ok, false)
}