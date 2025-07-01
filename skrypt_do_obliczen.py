import math
import pandas as pd
from typing import Literal

# Stałe fizyczne
h = 6.63e-34  # stała Plancka [J*s]
c = 3e8       # prędkość światła [m/s]
eta = 0.25    # sprawność fotodiody
n0 = 6000     # liczba fotonów na bit (poprawiona wartość)

# Parametry łącza
L = 80  # długość łącza w km
alpha_fiber = 0.17  # tłumienność światłowodu SMF-28 [dB/km]
As = 0.1  # tłumienie spawu [dB]
Ac = 0.5  # tłumienie złącza [dB]
Ls = 20  # odległość między spawami [km]
margin = 1  # margines zapasu [dB]
num_splices = math.floor(L / Ls) - 1
num_connectors = 2

# Dyspersja SMF-28
D_fiber = 18  # ps/(nm*km)
total_dispersion = D_fiber * L  # [ps/nm]

# Kompensatory (zastąpiono DCM-60 → DCM-80)
compensators = {
    "DCM-80": {
        "dispersion": -1440,  # ps/nm
        "attenuation": 6.3    # dB
    },
    "PMDCF": {
        "dispersion": -100,      # ps/(nm·km)
        "attenuation_per_km": 0.45  # dB/km
    }
}

# Lasery
lasers = {
    "Laser-1": {
        "power_dBm": 19.0,  # 79.43 mW
    },
    "Laser-2": {
        "power_dBm": 16.0,  # 39.81 mW
    }
}

# Funkcja do obliczeń
def calc_link(power_dBm: float, bitrate_Gbps: float, compensator: Literal["DCM-80", "PMDCF"]):
    f = c / 1550e-9  # częstotliwość [Hz]
    B = bitrate_Gbps * 1e9  # przepływność [bit/s]
    
    # Czułość fotodiody
    Pr = 10 * math.log10(n0 * h * f * B / (1e-3 * eta))  # [dBm]

    # Tłumienie toru
    At = alpha_fiber * L

    # Straty na połączeniach
    Pc = As * num_splices + Ac * num_connectors

    # Kompensacja dyspersji
    if compensator == "DCM-80":
        Ak = compensators["DCM-80"]["attenuation"]
    elif compensator == "PMDCF":
        Lcomp = total_dispersion / abs(compensators["PMDCF"]["dispersion"])
        Ak = Lcomp * compensators["PMDCF"]["attenuation_per_km"]
    else:
        raise ValueError("Nieznany kompensator")

    # Budżet mocy
    required_power = Pr + margin + Pc + At + Ak
    is_valid = power_dBm >= required_power

    return {
        "Bitrate (Gbps)": bitrate_Gbps,
        "Laser Power (dBm)": power_dBm,
        "Receiver Sensitivity (dBm)": round(Pr, 2),
        "Margin (dB)": margin,
        "Splice Loss (dB)": round(As * num_splices, 2),
        "Connector Loss (dB)": round(Ac * num_connectors, 2),
        "Fiber Loss (dB)": round(At, 2),
        "Dispersion Comp. Loss (dB)": round(Ak, 2),
        "Total Required Power (dBm)": round(required_power, 2),
        "Link OK": is_valid
    }

# Obliczenia dla wszystkich kombinacji
results = []
for bitrate in [1, 5, 20]:
    for laser_name, laser in lasers.items():
        for comp_name in compensators.keys():
            res = calc_link(laser["power_dBm"], bitrate, comp_name)
            res["Laser"] = laser_name
            res["Compensator"] = comp_name
            results.append(res)

# Tworzymy DataFrame
df_results = pd.DataFrame(results)
df_results.to_csv("wyniki.csv", index=False)
#print(df_results)
