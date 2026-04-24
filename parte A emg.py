# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:08:55 2026

@author: pipe1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Cargar datos
signal = np.loadtxt("dts_dq.txt")
fs = 2000

# Tiempo solo para 5 segundos
N_5s = int(5 * fs)
signal_5s = signal[:N_5s]
t_5s = np.arange(len(signal_5s)) / fs

# Señal recortada
plt.figure()
plt.plot(t_5s[::10], signal_5s[::10])
plt.title("Señal EMG (primeros 5 s)")
plt.xlabel("Tiempo (s)")
plt.ylabel("voltaje (v)")
plt.grid()
plt.show()

# SEGMENTACIÓN MANUAL (AJUSTAR)
c1 = signal[0:2000]
c2 = signal[2000:4000]
c3 = signal[4000:6000]
c4 = signal[6000:8000]
c5 = signal[8000:10000]

contracciones = [c1, c2, c3, c4, c5]

# Función de frecuencias
def calcular_frecuencias(segmento, fs):
    N = len(segmento)
    Y = fft(segmento)
    freqs = fftfreq(N, 1/fs)
    
    mask = freqs > 0
    freqs = freqs[mask]
    Y = np.abs(Y[mask])
    
    f_media = np.sum(freqs * Y) / np.sum(Y)
    
    suma_total = np.sum(Y)
    suma_acum = np.cumsum(Y)
    f_mediana = freqs[np.where(suma_acum >= suma_total/2)[0][0]]
    
    return f_media, f_mediana, freqs, Y

# Cálculo
for i, c in enumerate(contracciones):
    f_media, f_mediana, freqs, Y = calcular_frecuencias(c, fs)
    
    print(f"Contracción {i+1}")
    print(f"Frecuencia media: {f_media:.2f} Hz")
    print(f"Frecuencia mediana: {f_mediana:.2f} Hz\n")
    
    plt.figure()
    plt.plot(freqs, Y)
    plt.axvline(f_media, linestyle='--')
    plt.axvline(f_mediana, linestyle='--')
    plt.title(f"Espectro Contracción {i+1}")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Magnitud")
    plt.grid()
    plt.show()