-- Загрузка исходных данных из протокола
dofile('protocol.lua')

-- Создание таблицы для хранения результатов расчетов
results = {}

----------------------------------------------------------------------
-- Расчеты для п. 1: Исследование переходного процесса
----------------------------------------------------------------------
results.step_response = {}
local data = protocol.step_response
local k_H = protocol.initial_params.k_H

-- Расчет идеального выходного сигнала
results.step_response.u_ideal_i = {}
for i = 1, #data.u_in_i do
    results.step_response.u_ideal_i[i] = k_H * data.u_in_i[i]
end

-- Расчет абсолютной динамической погрешности
-- delta_y(t) = y_real(t) - y_ideal(t)
results.step_response.delta_y_i = {}
for i = 1, #data.u_out_i do
    results.step_response.delta_y_i[i] = data.u_out_i[i] - results.step_response.u_ideal_i[i]
end

-- Расчет относительной динамической погрешности
-- gamma(t) = (delta_y(t) / y_ss) * 100%, где y_ss - установившееся значение
-- Примем установившееся значение равным амплитуде входного сигнала
local u_in_ss = data.u_in_i[#data.u_in_i] -- Последнее значение входного сигнала
results.step_response.gamma_i = {}
for i = 1, #results.step_response.delta_y_i do
    results.step_response.gamma_i[i] = (results.step_response.delta_y_i[i] / u_in_ss) * 100
end


----------------------------------------------------------------------
-- Данные для п. 2: Зависимость времени установления
-- Прямого расчета не требуется, данные используются для построения графиков
----------------------------------------------------------------------
results.settling_freq = protocol.settling_freq
results.settling_beta = protocol.settling_beta


----------------------------------------------------------------------
-- Расчеты для п. 3: Исследование синусоидального воздействия
----------------------------------------------------------------------
results.sine_response = {}
local data_sine = protocol.sine_response

-- Расчет идеального выходного сигнала
results.sine_response.u_ideal_i = {}
for i = 1, #data_sine.u_in_i do
    results.sine_response.u_ideal_i[i] = k_H * data_sine.u_in_i[i]
end

-- Расчет абсолютной динамической погрешности
results.sine_response.delta_y_i = {}
for i = 1, #data_sine.u_out_i do
    results.sine_response.delta_y_i[i] = data_sine.u_out_i[i] - results.sine_response.u_ideal_i[i]
end

-- Определение максимальной (амплитудной) динамической погрешности
results.sine_response.max_abs_delta_y = 0
for i = 1, #results.sine_response.delta_y_i do
    local current_abs_delta = math.abs(results.sine_response.delta_y_i[i])
    if current_abs_delta > results.sine_response.max_abs_delta_y then
        results.sine_response.max_abs_delta_y = current_abs_delta
    end
end