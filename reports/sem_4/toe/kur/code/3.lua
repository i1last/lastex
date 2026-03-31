dofile('code/2.lua')

fact = {
    K = tf.N2 / tf.D3,
    alpha1 = -tf.p1_re,
    alpha2 = -tf.p2_re,
    beta2 = tf.p2_im,
    omega0_sq = tf.z1_im^2
}

freq = {}
freq.A0 = tf.N0 / tf.D0

-- Функция расчета АЧХ и ФЧХ через множители
function get_h_factored(w)
    -- Числитель: |w0^2 - w^2|
    local num_mag = math.abs(fact.omega0_sq - w^2)
    local num_phi = (w < tf.z1_im) and 0 or -math.pi
    
    -- Знаменатель: произведение модулей и сумма аргументов
    local den_mag = math.sqrt(w^2 + fact.alpha1^2) * 
                    math.sqrt(fact.alpha2^2 + (w - fact.beta2)^2) * 
                    math.sqrt(fact.alpha2^2 + (w + fact.beta2)^2)
    
    local den_phi = math.atan(w, fact.alpha1) + 
                    math.atan(w - fact.beta2, fact.alpha2) + 
                    math.atan(w + fact.beta2, fact.alpha2)
    
    local a_w = fact.K * (num_mag / den_mag)
    local phi_w = num_phi - den_phi
    
    return a_w, phi_w
end

-- Контрольные точки
freq.w1 = 0
freq.A1, freq.Phi1 = get_h_factored(freq.w1)

freq.w2 = tf.z1_im
freq.A2, freq.Phi2 = get_h_factored(freq.w2)

freq.level = 0.707 * freq.A0
freq.w_c = 0.45 
freq.td = math.rad(25) / 0.5 -- Оценочное значение из ФЧХ