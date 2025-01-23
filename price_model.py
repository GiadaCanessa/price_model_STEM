# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 14:53:11 2025

@author: GIADCANE
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titolo dell'app
st.title("Prevedi il prezzo dell'energia")

# Input degli studenti
temperatura = st.slider("Temperatura (°C)", min_value=-10, max_value=40, value=20)
produzione_rinnovabili = st.slider("Produzione di rinnovabili (%)", min_value=0, max_value=100, value=50)
prezzo_gas = st.slider("Prezzo del gas naturale (€/MWh)", min_value=10, max_value=200, value=50)
domanda = st.selectbox("Domanda di energia", ["Bassa", "Media", "Alta"])

# Conversione della domanda in un coefficiente numerico
domanda_coeff = {"Bassa": 0.8, "Media": 1.0, "Alta": 1.2}[domanda]

# Calcolo del prezzo
base_price = 50
prezzo_finale = base_price + (domanda_coeff * 20) - (produzione_rinnovabili * 0.3) + (prezzo_gas * 0.1)

# Output
st.write(f"Prezzo dell'energia previsto: **{prezzo_finale:.2f} €/MWh**")

# Visualizzazione del grafico
fig, ax = plt.subplots()
fattori = ['Base Price', 'Domanda', 'Rinnovabili', 'Prezzo Gas']
valori = [base_price, domanda_coeff * 20, -(produzione_rinnovabili * 0.3), prezzo_gas * 0.1]
ax.bar(fattori, valori, color=['blue', 'green', 'orange', 'red'])
ax.set_title("Contributo dei fattori al prezzo finale")
st.pyplot(fig)
