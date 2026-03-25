dofile("code/protocol.lua")
-- dofile("protocol.lua")
-- Глобальная таблица для результатов
r = {}

-- [[ 1. Обработка RC-цепи ]]
r.RC = {
    R = {},
    C = {},
    phi_vd = {},
    err = {}
}

for i = 1, #p.RC.f do
    local f = p.RC.f[i]
    local U_R = p.RC.U_R[i]
    local U_C = p.RC.U_C[i]
    local I = p.RC.I[i]
    local phi_osc = p.RC.phi[i]
    local omega = 2 * math.pi * f

    -- Расчет параметров
    r.RC.R[i] = U_R / I
    local Z_C = U_C / I
    r.RC.C[i] = 1 / (omega * Z_C)

    -- Расчет сдвига фаз и погрешности
    r.RC.phi_vd[i] = math.atan(-U_C / U_R) * 180 / math.pi
    r.RC.err[i] = math.abs((r.RC.phi_vd[i] - phi_osc) / phi_osc) * 100
end

-- [[ 2. Обработка RL-цепи ]]
r.RL = {
    R = {},
    L = {},
    phi_vd = {},
    err = {}
}

for i = 1, #p.RL.f do
    local f = p.RL.f[i]
    local U_R = p.RL.U_R[i]
    local U_L = p.RL.U_L[i]
    local I = p.RL.I[i]
    local phi_osc = p.RL.phi[i]
    local omega = 2 * math.pi * f

    -- Расчет параметров
    r.RL.R[i] = U_R / I
    local Z_L = U_L / I
    r.RL.L[i] = Z_L / omega

    -- Расчет сдвига фаз и погрешности
    r.RL.phi_vd[i] = math.atan(U_L / U_R) * 180 / math.pi
    r.RL.err[i] = math.abs((r.RL.phi_vd[i] - phi_osc) / phi_osc) * 100
end

-- [[ 3. Обработка RLC-цепи ]]
r.RLC = {}

-- Определение параметров R, L, C из резонансного режима (i=1)
local I_res = p.RLC.I[1]
r.RLC.R_res = p.RLC.U_R[1] / I_res
local Z_L_res = p.RLC.U_L[1] / I_res
local f0 = p.RLC.f[1]
local omega0 = 2 * math.pi * f0

r.RLC.L_res = Z_L_res / omega0
r.RLC.C_res = 1 / (omega0 * Z_L_res)
r.RLC.f0_calc = 1 / (2 * math.pi * math.sqrt(r.RLC.L_res * r.RLC.C_res))
r.RLC.Q = Z_L_res / r.RLC.R_res

-- Расчет теоретических значений для всех режимов
r.RLC.calc = {
    Z = {},
    I = {},
    phi = {},
    err_I = {},
    err_phi = {}
}

for i = 1, #p.RLC.f do
    local f = p.RLC.f[i]
    local omega = 2 * math.pi * f
    local X_L = omega * r.RLC.L_res
    local X_C = 1 / (omega * r.RLC.C_res)
    
    r.RLC.calc.Z[i] = math.sqrt(r.RLC.R_res^2 + (X_L - X_C)^2)
    r.RLC.calc.I[i] = p.RLC.U0[i] / r.RLC.calc.Z[i]
    r.RLC.calc.phi[i] = math.atan((X_L - X_C) / r.RLC.R_res) * 180 / math.pi
    
    r.RLC.calc.err_I[i] = math.abs((r.RLC.calc.I[i] - p.RLC.I[i]) / p.RLC.I[i]) * 100
    -- Погрешность для фазы в резонансе не вычисляем (деление на 0)
    if p.RLC.phi[i] == 0 then
        r.RLC.calc.err_phi[i] = 0
    else
        r.RLC.calc.err_phi[i] = math.abs((r.RLC.calc.phi[i] - p.RLC.phi[i]) / p.RLC.phi[i]) * 100
    end
end

-- Данные для построения АЧХ
r.RLC.plot = {
    f = {},
    I = {}
}
local U0_plot = p.RLC.U0[1] -- Напряжение источника считаем постоянным
for f_plot = 1000, 25000, 100 do
    local omega_plot = 2 * math.pi * f_plot
    local X_L_plot = omega_plot * r.RLC.L_res
    local X_C_plot = 1 / (omega_plot * r.RLC.C_res)
    local Z_plot = math.sqrt(r.RLC.R_res^2 + (X_L_plot - X_C_plot)^2)
    
    table.insert(r.RLC.plot.f, f_plot)
    table.insert(r.RLC.plot.I, U0_plot / Z_plot)
end

