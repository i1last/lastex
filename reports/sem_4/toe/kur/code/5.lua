dofile('code/2.lua')
dofile('code/3.lua')
dofile('code/4.lua')
local complex = require "code/complex"


-- С ДАННЫМ ПУНКТОМ ПРОБЕЛМЫ В РАССЧЕТАХ
-- ИЗ-ЗА КОТОРЫХ БЫЛО РЕШЕНО УЙТИ ОТ
-- LUA В ПОЛЬЗУ PYTHON. ЕГО СЛЕДУЕТ
-- ПЕРЕДЕЛАТЬ ПОЛНОСТЬЮ


res = {}

-- Вспомогательные функции для комплексной арифметики
local function c_mul(r1, i1, r2, i2) return r1*r2 - i1*i2, r1*i2 + r2*i1 end
local function c_div(r1, i1, r2, i2)
    local den = r2^2 + i2^2
    return (r1*r2 + i1*i2)/den, (i1*r2 - r1*i2)/den
end
local function poly_eval(coeffs, r, i)
    local res_r, res_i = coeffs[1], 0
    local s_r, s_i = r, i
    for k=2, #coeffs do
        local term_r, term_i = c_mul(coeffs[k], 0, s_r, s_i)
        res_r, res_i = res_r + term_r, res_i + term_i
        s_r, s_i = c_mul(s_r, s_i, r, i)
    end
    return res_r, res_i
end

-- Коэффициенты числителя N(s) и производной знаменателя D'(s)
local n_coeffs = {tf.N0, 0, tf.N2}
local dp_coeffs = {tf.D1, 2*tf.D2, 3*tf.D3}

-- Вычеты для импульсной характеристики h(t)
-- Полюс 1 (вещественный)
local n1r, n1i = c_mul(tf.p1_re, -tf.z1_im, tf.p1_re, tf.z1_im)
local d1r, d1i = c_mul(tf.p1_re - tf.p2_re, -tf.p2_im, tf.p1_re - tf.p2_re, tf.p2_im)
res.A1_r, _ = c_div(n1r, n1i, d1r, d1i)

-- Полюс 2 (комплексный)
local calc_A2 = function(s)
    return (s + complex.new(0,tf.z1_im)) *
    (s + complex.new(0,tf.z2_im)) /
    (s + complex.new(0,tf.p1_re)) / 
    (s + complex.new(tf.p2_re, tf.p2_im))
end
res.A2_r, res.A2_i = complex.get(calc_A2(complex.new(-tf.p2_re, -tf.p2_im)))
print(res.A1_r)

-- -- local s2 = tf.p2_im + tf.p2_re
-- -- print(tf.p2_re, -tf.z1_im, tf.p1_re, tf.z1_im)
-- z = complex.new(5, 3)
-- zs = tostring( z )
-- sss = 'hello'
-- print(tostring( z ))
-- -- (s)
-- local n2r, n2i = c_mul(tf.p2_re, -tf.z1_im, tf.p1_re, tf.z1_im)
-- -- local n2_r, n2_i = poly_eval(n_coeffs, tf.p2_re, tf.p2_im)
-- -- local dp2_r, dp2_i = poly_eval(dp_coeffs, tf.p2_re, tf.p2_im)
-- -- local A2_r, A2_i = c_div(n2_r, n2_i, dp2_r, dp2_i)
-- local A2_r, A2_i = 0,0

res.A2_r = A2_r
res.A2_i = A2_i
res.A2_mag_half = math.sqrt(A2_r^2 + A2_i^2)
res.A2_mag = 2 * res.A2_mag_half
res.A2_arg = math.deg(math.atan(A2_i, A2_r))

-- Вычеты для переходной характеристики h1(t) = H(s)/s
res.B0 = tf.N0 / tf.D0
res.B1_r, _ = c_div(res.A1_r, 0, tf.p1_re, 0)

local B2_r, B2_i = c_div(A2_r, A2_i, tf.p2_re, tf.p2_im)
res.B2_r = B2_r
res.B2_i = B2_i
res.B2_mag_half = math.sqrt(B2_r^2 + B2_i^2)
res.B2_mag = 2 * res.B2_mag_half
res.B2_arg = math.deg(math.atan(B2_i, B2_r))

-- Аналитическая функция h1(t)
local function h1_an(t)
    return res.B0 + res.B1_r * math.exp(tf.p1_re * t) + 
           res.B2_mag * math.exp(tf.p2_re * t) * math.cos(tf.p2_im * t + math.rad(res.B2_arg))
end

-- Параметры численного метода Эйлера
res.tau1 = 1 / math.abs(tf.p1_re)
res.tau2 = 1 / math.abs(tf.p2_re)
res.T2 = 2 * math.pi / math.abs(tf.p2_im)

local dt_calc = 0.2 * math.min(res.tau1, res.tau2, res.T2 / 4)
res.dt = tonumber(string.format("%.3f", dt_calc))
if res.dt == 0 then res.dt = 0.001 end

res.t_max = 3 * math.max(res.tau1, res.tau2)
local steps = math.floor(res.t_max / res.dt)

-- Инициализация переменных состояния для метода Эйлера
local x1, x2, x3 = 0, 0, 0 -- uC1, iL1, iL2
local input_F = 1

-- Фиксация первых двух шагов для демонстрации в отчете
res.dx1_0 = mat.A11*x1 + mat.A12*x2 + mat.A13*x3 + mat.B11*input_F
res.dx2_0 = mat.A21*x1 + mat.A22*x2 + mat.A23*x3 + mat.B21*input_F
res.dx3_0 = mat.A31*x1 + mat.A32*x2 + mat.A33*x3 + mat.B31*input_F

res.x1_1 = x1 + res.dt * res.dx1_0
res.x2_1 = x2 + res.dt * res.dx2_0
res.x3_1 = x3 + res.dt * res.dx3_0

res.dx1_1 = mat.A11*res.x1_1 + mat.A12*res.x2_1 + mat.A13*res.x3_1 + mat.B11*input_F
res.dx2_1 = mat.A21*res.x1_1 + mat.A22*res.x2_1 + mat.A23*res.x3_1 + mat.B21*input_F
res.dx3_1 = mat.A31*res.x1_1 + mat.A32*res.x2_1 + mat.A33*res.x3_1 + mat.B31*input_F

res.x1_2 = res.x1_1 + res.dt * res.dx1_1
res.x2_2 = res.x2_1 + res.dt * res.dx2_1
res.x3_2 = res.x3_1 + res.dt * res.dx3_1

-- Формирование данных для таблицы LaTeX
res.euler_paths = {}
local print_step = math.max(1, math.floor(steps / 15)) -- Сокращение вывода для читаемости

for i = 0, steps do
    local t = i * res.dt
    local an_val = h1_an(t)
    
    if i % print_step == 0 or i == steps then
        table.insert(res.euler_paths, string.format("%f,%f,%f,%f,%f", t, x1, x2, x3, an_val))
    end
    
    local dx1 = mat.A11*x1 + mat.A12*x2 + mat.A13*x3 + mat.B11*input_F
    local dx2 = mat.A21*x1 + mat.A22*x2 + mat.A23*x3 + mat.B21*input_F
    local dx3 = mat.A31*x1 + mat.A32*x2 + mat.A33*x3 + mat.B31*input_F
    
    x1 = x1 + res.dt * dx1
    x2 = x2 + res.dt * dx2
    x3 = x3 + res.dt * dx3
end