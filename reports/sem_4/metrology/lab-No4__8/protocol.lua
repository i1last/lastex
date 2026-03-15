protocol = {
    resistors_data = {
        R2 = {
            immitanse = 905.7,
            voltmetr = 904
        },
        RN2 = {
            immitanse = 1000,
            voltmetr = 999
        }
    },
    reactive_elements = {
        capacitor = {
            C = 2.094e-9,
            tandelta = 0.014
        },
        induction = {
            L = 1.028e-3,
            Q = 0.275
        }
    }
}

function print_val(val)
    if val == nil or val == 0 then 
        tex.print("---") 
        return 
    end
    
    -- Если число очень маленькое или очень большое, используем экспоненту
    if val < 1e-2 or val >= 1e4 then
        local s = string.format("%.3e", val)
        local base, exp = s:match("^(.*)e([+-]%d+)$")
        tex.print(string.format("$%s \\cdot 10^{%d}$", base, tonumber(exp)))
    else
        -- Для обычных сопротивлений выводим как есть (1 знак после запятой)
        tex.print(string.format("$%g$", val))
    end
end