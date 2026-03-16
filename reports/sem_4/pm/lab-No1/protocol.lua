protocol = {
    leather = {
        before = {
            w = 1e-2,
            h = 1.5e-3,
            l = 5e-2
        },
        after = {
            w = 0.35e-2,
            h = 2e-3,
            l = 7.6e-2
        }
    },
    rope = {
        before = {
            d = 1.5e-3,
            l = 5e-2
        },
        after = {
            d = 0,
            l = 7.2e-2
        }
    },
    wire = {
        before = {
            d = 0.5e-3,
            l = 5e-2
        },
        after = {
            d = 0.27e-3,
            l = 7.3e-2
        }
    }
}

function print_sci(val)
    if val == 0 or val == nil then 
        tex.print("---") 
        return 
    end
    -- Форматируем число в экспоненциальный вид
    local s = string.format("%.2e", val)
    local base, exp = s:match("^(.*)e([+-]%d+)$")
    -- Убираем лишние плюсы и нули в экспоненте
    exp = tonumber(exp) 
    tex.print(string.format("$%s \\cdot 10^{%d}$", base, exp))
end