# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 09:04:59 2026

@author: pipe1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# --- 1. Cargar los datos ---
fs = 1000
datos_emg = np.loadtxt("señal_felipe.txt", skiprows=1)

N_5s = int(10 * fs)
signal_10s = datos_emg[:N_5s]
t_5s = np.arange(len(signal_10s)) / fs

# Señal recortada
plt.figure()
plt.plot(t_5s, signal_10s)
plt.title("Señal EMG (primeros 10 s)")
plt.xlabel("Tiempo (s)")
plt.ylabel("voltaje (v)")
plt.grid()
plt.show()

# --- 2. Definir segmentación ---
duracion_segmento = 1  # segundos
muestras_segmento = int(fs * duracion_segmento)

num_segmentos = 5  # o los que quieras analizar

# --- 3. Loop por segmentos ---
for i in range(num_segmentos):
    
    inicio = i * muestras_segmento
    fin = (i + 1) * muestras_segmento
    
    segmento = datos_emg[inicio:fin]
    N = len(segmento)
    
    # --- Quitar DC ---
    segmento = segmento - np.mean(segmento)
    
    # --- FFT ---
    yf = fft(segmento)
    xf = fftfreq(N, 1/fs)[:N//2]
    
    magnitud = (2.0/N) * np.abs(yf[0:N//2])
    espectro_potencia = magnitud**2
    
    # --- MNF ---
    mnf = np.sum(xf * espectro_potencia) / np.sum(espectro_potencia)
    
    # --- MDF ---
    potencia_acumulada = np.cumsum(espectro_potencia)
    potencia_total = potencia_acumulada[-1]
    indice_mdf = np.where(potencia_acumulada >= potencia_total / 2)[0][0]
    mdf = xf[indice_mdf]
    
    # --- Frecuencia pico ---
    indice_pico = np.argmax(magnitud)
    frecuencia_pico = xf[indice_pico]
    
    # --- Resultados ---
    print(f"\nSegmento {i+1}")
    print(f" - Frecuencia Media (MNF): {mnf:.2f} Hz")
    print(f" - Frecuencia Mediana (MDF): {mdf:.2f} Hz")
    print(f" - Frecuencia Pico: {frecuencia_pico:.2f} Hz")
    
    # --- Gráfica ---
    plt.figure()
    plt.plot(xf, magnitud)
    plt.axvline(mnf, linestyle='--', label='Media')
    plt.axvline(mdf, linestyle='--', label='Mediana')
    plt.axvline(frecuencia_pico, linestyle='-', label='Pico')
    
    plt.title(f"Espectro Segmento {i+1}")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.xlim(0, 250)
    plt.legend()
    plt.grid()
    plt.show()