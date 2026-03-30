dofile("code/protocol.lua")
-- dofile("protocol.lua")

r = {
    fc = {},
    of = {},
    ph = {},
    const = {
        b = 0.025,      -- визуальная погрешность (толщина луча), дел
        d_kp = 3.0,   -- погрешность коэффициента развертки, %
        d_nr = 2.0    -- нелинейность развертки, %
    }
}

-- 1. Обработка данных цифрового частотомера
for var_name, data in pairs(p.fc) do
    r.fc[var_name] = { dF = {}, relF = {}, k = {} }
    for i, fx in ipairs(data.f_x) do
        -- Определение шага квантования k по количеству знаков после запятой
        local str_fx = tostring(fx)
        local dec_places = 0
        local dot_pos = str_fx:find("%.")
        if dot_pos then
            dec_places = #str_fx - dot_pos
        end
        local k = 10^(-dec_places)
        if dec_places == 0 then k = 1 end

        local dF = 5e-6 * fx + k
        local relF = (dF / fx) * 100

        r.fc[var_name].k[i] = k
        r.fc[var_name].dF[i] = dF
        r.fc[var_name].relF[i] = relF
    end
end

-- 2. Обработка данных осциллографа (частота/период)
for i = 1, #p.of.L_T do
    local LT = p.of.L_T[i]
    local td = p.of.td[i]
    
    if LT > 0 then
        local Tx = LT * td
        local fx = 1 / Tx
        local d_vis = (r.const.b / LT) * 100
        local dT = r.const.d_kp + r.const.d_nr + d_vis
        local abs_dT = Tx * (dT / 100)
        local abs_df = fx * (dT / 100)

        r.of[i] = {
            Tx = Tx,
            fx = fx,
            d_vis = d_vis,
            dT = dT,
            abs_dT = abs_dT,
            abs_df = abs_df
        }
    else
        r.of[i] = { Tx = 0, fx = 0, d_vis = 0, dT = 0, abs_dT = 0, abs_df = 0 }
    end
end

-- 3. Обработка данных фазового сдвига
for i = 1, #p.ph.tau do
    local tau = p.ph.tau[i]
    local LT = p.ph.L_T[i]
    local A = p.ph.A[i]
    local B = p.ph.B[i]

    -- Метод линейной развертки
    local phi_lin = 0
    local d_phi_lin = 0
    local abs_d_phi_lin = 0
    if LT > 0 and tau > 0 then
        phi_lin = 360 * (tau / LT)
        local d_tau = (r.const.b / tau) * 100
        local d_LT = (r.const.b / LT) * 100
        d_phi_lin = d_tau + d_LT
        abs_d_phi_lin = phi_lin * (d_phi_lin / 100)
    end

    -- Метод фигур Лиссажу
    local phi_lis = 0
    local phi_H = 0
    local phi_B = 0
    local abs_d_phi_lis = 0
    if A > 0 and B > 0 then
        phi_lis = math.deg(math.asin(B / A))
        
        local val_H = (B - r.const.b) / (A + r.const.b)
        local val_B = (B + r.const.b) / (A - r.const.b)
        
        if val_H < -1 then val_H = -1 end
        if val_H > 1 then val_H = 1 end
        if val_B < -1 then val_B = -1 end
        if val_B > 1 then val_B = 1 end

        phi_H = math.deg(math.asin(val_H))
        phi_B = math.deg(math.asin(val_B))

        local d1 = math.abs(phi_lis - phi_H)
        local d2 = math.abs(phi_B - phi_lis)
        abs_d_phi_lis = math.max(d1, d2)
    end

    r.ph[i] = {
        phi_lin = phi_lin,
        d_phi_lin = d_phi_lin,
        abs_d_phi_lin = abs_d_phi_lin,
        phi_lis = phi_lis,
        phi_H = phi_H,
        phi_B = phi_B,
        abs_d_phi_lis = abs_d_phi_lis
    }
end
