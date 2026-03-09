protocol = {
    DarkResistanceOfCdS = 12.3e+3,
    DarkResistanceOfCdSe = 16.1e+6,
    SpectralCdS = {
        Divisions = {},
        lambda = {},
        E_lambda = {},
        R_c = {12.220, }
    },
    SpectralCdSe = {
        Divisions = {},
        lambda = {},
        E_lambda = {},
        R_c = {}
    },
    Intensity = {
        d = {},
        R_c = {}
    }
}

local raw_data = [[
600  0.476 0.141
700  0.477 0.143
800  0.478 0.145
900  0.479 0.147
1000 0.480 0.150
1100 0.481 0.153
1200 0.482 0.157
1300 0.484 0.163
1400 0.487 0.172
1500 0.490 0.182
1600 0.494 0.195
1700 0.499 0.210
1800 0.505 0.228
1900 0.512 0.248
2000 0.520 0.270
2100 0.528 0.295
2200 0.536 0.323
2300 0.545 0.353
2400 0.555 0.385
2500 0.566 0.420
2600 0.579 0.460
2700 0.594 0.505
2800 0.611 0.560
2900 0.629 0.630
3000 0.649 0.710
3100 0.672 0.830
3200 0.697 0.990
3300 0.725 1.170
3400 0.758 1.370
3500 0.800 1.600 
]]

for div, lam, e_lam in raw_data:gmatch("(%d+)%s+([%d%.]+)%s+([%d%.]+)") do
    local target_tables = { protocol.SpectralCdS, protocol.SpectralCdSe }  
    for _, tab in ipairs(target_tables) do
        table.insert(tab.Divisions, tonumber(div))
        table.insert(tab.lambda,    tonumber(lam) / 1e6)
        table.insert(tab.E_lambda, tonumber(e_lam))
    end
end

local function scale(tbl, factor)
    local res = {}
    for i, v in ipairs(tbl) do res[i] = v * factor end
    return res
end

protocol.SpectralCdS.R_c = scale(
    {12.220, 12.230, 12.230, 12.231, 12.228, 12.225, 12.217, 12.210, 12.197, 12.180, 12.135, 12.063, 11.920, 11.628, 10.951, 9.990, 8.915, 7.670, 5.689, 2.085, 1.754, 3.140, 7.500, 11.174, 11.871, 11.979, 12.030, 12.060, 12.110, 12.120},
1000)

protocol.SpectralCdSe.R_c = scale(
    {3.437, 2.700, 2.102, 1.577, 1.170, 0.850, 0.624, 0.456, 0.332, 0.238, 0.161, 0.105, 0.0724, 0.0468, 0.0341, 0.0362, 0.0366, 0.0368, 0.0440, 0.0656, 0.1235, 0.248, 0.550, 1.839, 6.420, 8.960, 9.700, 10.160, 10.270, 9.880},
1000000)

protocol.Intensity.d = scale(
    {0.01, 0.02, 0.03, 0.05, 0.10, 0.20, 0.30, 0.50, 1.00, 2.00, 4.00},
0.001)

protocol.Intensity.R_c = scale(
    {4.77, 2.77, 1.65, 1.00, 0.47, 0.234, 0.162, 0.103, 0.056, 0.035, 0.0348},
1000000)
