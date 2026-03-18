--[[
    Модуль для обработки результатов лабораторной работы №5.
    Выполняет коррекцию данных, численное дифференцирование
    и расчет температурных коэффициентов.
]]

-- Импорт исходных данных из протокола
dofile("code/protocol.lua")

-- Глобальная таблица для хранения результатов
r = {}

-- Коэффициенты линейного расширения диэлектриков (alpha_l_d), 1/K
r.ald = {
    3e-6,    -- 1. Неорганическое стекло
    13.5e-6, -- 2. Слюда
    8e-6,    -- 3. Тиконд
    1.1e-4,  -- 4. Полипропилен
    12e-6    -- 5. Сегнетокерамика
}

--[[
    Вспомогательная функция для вычитания емкости C0.
    @param c_table - таблица измеренных емкостей
    @return new_table - таблица скорректированных емкостей
]]
local function correct_capacitance(c_table)
    local new_table = {}
    for i = 1, #c_table do
        new_table[i] = c_table[i] - p.C0
    end
    return new_table
end

-- Коррекция емкостей для всех образцов
r.C1_net = correct_capacitance(p.C1)
r.C2_net = correct_capacitance(p.C2)
r.C3_net = correct_capacitance(p.C3)
r.C4_net = correct_capacitance(p.C4)
r.C5_net = correct_capacitance(p.C5)


--[[
    Основная функция для расчета коэффициентов alpha_C и alpha_epsilon.
    @param C_net_table - таблица скорректированных емкостей
    @param ald_val - значение коэффициента линейного расширения
    @return ac_table, ae_table - таблицы рассчитанных коэффициентов
]]
local function calculate_coeffs(C_net_table, ald_val)
    local ac_table = {}
    local ae_table = {}
    -- Итерация до предпоследнего элемента, т.к. используется метод конечных разностей
    for i = 1, #C_net_table - 1 do
        local dC = C_net_table[i+1] - C_net_table[i]
        local dt = p.t[i+1] - p.t[i]

        if dt == 0 then
            -- Обработка случая деления на ноль, если температуры совпадают
            -- В данном контексте маловероятно, но является хорошей практикой
            dCdt = 0
        else
            dCdt = dC / dt
        end

        local ac = (1 / C_net_table[i]) * dCdt
        local ae = ac - ald_val

        table.insert(ac_table, ac)
        table.insert(ae_table, ae)
    end
    return ac_table, ae_table
end

-- Расчет коэффициентов для всех образцов
r.ac1, r.ae1 = calculate_coeffs(r.C1_net, r.ald[1])
r.ac2, r.ae2 = calculate_coeffs(r.C2_net, r.ald[2])
r.ac3, r.ae3 = calculate_coeffs(r.C3_net, r.ald[3])
r.ac4, r.ae4 = calculate_coeffs(r.C4_net, r.ald[4])
r.ac5, r.ae5 = calculate_coeffs(r.C5_net, r.ald[5])

-- Создание таблицы температур, соответствующей рассчитанным коэффициентам
-- (на один элемент короче исходной)
r.t_calc = {}
for i = 1, #p.t - 1 do
    r.t_calc[i] = p.t[i]
end