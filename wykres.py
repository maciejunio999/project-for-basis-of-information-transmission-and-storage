import matplotlib.pyplot as plt
import numpy as np

# Stałe
h = 6.63e-34  # [J*s]
c = 3e8       # [m/s]
eta = 0.25    # sprawność fotodiody
wavelength = 1550e-9  # [m]
f = c / wavelength  # [Hz]

# Zakres liczby fotonów na bit (poszerzony z uwagi na n0=6000)
n0_values = np.linspace(500, 10000, 300)

# Różne przepływności [bit/s]
bitrates = {
    "1 Gb/s": 1e9,
    "5 Gb/s": 5e9,
    "20 Gb/s": 20e9
}

# Wykres
plt.figure(figsize=(10, 6))

for label, B in bitrates.items():
    Pr_values = 10 * np.log10(n0_values * h * f * B / (1e-3 * eta))
    plt.plot(n0_values, Pr_values, label=label)

plt.xlabel('Liczba fotonów na bit')
plt.ylabel('Czułość [dBm]')
plt.title('Czułość odbiornika w zależności od liczby fotonów na bit')
plt.grid(True)
plt.legend(title='Przepływność')
plt.tight_layout()

# Zapis wykresu
plt.savefig("czulosc_od_fotonow_wielobit.png")
plt.show()
