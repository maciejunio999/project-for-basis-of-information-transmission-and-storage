import matplotlib.pyplot as plt
import numpy as np

# Stałe i wspólne parametry
h = 6.63e-34  # [J*s]
c = 3e8       # [m/s]
eta = 0.25    # sprawność fotodiody
wavelength = 1550e-9  # [m]
f = c / wavelength  # [Hz]
n0_values = np.linspace(50, 10000, 300)

# Nowe n0 = 6000, więc zakres zwiększamy do porównania

# Konfiguracja optymalna: Laser-1 + DCM-80 + 1 Gb/s
bitrate_opt = 1e9
Pr_opt = 10 * np.log10(n0_values * h * f * bitrate_opt / (1e-3 * eta))
required_power_opt = -13.32  # obliczone ponownie dla DCM-80 i n0=6000

# Konfiguracja porównawcza: Laser-2 + PMDCF + 20 Gb/s
bitrate_alt = 20e9
Pr_alt = 10 * np.log10(n0_values * h * f * bitrate_alt / (1e-3 * eta))
required_power_alt = -3.85  # obliczone dla n0=6000 i 20 Gb/s

# Wykres
plt.figure(figsize=(10, 6))
plt.plot(n0_values, Pr_opt, label='Laser-1 + DCM-80 + 1 Gb/s (optymalna)', color='green')
plt.plot(n0_values, Pr_alt, label='Laser-2 + PMDCF + 20 Gb/s (porównawcza)', color='orange')
plt.axhline(required_power_opt, color='green', linestyle='--', linewidth=1)
plt.axhline(required_power_alt, color='orange', linestyle='--', linewidth=1)

plt.xlabel('Liczba fotonów na bit')
plt.ylabel('Czułość [dBm]')
plt.title('Porównanie dwóch konfiguracji systemu optycznego (n₀ = 6000)')
plt.grid(True)
plt.legend()
plt.tight_layout()

# Zapis wykresu
plt.savefig("porownanie_konfiguracji_wykres.png")
plt.show()
