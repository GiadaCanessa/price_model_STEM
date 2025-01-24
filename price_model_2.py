# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:52:34 2025

@author: GIADCANE
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Titolo dell'app
st.title("Forecast del prezzo del Power")

# Input utente
st.sidebar.header("Parametri di simulazione")
prezzo_iniziale = st.sidebar.number_input("Prezzo iniziale (€/MWh)", min_value=10, max_value=500, value=100)
volatilita = st.sidebar.slider("Volatilità giornaliera (%)", min_value=1, max_value=100, value=20) / 100
trend = st.sidebar.slider("Trend medio giornaliero (%)", min_value=-10, max_value=10, value=1) / 100
giorni = st.sidebar.number_input("Giorni di forecast", min_value=1, max_value=365, value=30)
simulazioni = st.sidebar.number_input("Numero di simulazioni", min_value=10, max_value=1000, value=100)

# Simulazione Monte Carlo
def simula_prezzi(prezzo_iniziale, volatilita, trend, giorni, simulazioni):
    dt = 1  # Intervallo di tempo (giornaliero)
    prezzi = np.zeros((giorni, simulazioni))
    prezzi[0] = prezzo_iniziale
    
    for t in range(1, giorni):
        random_shocks = np.random.normal(loc=0, scale=1, size=simulazioni)
        prezzi[t] = prezzi[t-1] * np.exp((trend - (volatilita**2) / 2) * dt + volatilita * random_shocks * np.sqrt(dt))
    
    return prezzi

# Genera simulazioni
prezzi_simulati = simula_prezzi(prezzo_iniziale, volatilita, trend, giorni, simulazioni)

# Calcolo forecast medio
prezzo_medio = prezzi_simulati.mean(axis=1)

# Visualizzazione del grafico
st.subheader("Forecast del prezzo del Power")
fig, ax = plt.subplots(figsize=(10, 6))

# Traccia tutte le simulazioni
for i in range(min(simulazioni, 50)):  # Mostra solo le prime 50 simulazioni
    ax.plot(prezzi_simulati[:, i], color='lightgray', alpha=0.5)

# Traccia il forecast medio
ax.plot(prezzo_medio, color='blue', linewidth=2, label='Forecast medio')
ax.set_title("Simulazione del prezzo del Power")
ax.set_xlabel("Giorni")
ax.set_ylabel("Prezzo (€/MWh)")
ax.legend()

st.pyplot(fig)

# Output dei risultati
st.write(f"Prezzo medio stimato a {giorni} giorni: **{prezzo_medio[-1]:.2f} €/MWh**")
