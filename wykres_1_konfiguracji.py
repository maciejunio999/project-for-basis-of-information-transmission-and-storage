import matplotlib.pyplot as plt
import numpy as np

# Parametry
h = 6.63e-34  # [J*s]
c = 3e8       # [m/s]
eta = 0.25
wavelength = 1550e-9  # [m]
f = c / wavelength
bitrate = 1e9  # 1 Gb/s

# Nowa liczba fotonów
n0_values = np.linspace(1000, 10000, 200)
Pr_values = 10 * np.log10(n0_values * h * f * bitrate / (1e-3 * eta))

# Zmienione wartości
min_required_power = -13.32  # zaktualizowane dla DCM-80 i n0=6000
realistic_n0 = 6000
marker_power = 10 * np.log10(realistic_n0 * h * f * bitrate / (1e-3 * eta))

# Wykres
plt.figure(figsize=(10, 6))
plt.plot(n0_values, Pr_values, label='Laser-1 + DCM-80 + 1 Gb/s', color='green')
plt.axhline(min_required_power, color='red', linestyle='--', label=f'Wymagany budżet mocy: {min_required_power} dBm')
plt.axvline(realistic_n0, color='blue', linestyle=':', label=f'n₀ = {realistic_n0}')
plt.scatter([realistic_n0], [marker_power], color='black', zorder=5)

plt.xlabel('Liczba fotonów na bit')
plt.ylabel('Czułość [dBm]')
plt.title('Czułość odbiornika – konfiguracja: Laser-1 + DCM-80 + 1 Gb/s')
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("czulosc_konfiguracja_laser1_dcm80_1g.png")
plt.show()
