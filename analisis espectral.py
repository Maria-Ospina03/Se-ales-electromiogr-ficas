# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:04:59 2026

@author: pipe1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# --- 1. Cargar los datos ---
fs = 1000 # Debe ser la misma frecuencia usada en la captura
datos_emg = np.loadtxt("señal_normal_felipe.txt", skiprows=1) # skiprows=1 salta el encabezado
N = len(datos_emg)

# --- 2. Aplicar Transformada Rápida de Fourier (FFT) ---
# Eliminar el componente DC (Offset) restando la media para no sesgar la FFT
datos_sin_dc = datos_emg - np.mean(datos_emg)

yf = fft(datos_sin_dc)
xf = fftfreq(N, 1/fs)[:N//2] # Frecuencias positivas

# Magnitud del espectro de amplitud
magnitud = (2.0/N) * np.abs(yf[0:N//2])
espectro_potencia = magnitud**2 # Potencia para los cálculos de MNF y MDF

# --- 3. Calcular Frecuencia Media (MNF - Mean Frequency) ---
# Ecuación: MNF = Sumatoria(f * P) / Sumatoria(P)
mnf = np.sum(xf * espectro_potencia) / np.sum(espectro_potencia)

# --- 4. Calcular Frecuencia Mediana (MDF - Median Frequency) ---
# Es la frecuencia que divide el área del espectro de potencia a la mitad
potencia_acumulada = np.cumsum(espectro_potencia)
potencia_total = potencia_acumulada[-1]
# Encontrar el índice donde se supera la mitad de la potencia total
indice_mdf = np.where(potencia_acumulada >= potencia_total / 2)[0][0]
mdf = xf[indice_mdf]

# --- 5. Calcular Desplazamiento del Pico Espectral ---
# (Frecuencia dominante)
indice_pico = np.argmax(magnitud)
frecuencia_pico = xf[indice_pico]

# --- Resultados ---
print(f"Resultados del Análisis Espectral:")
print(f" - Frecuencia Media (MNF): {mnf:.2f} Hz")
print(f" - Frecuencia Mediana (MDF): {mdf:.2f} Hz")
print(f" - Frecuencia Pico (Dominante): {frecuencia_pico:.2f} Hz")

# --- 6. Graficar el Espectro de Amplitud ---
plt.figure(figsize=(10, 5))
plt.plot(xf, magnitud, color='darkcyan', label='Espectro de Amplitud')

# Marcar las frecuencias calculadas en la gráfica
plt.axvline(x=mnf, color='r', linestyle='--', label=f'Media: {mnf:.1f} Hz')
plt.axvline(x=mdf, color='g', linestyle='--', label=f'Mediana: {mdf:.1f} Hz')
plt.axvline(x=frecuencia_pico, color='orange', linestyle='-', label=f'Pico: {frecuencia_pico:.1f} Hz')

plt.title("Espectro de Amplitud de la Señal EMG (FFT)")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("[.]")
plt.xlim(0, 250) # Limitamos a 250 Hz para mejor visualización (mayor parte de energía EMG)
plt.legend()
plt.grid(True)
plt.show()