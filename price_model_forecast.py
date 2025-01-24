# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 16:02:55 2025

@author: GIADCANE
"""
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Titolo dell'app
st.title("Forecast del prezzo del Power")

# Parametri regolabili dagli studenti
st.sidebar.header("Parametri di simulazione")
prezzo_iniziale = st.sidebar.number_input("Prezzo iniziale (€/MWh)", min_value=50, max_value=180, value=100)

# Parametro aggregato per domanda
orario_e_giorno = st.sidebar.selectbox(
    "Condizione di utilizzo",
    ["Picco (giorno lavorativo)", "Fuori-picco (notte o weekend)"]
)

# Produzione da rinnovabili (% della capacità massima)
produzione_rinnovabili = st.sidebar.slider(
    "Produzione da rinnovabili (% capacità massima)", min_value=0, max_value=100, value=45
)

# Costo del gas naturale
costo_gas = st.sidebar.slider("Costo del gas naturale (€/MWh)", min_value=20, max_value=90, value=40)

# Pesi corretti dei parametri
peso_domanda = {"Picco (giorno lavorativo)": 10, "Fuori-picco (notte o weekend)": -5}
peso_rinnovabili = -0.1  # Ogni 10% di produzione rinnovabile riduce il prezzo
peso_gas = 0.1  # Incremento lineare in base al costo del gas

# Simulazione Monte Carlo
def simula_prezzi(prezzo_iniziale, orario_e_giorno, rinnovabili, gas, giorni, simulazioni):
    dt = 1  # Giorno
    prezzi = np.zeros((giorni, simulazioni))
    prezzi[0] = prezzo_iniziale

    for t in range(1, giorni):
        random_shocks = np.random.normal(0, 1, simulazioni)  # Shock casuale
        # Impatto combinato dei parametri
        impatto = (
            peso_domanda[orario_e_giorno]
            + peso_rinnovabili * rinnovabili
            + peso_gas * gas
        )
        # Calcolo del prezzo con volatilità casuale
        prezzi[t] = np.clip(
            prezzi[t-1] + impatto * dt + random_shocks * prezzi[t-1] * 0.01,
            30,  # Limite minimo realistico
            300   # Limite massimo realistico
        )

    return prezzi

# Input studenti
giorni = st.sidebar.number_input("Giorni di forecast", min_value=1, max_value=30, value=20)
simulazioni = st.sidebar.number_input("Numero di simulazioni", min_value=10, max_value=1000, value=400)

# Genera simulazioni
prezzi_simulati = simula_prezzi(
    prezzo_iniziale, orario_e_giorno, produzione_rinnovabili, costo_gas, giorni, simulazioni
)

# Calcolo del forecast medio
prezzo_medio = prezzi_simulati.mean(axis=1)

# Visualizzazione del grafico
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

# Risultati finali
st.write(f"Prezzo medio stimato dopo {giorni} giorni: **{prezzo_medio[-1]:.2f} €/MWh**")
