dofile('code/1.lua')

tf = {}

-- Коэффициенты числителя N(s) = N2*s^2 + N0
tf.N2 = n.L1 * n.C1 * n.R1
tf.N0 = n.R1

-- Коэффициенты знаменателя D(s) = D3*s^3 + D2*s^2 + D1*s + D0
tf.D3 = n.L1 * n.L2 * n.C1
tf.D2 = n.L1 * n.C1 * n.R2 + n.L2 * n.C1 * n.R1 + n.L1 * n.C1 * n.R1
tf.D1 = n.L2 + n.R1 * n.R2 * n.C1
tf.D0 = n.R2 + n.R1

-- Расчет корней кубического уравнения (полюсов)
local function cbrt(x)
    if x < 0 then return -math.abs(x)^(1/3) else return x^(1/3) end
end

local a, b, c, d = tf.D3, tf.D2, tf.D1, tf.D0
local p = (3*a*c - b^2) / (3*a^2)
local q = (2*b^3 - 9*a*b*c + 27*a^2*d) / (27*a^3)
local Q = (p/3)^3 + (q/2)^2

local alpha = -q/2 + math.sqrt(Q)
local beta = -q/2 - math.sqrt(Q)
local A_c = cbrt(alpha)
local B_c = cbrt(beta)

local y1 = A_c + B_c
tf.p1_re = y1 - b/(3*a)
tf.p1_im = 0

tf.p2_re = -y1/2 - b/(3*a)
tf.p2_im = (A_c - B_c) * math.sqrt(3) / 2

tf.p3_re = tf.p2_re
tf.p3_im = -tf.p2_im

-- Расчет нулей
tf.z1_im = 1 / math.sqrt(tf.N2)
tf.z2_im = -tf.z1_im

-- Практическая длительность переходного процесса
local min_re = math.min(math.abs(tf.p1_re), math.abs(tf.p2_re))
tf.t_pp = 3 / min_re